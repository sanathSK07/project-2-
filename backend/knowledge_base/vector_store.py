"""
ChromaDB vector store management for the IT Helpdesk knowledge base.

Provides initialization, document insertion, similarity search,
and category-filtered queries against a persistent ChromaDB collection.
"""

import logging
from pathlib import Path
from typing import Any, Optional

import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

DEFAULT_PERSIST_DIR = str(Path(__file__).resolve().parent.parent / "chroma_db")
COLLECTION_NAME = "it_helpdesk_docs"


class VectorStore:
    """Manages a ChromaDB collection for IT helpdesk documents."""

    def __init__(
        self,
        persist_directory: str = DEFAULT_PERSIST_DIR,
        collection_name: str = COLLECTION_NAME,
    ) -> None:
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self._client: Optional[chromadb.ClientAPI] = None
        self._collection: Optional[chromadb.Collection] = None

    @property
    def client(self) -> chromadb.ClientAPI:
        if self._client is None:
            logger.info("Initializing ChromaDB client at %s", self.persist_directory)
            self._client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False),
            )
        return self._client

    @property
    def collection(self) -> chromadb.Collection:
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(
                "Collection '%s' ready (%d documents)",
                self.collection_name,
                self._collection.count(),
            )
        return self._collection

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        """Add documents with pre-computed embeddings to the collection."""
        if not ids:
            logger.warning("No documents to add.")
            return

        batch_size = 500
        for start in range(0, len(ids), batch_size):
            end = start + batch_size
            self.collection.upsert(
                ids=ids[start:end],
                documents=documents[start:end],
                embeddings=embeddings[start:end],
                metadatas=metadatas[start:end],
            )
            logger.info("Upserted documents %d-%d", start, min(end, len(ids)))

        logger.info("Total documents in collection: %d", self.collection.count())

    def query(
        self,
        query_embedding: list[float],
        n_results: int = 5,
        category: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Query the collection by similarity.

        Args:
            query_embedding: The embedding vector for the query.
            n_results: Number of results to return.
            category: Optional category filter.

        Returns:
            ChromaDB query result dict with ids, documents, metadatas, distances.
        """
        where_filter = {"category": category} if category else None

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        logger.debug(
            "Query returned %d results (category=%s)",
            len(results.get("ids", [[]])[0]),
            category,
        )
        return results

    def delete_collection(self) -> None:
        """Delete the entire collection (useful for re-indexing)."""
        try:
            self.client.delete_collection(self.collection_name)
            self._collection = None
            logger.info("Deleted collection '%s'", self.collection_name)
        except Exception:
            logger.exception("Failed to delete collection '%s'", self.collection_name)

    def get_stats(self) -> dict[str, Any]:
        """Return basic statistics about the collection."""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "persist_directory": self.persist_directory,
        }
