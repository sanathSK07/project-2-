"""
FastAPI route definitions for the IT Helpdesk API.

Endpoints:
    POST /chat          - Main chat endpoint (Router -> Retrieval -> Reranker -> Generator -> Escalation)
    POST /feedback      - Submit feedback on a response
    GET  /analytics     - Retrieve feedback analytics
    POST /admin/reindex - Re-index the knowledge base (requires API key)
    GET  /health        - Health check
"""

import logging
import os
import uuid
from typing import Any, Optional

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, Field

from backend.agents.escalation_agent import EscalationAgent
from backend.agents.feedback_agent import FeedbackAgent
from backend.agents.router_agent import RouterAgent
from backend.rag.generator import Generator
from backend.rag.reranker import rerank
from backend.rag.retriever import Retriever

logger = logging.getLogger(__name__)

router = APIRouter()

# Lazy-initialized singletons to avoid import-time heavy loading.
_retriever: Optional[Retriever] = None
_generator: Optional[Generator] = None
_router_agent: Optional[RouterAgent] = None
_escalation_agent: Optional[EscalationAgent] = None
_feedback_agent: Optional[FeedbackAgent] = None

# In-memory conversation store (shared with main.py via import).
conversation_store: dict[str, list[dict[str, str]]] = {}


def _get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def _get_generator() -> Generator:
    global _generator
    if _generator is None:
        _generator = Generator()
    return _generator


def _get_router_agent() -> RouterAgent:
    global _router_agent
    if _router_agent is None:
        _router_agent = RouterAgent()
    return _router_agent


def _get_escalation_agent() -> EscalationAgent:
    global _escalation_agent
    if _escalation_agent is None:
        _escalation_agent = EscalationAgent()
    return _escalation_agent


def _get_feedback_agent() -> FeedbackAgent:
    global _feedback_agent
    if _feedback_agent is None:
        _feedback_agent = FeedbackAgent()
    return _feedback_agent


# ---------- Request / Response models ----------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sources: list[str]
    category: str
    confidence: float
    escalated: bool
    conversation_id: str
    message_id: str
    escalation_details: Optional[dict[str, Any]] = None


class FeedbackRequest(BaseModel):
    conversation_id: str
    message_id: str
    rating: str = Field(..., pattern=r"^(helpful|not_helpful)$")
    feedback_text: Optional[str] = None


class FeedbackResponse(BaseModel):
    status: str
    message: str


class AnalyticsResponse(BaseModel):
    total_feedback: int
    helpful_count: int
    not_helpful_count: int
    satisfaction_rate: float
    by_category: dict[str, Any]


class ReindexResponse(BaseModel):
    status: str
    chunks_indexed: int


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


# ---------- Endpoints ----------

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint. Processes a user message through the full RAG pipeline:
    Router -> Retrieval -> Reranker -> Generator -> Escalation check.
    """
    try:
        # Resolve or create conversation.
        conv_id = request.conversation_id or str(uuid.uuid4())
        if conv_id not in conversation_store:
            conversation_store[conv_id] = []

        message_id = str(uuid.uuid4())

        # 1. Route: classify the query.
        router_agent = _get_router_agent()
        category = router_agent.classify(request.message)
        logger.info("Routed to category: %s", category)

        # 2. Retrieve: semantic search with category filter.
        retriever = _get_retriever()
        retrieved_chunks = retriever.retrieve(
            query=request.message,
            category=category if category != "general" else None,
        )

        # If category-filtered search returns few results, try without filter.
        if len(retrieved_chunks) < 2 and category != "general":
            logger.info("Few results with category filter; broadening search.")
            retrieved_chunks = retriever.retrieve(query=request.message)

        # 3. Rerank: score and select top 3.
        ranked_chunks = rerank(query=request.message, chunks=retrieved_chunks)

        # 4. Generate: produce response with context.
        generator = _get_generator()
        history = conversation_store[conv_id]
        result = generator.generate(
            query=request.message,
            chunks=ranked_chunks,
            conversation_history=history,
        )

        # 5. Escalation check.
        escalation_agent = _get_escalation_agent()
        escalation = escalation_agent.check(
            query=request.message,
            confidence=result["confidence"],
            conversation_history=history,
            category=category,
        )

        # Update conversation history.
        conversation_store[conv_id].append({"role": "user", "content": request.message})
        conversation_store[conv_id].append({"role": "assistant", "content": result["response"]})

        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            category=category,
            confidence=result["confidence"],
            escalated=escalation.should_escalate,
            conversation_id=conv_id,
            message_id=message_id,
            escalation_details=escalation.to_dict() if escalation.should_escalate else None,
        )

    except Exception:
        logger.exception("Error processing chat request")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your request.",
        )


@router.post("/feedback", response_model=FeedbackResponse)
async def feedback(request: FeedbackRequest) -> FeedbackResponse:
    """Record user feedback on a chatbot response."""
    try:
        feedback_agent = _get_feedback_agent()

        # Look up original query/response from conversation history.
        history = conversation_store.get(request.conversation_id, [])
        query = ""
        response_text = ""
        category = "general"

        # Find the last user/assistant pair.
        for i, msg in enumerate(history):
            if msg["role"] == "user":
                query = msg["content"]
            elif msg["role"] == "assistant":
                response_text = msg["content"]

        feedback_agent.record_feedback(
            conversation_id=request.conversation_id,
            message_id=request.message_id,
            query=query,
            response=response_text,
            rating=request.rating,
            category=category,
            feedback_text=request.feedback_text,
        )

        return FeedbackResponse(
            status="success",
            message="Feedback recorded. Thank you!",
        )

    except Exception:
        logger.exception("Error recording feedback")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record feedback.",
        )


@router.get("/analytics", response_model=AnalyticsResponse)
async def analytics() -> AnalyticsResponse:
    """Return feedback analytics and satisfaction metrics."""
    try:
        feedback_agent = _get_feedback_agent()
        stats = feedback_agent.get_analytics()
        return AnalyticsResponse(**stats)
    except Exception:
        logger.exception("Error fetching analytics")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch analytics.",
        )


@router.post("/admin/reindex", response_model=ReindexResponse)
async def reindex(x_api_key: str = Header(...)) -> ReindexResponse:
    """
    Re-index all documents in the knowledge base.
    Requires a valid API key passed via the X-API-Key header.
    """
    expected_key = os.getenv("ADMIN_API_KEY", "")
    if not expected_key or x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )

    try:
        from backend.knowledge_base.embedder import Embedder

        embedder = Embedder()
        count = embedder.reindex()

        # Reset the retriever so it picks up the new index.
        global _retriever
        _retriever = None

        return ReindexResponse(status="success", chunks_indexed=count)

    except Exception:
        logger.exception("Error during re-indexing")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Re-indexing failed.",
        )


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="IT Helpdesk AI Chatbot",
        version="1.0.0",
    )
