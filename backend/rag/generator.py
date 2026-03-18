"""
Response generator for the IT Helpdesk RAG pipeline.

Uses the Anthropic Claude API to produce grounded answers from retrieved
context chunks. Supports multi-turn conversation history.
"""

import logging
import os
from typing import Any, Optional

import anthropic
from dotenv import load_dotenv

from backend.rag.reranker import RankedChunk

load_dotenv()

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"
TEMPERATURE = 0.2
MAX_TOKENS = 1024
MAX_HISTORY_MESSAGES = 5

SYSTEM_PROMPT = """You are an IT Helpdesk assistant. Follow these rules strictly:

1. **Only answer from the provided context.** Do not use external knowledge.
2. **Cite your sources** by referencing the document name in parentheses, e.g. (source: password_reset.md).
3. **Use numbered steps** when providing instructions or procedures.
4. **Be professional but friendly.** Use clear, concise language.
5. If the context does not contain enough information to answer the question, respond with:
   "I don't have information on this topic. Let me escalate this to our IT team."
6. If the user's question is ambiguous, ask a clarifying question before answering.
7. Never fabricate information or procedures."""

NO_CONTEXT_RESPONSE = (
    "I don't have information on this topic. "
    "Let me escalate this to our IT team."
)


def _build_context_block(chunks: list[RankedChunk]) -> str:
    """Format retrieved chunks into a context block for the prompt."""
    if not chunks:
        return "No relevant documents were found."

    parts: list[str] = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Document {i}] (source: {chunk.source_doc}, category: {chunk.category})\n"
            f"{chunk.text}"
        )
    return "\n\n---\n\n".join(parts)


def _trim_history(history: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep only the last MAX_HISTORY_MESSAGES messages for multi-turn."""
    if len(history) <= MAX_HISTORY_MESSAGES:
        return history
    return history[-MAX_HISTORY_MESSAGES:]


class Generator:
    """Generates responses using Claude with retrieved context."""

    def __init__(self) -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning(
                "ANTHROPIC_API_KEY not set. Generator will fail on generate()."
            )
        self._client = anthropic.Anthropic(api_key=api_key or "")

    def generate(
        self,
        query: str,
        chunks: list[RankedChunk],
        conversation_history: Optional[list[dict[str, str]]] = None,
    ) -> dict[str, Any]:
        """
        Generate a response grounded in the retrieved context.

        Args:
            query: The user's current question.
            chunks: Reranked context chunks.
            conversation_history: Previous messages as
                [{"role": "user"|"assistant", "content": "..."}].

        Returns:
            Dict with keys: response, sources, confidence, model.
        """
        context_block = _build_context_block(chunks)

        user_message = (
            f"### Context\n{context_block}\n\n"
            f"### Question\n{query}"
        )

        # Build messages list with history
        messages: list[dict[str, str]] = []
        if conversation_history:
            messages.extend(_trim_history(conversation_history))
        messages.append({"role": "user", "content": user_message})

        if not chunks:
            logger.info("No context chunks provided; returning fallback response.")
            return {
                "response": NO_CONTEXT_RESPONSE,
                "sources": [],
                "confidence": 0.0,
                "model": MODEL,
            }

        try:
            api_response = self._client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                system=SYSTEM_PROMPT,
                messages=messages,
            )

            response_text = api_response.content[0].text

            sources = list({chunk.source_doc for chunk in chunks})
            avg_score = sum(c.final_score for c in chunks) / len(chunks)

            logger.info(
                "Generated response (model=%s, confidence=%.2f, sources=%s)",
                MODEL,
                avg_score,
                sources,
            )

            return {
                "response": response_text,
                "sources": sources,
                "confidence": round(avg_score, 4),
                "model": MODEL,
            }

        except anthropic.AuthenticationError:
            logger.error("Anthropic API authentication failed. Check ANTHROPIC_API_KEY.")
            return {
                "response": "I'm experiencing an authentication issue. Please contact IT support directly.",
                "sources": [],
                "confidence": 0.0,
                "model": MODEL,
            }
        except anthropic.RateLimitError:
            logger.error("Anthropic API rate limit exceeded.")
            return {
                "response": "I'm currently experiencing high demand. Please try again in a moment.",
                "sources": [],
                "confidence": 0.0,
                "model": MODEL,
            }
        except Exception:
            logger.exception("Failed to generate response")
            return {
                "response": "I encountered an error processing your request. Please try again.",
                "sources": [],
                "confidence": 0.0,
                "model": MODEL,
            }
