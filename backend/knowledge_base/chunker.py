"""
Document chunker for IT Helpdesk knowledge base.

Loads markdown files from the documents/ directory and splits them into
manageable chunks with preserved metadata for downstream embedding and retrieval.
"""

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

DOCUMENTS_DIR = Path(__file__).resolve().parent / "documents"

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "password": ["password", "reset", "credential", "login", "authentication", "mfa", "2fa"],
    "vpn": ["vpn", "remote", "tunnel", "wireguard", "openvpn"],
    "wifi": ["wifi", "wireless", "network", "ssid", "wpa"],
    "email": ["email", "outlook", "mail", "smtp", "imap", "calendar"],
    "software": ["software", "install", "update", "application", "app", "license"],
    "printer": ["printer", "print", "scanner", "scan", "fax"],
    "security": ["security", "virus", "malware", "phishing", "firewall", "encryption"],
    "hardware": ["hardware", "laptop", "monitor", "keyboard", "mouse", "dock"],
    "onboarding": ["onboarding", "new hire", "setup", "account creation", "welcome"],
    "cloud": ["cloud", "aws", "azure", "gcp", "saas", "office 365", "google workspace"],
}


@dataclass
class DocumentChunk:
    """Represents a single chunk of a document with metadata."""

    text: str
    source_doc: str
    category: str
    chunk_index: int
    title: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "source_doc": self.source_doc,
            "category": self.category,
            "chunk_index": self.chunk_index,
            "title": self.title,
            **self.metadata,
        }


def derive_category(filename: str, content: str = "") -> str:
    """Derive the document category from filename and content."""
    name_lower = filename.lower()
    content_lower = content.lower() if content else ""

    best_category = "general"
    best_score = 0

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in name_lower:
                score += 3
            if keyword in content_lower[:500]:
                score += 1
        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def extract_title(content: str, filename: str) -> str:
    """Extract title from markdown content or fall back to filename."""
    lines = content.strip().split("\n")
    for line in lines:
        match = re.match(r"^#\s+(.+)$", line.strip())
        if match:
            return match.group(1).strip()
    return Path(filename).stem.replace("_", " ").replace("-", " ").title()


def load_markdown_files(documents_dir: Optional[Path] = None) -> list[dict]:
    """
    Load all markdown files from the documents directory.

    Returns a list of dicts with keys: content, filename, category, title.
    """
    docs_path = documents_dir or DOCUMENTS_DIR

    if not docs_path.exists():
        logger.warning("Documents directory does not exist: %s", docs_path)
        return []

    documents = []
    for filepath in sorted(docs_path.glob("*.md")):
        try:
            content = filepath.read_text(encoding="utf-8")
            if not content.strip():
                logger.warning("Skipping empty file: %s", filepath.name)
                continue

            category = derive_category(filepath.name, content)
            title = extract_title(content, filepath.name)

            documents.append({
                "content": content,
                "filename": filepath.name,
                "category": category,
                "title": title,
            })
            logger.info("Loaded document: %s (category=%s)", filepath.name, category)
        except Exception:
            logger.exception("Failed to load file: %s", filepath.name)

    logger.info("Loaded %d documents from %s", len(documents), docs_path)
    return documents


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[DocumentChunk]:
    """
    Split documents into chunks using RecursiveCharacterTextSplitter.

    Args:
        documents: List of document dicts from load_markdown_files().
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Character overlap between consecutive chunks.

    Returns:
        List of DocumentChunk objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )

    all_chunks: list[DocumentChunk] = []

    for doc in documents:
        texts = splitter.split_text(doc["content"])
        for idx, text in enumerate(texts):
            chunk = DocumentChunk(
                text=text.strip(),
                source_doc=doc["filename"],
                category=doc["category"],
                chunk_index=idx,
                title=doc["title"],
            )
            all_chunks.append(chunk)

        logger.debug(
            "Chunked '%s' into %d pieces", doc["filename"], len(texts)
        )

    logger.info("Created %d total chunks from %d documents", len(all_chunks), len(documents))
    return all_chunks


def load_and_chunk(
    documents_dir: Optional[Path] = None,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[DocumentChunk]:
    """Convenience function: load markdown files and chunk them in one call."""
    documents = load_markdown_files(documents_dir)
    return chunk_documents(documents, chunk_size, chunk_overlap)
