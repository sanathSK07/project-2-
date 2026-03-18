"""
Embedding pipeline for the IT Helpdesk knowledge base.

Uses sentence-transformers/all-MiniLM-L6-v2 to encode document chunks
and stores them in a ChromaDB persistent collection.

Run as:
    python -m backend.knowledge_base.embedder
"""

import logging
import sys
from typing import Optional

from sentence_transformers import SentenceTransformer

from backend.knowledge_base.chunker import DocumentChunk, load_and_chunk
from backend.knowledge_base.vector_store import VectorStore

logger = logging.getLogger(__name__)

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class Embedder:
    """Generates embeddings and stores them in the vector store."""

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        logger.info("Loading embedding model: %s", model_name)
        self._model = SentenceTransformer(model_name)
        self._vector_store = VectorStore()

    @property
    def vector_store(self) -> VectorStore:
        return self._vector_store

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of text strings."""
        embeddings = self._model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """Generate an embedding for a single query string."""
        embedding = self._model.encode(query, convert_to_numpy=True)
        return embedding.tolist()

    def index_chunks(self, chunks: list[DocumentChunk]) -> int:
        """
        Embed and store document chunks in ChromaDB.

        Returns the number of chunks indexed.
        """
        if not chunks:
            logger.warning("No chunks to index.")
            return 0

        texts = [chunk.text for chunk in chunks]
        embeddings = self.embed_texts(texts)

        ids = [
            f"{chunk.source_doc}::chunk_{chunk.chunk_index}"
            for chunk in chunks
        ]
        metadatas = [
            {
                "source_doc": chunk.source_doc,
                "category": chunk.category,
                "chunk_index": chunk.chunk_index,
                "title": chunk.title,
            }
            for chunk in chunks
        ]

        self._vector_store.add_documents(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info("Indexed %d chunks", len(chunks))
        return len(chunks)

    def reindex(self) -> int:
        """Delete existing collection and rebuild from documents/."""
        logger.info("Starting full re-index...")
        self._vector_store.delete_collection()
        chunks = load_and_chunk()
        count = self.index_chunks(chunks)
        logger.info("Re-index complete: %d chunks indexed", count)
        return count


def build_index(documents_dir: Optional[str] = None) -> int:
    """Load, chunk, embed, and store all documents. Returns chunk count."""
    from pathlib import Path

    dir_path = Path(documents_dir) if documents_dir else None
    chunks = load_and_chunk(documents_dir=dir_path)
    embedder = Embedder()
    return embedder.index_chunks(chunks)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger.info("Starting knowledge base indexing pipeline...")
    try:
        count = build_index()
        logger.info("Indexing complete. Total chunks: %d", count)
    except Exception:
        logger.exception("Indexing failed")
        sys.exit(1)
