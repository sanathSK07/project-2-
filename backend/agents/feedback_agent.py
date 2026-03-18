"""
Feedback agent for the IT Helpdesk chatbot.

Collects user feedback (helpful / not helpful) on responses and persists
it to a JSON log file for analytics and model improvement.
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

FEEDBACK_FILE = Path(__file__).resolve().parent.parent / "data" / "feedback_log.json"


class FeedbackAgent:
    """Records and retrieves user feedback on chatbot responses."""

    def __init__(self, feedback_file: Optional[Path] = None) -> None:
        self._feedback_file = feedback_file or FEEDBACK_FILE
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the feedback file and parent directories if needed."""
        self._feedback_file.parent.mkdir(parents=True, exist_ok=True)
        if not self._feedback_file.exists():
            self._feedback_file.write_text("[]", encoding="utf-8")

    def _load_entries(self) -> list[dict[str, Any]]:
        """Load all feedback entries from disk."""
        try:
            content = self._feedback_file.read_text(encoding="utf-8").strip()
            if not content:
                return []
            data = json.loads(content)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            logger.exception("Failed to load feedback file")
            return []

    def _save_entries(self, entries: list[dict[str, Any]]) -> None:
        """Persist feedback entries to disk."""
        try:
            self._feedback_file.write_text(
                json.dumps(entries, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError:
            logger.exception("Failed to save feedback file")

    def record_feedback(
        self,
        conversation_id: str,
        message_id: str,
        query: str,
        response: str,
        rating: str,
        category: str = "general",
        feedback_text: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Record a feedback entry.

        Args:
            conversation_id: UUID of the conversation.
            message_id: UUID of the specific message.
            query: The original user query.
            response: The chatbot's response.
            rating: 'helpful' or 'not_helpful'.
            category: The query category.
            feedback_text: Optional free-text feedback from the user.

        Returns:
            The recorded feedback entry.
        """
        entry = {
            "conversation_id": conversation_id,
            "message_id": message_id,
            "query": query,
            "response": response,
            "rating": rating,
            "feedback_text": feedback_text or "",
            "category": category,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        entries = self._load_entries()
        entries.append(entry)
        self._save_entries(entries)

        logger.info(
            "Recorded feedback: conversation=%s, rating=%s, category=%s",
            conversation_id,
            rating,
            category,
        )
        return entry

    def get_analytics(self) -> dict[str, Any]:
        """
        Compute analytics from collected feedback.

        Returns:
            Dict with total_feedback, helpful_count, not_helpful_count,
            satisfaction_rate, and per-category breakdown.
        """
        entries = self._load_entries()

        total = len(entries)
        helpful = sum(1 for e in entries if e.get("rating") == "helpful")
        not_helpful = sum(1 for e in entries if e.get("rating") == "not_helpful")

        category_stats: dict[str, dict[str, int]] = {}
        for entry in entries:
            cat = entry.get("category", "general")
            if cat not in category_stats:
                category_stats[cat] = {"helpful": 0, "not_helpful": 0, "total": 0}
            category_stats[cat]["total"] += 1
            if entry.get("rating") == "helpful":
                category_stats[cat]["helpful"] += 1
            elif entry.get("rating") == "not_helpful":
                category_stats[cat]["not_helpful"] += 1

        return {
            "total_feedback": total,
            "helpful_count": helpful,
            "not_helpful_count": not_helpful,
            "satisfaction_rate": round(helpful / total, 4) if total > 0 else 0.0,
            "by_category": category_stats,
        }
