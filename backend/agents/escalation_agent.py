"""
Escalation agent for the IT Helpdesk chatbot.

Detects signals that indicate a query should be escalated to a human agent,
generates a summary ticket, and returns structured escalation data.
"""

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Thresholds
REPEATED_QUESTION_THRESHOLD = 3
LOW_CONFIDENCE_THRESHOLD = 0.5

# Keywords indicating the user explicitly wants human help.
HUMAN_HELP_KEYWORDS = [
    "speak to a human",
    "talk to someone",
    "real person",
    "human agent",
    "escalate",
    "supervisor",
    "manager",
    "transfer me",
    "live agent",
    "help me please",
    "this isn't working",
    "not helpful",
]

# Sensitive operations that should always be escalated.
SENSITIVE_OPERATIONS = [
    "delete account",
    "admin access",
    "root access",
    "production server",
    "database access",
    "data breach",
    "terminated employee",
    "executive account",
    "compliance",
    "audit",
    "legal",
    "gdpr",
    "data export",
    "bulk delete",
]


@dataclass
class EscalationResult:
    """Result of the escalation check."""

    should_escalate: bool
    reason: str
    priority: str  # "low", "medium", "high", "critical"
    ticket_summary: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "should_escalate": self.should_escalate,
            "reason": self.reason,
            "priority": self.priority,
        }
        if self.ticket_summary:
            result["ticket_summary"] = self.ticket_summary
        return result


class EscalationAgent:
    """Detects when a conversation should be escalated to a human agent."""

    def check(
        self,
        query: str,
        confidence: float,
        conversation_history: Optional[list[dict[str, str]]] = None,
        category: str = "general",
    ) -> EscalationResult:
        """
        Evaluate whether the current interaction should be escalated.

        Args:
            query: The user's current message.
            confidence: Confidence score from the RAG pipeline (0.0 - 1.0).
            conversation_history: List of previous messages in the conversation.
            category: Detected category of the query.

        Returns:
            EscalationResult with escalation decision and metadata.
        """
        history = conversation_history or []

        # Check each escalation signal in priority order.
        # 1. Sensitive operations (critical priority).
        if self._is_sensitive_operation(query):
            return self._escalate(
                reason="Sensitive operation detected",
                priority="critical",
                query=query,
                category=category,
            )

        # 2. Explicit human help request (high priority).
        if self._requests_human_help(query):
            return self._escalate(
                reason="User explicitly requested human assistance",
                priority="high",
                query=query,
                category=category,
            )

        # 3. Repeated questions (medium priority).
        if self._has_repeated_questions(query, history):
            return self._escalate(
                reason=f"User has repeated similar questions {REPEATED_QUESTION_THRESHOLD}+ times",
                priority="medium",
                query=query,
                category=category,
            )

        # 4. Low confidence (medium priority).
        if confidence < LOW_CONFIDENCE_THRESHOLD:
            return self._escalate(
                reason=f"Low confidence score ({confidence:.2f} < {LOW_CONFIDENCE_THRESHOLD})",
                priority="medium",
                query=query,
                category=category,
            )

        return EscalationResult(
            should_escalate=False,
            reason="No escalation signals detected",
            priority="low",
        )

    @staticmethod
    def _is_sensitive_operation(query: str) -> bool:
        query_lower = query.lower()
        return any(op in query_lower for op in SENSITIVE_OPERATIONS)

    @staticmethod
    def _requests_human_help(query: str) -> bool:
        query_lower = query.lower()
        return any(phrase in query_lower for phrase in HUMAN_HELP_KEYWORDS)

    @staticmethod
    def _has_repeated_questions(
        query: str, history: list[dict[str, str]]
    ) -> bool:
        """Check if the user has asked similar questions repeatedly."""
        if len(history) < REPEATED_QUESTION_THRESHOLD:
            return False

        query_words = set(re.findall(r"[a-z0-9]+", query.lower()))
        if not query_words:
            return False

        similar_count = 0
        for msg in history:
            if msg.get("role") != "user":
                continue
            msg_words = set(re.findall(r"[a-z0-9]+", msg.get("content", "").lower()))
            if not msg_words:
                continue
            overlap = len(query_words & msg_words) / max(len(query_words), 1)
            if overlap > 0.6:
                similar_count += 1

        return similar_count >= REPEATED_QUESTION_THRESHOLD

    @staticmethod
    def _escalate(
        reason: str,
        priority: str,
        query: str,
        category: str,
    ) -> EscalationResult:
        """Build an escalation result with a summary ticket."""
        timestamp = datetime.now(timezone.utc).isoformat()
        ticket_summary = (
            f"--- Escalation Ticket ---\n"
            f"Timestamp: {timestamp}\n"
            f"Priority: {priority.upper()}\n"
            f"Category: {category}\n"
            f"Reason: {reason}\n"
            f"User Query: {query}\n"
            f"-------------------------"
        )

        logger.warning(
            "Escalation triggered: reason='%s', priority=%s, category=%s",
            reason,
            priority,
            category,
        )

        return EscalationResult(
            should_escalate=True,
            reason=reason,
            priority=priority,
            ticket_summary=ticket_summary,
        )
