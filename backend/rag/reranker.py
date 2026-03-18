"""
Reranker for the IT Helpdesk RAG pipeline.

Scores retrieved chunks using a combination of similarity score,
keyword overlap with the original query, and priority weighting
for security-related documents. Returns the top 3 after reranking.
"""

import logging
import re
from dataclasses import dataclass
from typing import Any

from backend.rag.retriever import RetrievedChunk

logger = logging.getLogger(__name__)

# Security documents receive a priority boost.
SECURITY_PRIORITY_BOOST = 0.10

# Weight factors for the final score.
WEIGHT_SIMILARITY = 0.55
WEIGHT_KEYWORD = 0.30
WEIGHT_PRIORITY = 0.15

# Default number of top results to return.
DEFAULT_TOP_N = 3


@dataclass
class RankedChunk:
    """A chunk after reranking with a composite score."""

    text: str
    source_doc: str
    category: str
    chunk_index: int
    title: str
    similarity_score: float
    keyword_score: float
    priority_score: float
    final_score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "source_doc": self.source_doc,
            "category": self.category,
            "chunk_index": self.chunk_index,
            "title": self.title,
            "similarity_score": self.similarity_score,
            "keyword_score": self.keyword_score,
            "priority_score": self.priority_score,
            "final_score": self.final_score,
        }


def _tokenize(text: str) -> set[str]:
    """Lowercase tokenization, stripping non-alphanumeric characters."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _compute_keyword_overlap(query: str, chunk_text: str) -> float:
    """
    Compute keyword overlap between query and chunk as a ratio [0, 1].
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return 0.0
    chunk_tokens = _tokenize(chunk_text)
    overlap = query_tokens & chunk_tokens
    return len(overlap) / len(query_tokens)


def _compute_priority_score(category: str, query: str) -> float:
    """
    Assign a priority score. Security-related documents get a boost.
    """
    security_terms = {"security", "phishing", "malware", "virus", "breach", "encryption", "firewall"}
    query_tokens = _tokenize(query)

    if category == "security":
        return SECURITY_PRIORITY_BOOST
    if query_tokens & security_terms:
        return SECURITY_PRIORITY_BOOST * 0.5
    return 0.0


def rerank(
    query: str,
    chunks: list[RetrievedChunk],
    top_n: int = DEFAULT_TOP_N,
) -> list[RankedChunk]:
    """
    Rerank retrieved chunks and return the top_n results.

    Scoring formula:
        final = (WEIGHT_SIMILARITY * similarity)
              + (WEIGHT_KEYWORD   * keyword_overlap)
              + (WEIGHT_PRIORITY  * priority_score)

    Args:
        query: The original user query.
        chunks: Retrieved chunks from the retriever.
        top_n: Number of results to return after reranking.

    Returns:
        List of RankedChunk sorted by final_score descending.
    """
    if not chunks:
        return []

    ranked: list[RankedChunk] = []

    for chunk in chunks:
        keyword_score = _compute_keyword_overlap(query, chunk.text)
        priority_score = _compute_priority_score(chunk.category, query)

        final_score = (
            WEIGHT_SIMILARITY * chunk.similarity_score
            + WEIGHT_KEYWORD * keyword_score
            + WEIGHT_PRIORITY * priority_score
        )

        ranked.append(
            RankedChunk(
                text=chunk.text,
                source_doc=chunk.source_doc,
                category=chunk.category,
                chunk_index=chunk.chunk_index,
                title=chunk.title,
                similarity_score=chunk.similarity_score,
                keyword_score=round(keyword_score, 4),
                priority_score=round(priority_score, 4),
                final_score=round(final_score, 4),
            )
        )

    ranked.sort(key=lambda c: c.final_score, reverse=True)

    top_results = ranked[:top_n]
    logger.info(
        "Reranked %d chunks -> top %d (best score=%.4f)",
        len(chunks),
        len(top_results),
        top_results[0].final_score if top_results else 0.0,
    )
    return top_results
