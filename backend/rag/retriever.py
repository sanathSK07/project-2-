"""
Semantic similarity retriever for the IT Helpdesk RAG pipeline.

Retrieves the top-k most relevant document chunks from ChromaDB
based on cosine similarity of embeddings.
"""

import logging
from dataclasses import dataclass
from typing import Any, Optional

from backend.knowledge_base.embedder import Embedder
from backend.knowledge_base.vector_store import VectorStore

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    """A single retrieved chunk with its similarity score and metadata."""

    text: str
    source_doc: str
    category: str
    chunk_index: int
    title: str
    similarity_score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "source_doc": self.source_doc,
            "category": self.category,
            "chunk_index": self.chunk_index,
            "title": self.title,
            "similarity_score": self.similarity_score,
        }


class Retriever:
    """Performs semantic similarity search against the vector store."""

    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k
        self._embedder = Embedder()
        self._vector_store: VectorStore = self._embedder.vector_store

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        category: Optional[str] = None,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant chunks for a query.

        Args:
            query: The user's question or search text.
            top_k: Number of results to return (defaults to self.top_k).
            category: Optional category filter for scoped retrieval.

        Returns:
            List of RetrievedChunk objects sorted by similarity (best first).
        """
        k = top_k or self.top_k

        query_embedding = self._embedder.embed_query(query)

        results = self._vector_store.query(
            query_embedding=query_embedding,
            n_results=k,
            category=category,
        )

        chunks = self._parse_results(results)

        logger.info(
            "Retrieved %d chunks for query (category=%s): %.80s...",
            len(chunks),
            category,
            query,
        )
        return chunks

    @staticmethod
    def _parse_results(results: dict[str, Any]) -> list[RetrievedChunk]:
        """Convert raw ChromaDB results into RetrievedChunk objects."""
        chunks: list[RetrievedChunk] = []

        if not results or not results.get("ids") or not results["ids"][0]:
            return chunks

        ids = results["ids"][0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for i in range(len(ids)):
            # ChromaDB cosine distance: 0 = identical, 2 = opposite.
            # Convert to similarity score: 1 - (distance / 2).
            distance = distances[i] if i < len(distances) else 1.0
            similarity = 1.0 - (distance / 2.0)

            meta = metadatas[i] if i < len(metadatas) else {}
            text = documents[i] if i < len(documents) else ""

            chunk = RetrievedChunk(
                text=text,
                source_doc=meta.get("source_doc", "unknown"),
                category=meta.get("category", "general"),
                chunk_index=meta.get("chunk_index", 0),
                title=meta.get("title", ""),
                similarity_score=round(similarity, 4),
            )
            chunks.append(chunk)

        return chunks
