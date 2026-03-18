"""
Router agent for the IT Helpdesk chatbot.

Classifies incoming queries into IT support categories using a two-stage
approach: fast keyword matching first, with LLM fallback for ambiguous cases.
"""

import logging
import os
import re
from typing import Optional

import anthropic
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

CATEGORIES = [
    "password",
    "vpn",
    "wifi",
    "email",
    "software",
    "printer",
    "security",
    "hardware",
    "onboarding",
    "cloud",
    "general",
]

KEYWORD_MAP: dict[str, list[str]] = {
    "password": [
        "password", "reset password", "forgot password", "login", "sign in",
        "locked out", "credential", "mfa", "two-factor", "2fa", "authentication",
        "sso", "single sign-on",
    ],
    "vpn": [
        "vpn", "remote access", "tunnel", "wireguard", "openvpn", "cisco anyconnect",
        "connect remotely", "work from home",
    ],
    "wifi": [
        "wifi", "wi-fi", "wireless", "network", "ssid", "internet",
        "connected but no internet", "can't connect to wifi",
    ],
    "email": [
        "email", "outlook", "mail", "inbox", "smtp", "imap",
        "calendar invite", "teams", "exchange", "signature",
    ],
    "software": [
        "install", "software", "application", "app", "update", "upgrade",
        "license", "download", "uninstall", "microsoft office", "adobe",
    ],
    "printer": [
        "printer", "print", "printing", "scanner", "scan", "fax",
        "paper jam", "toner", "cartridge",
    ],
    "security": [
        "security", "phishing", "malware", "virus", "suspicious",
        "breach", "encryption", "firewall", "ransomware", "spam",
        "compromised", "hacked",
    ],
    "hardware": [
        "hardware", "laptop", "computer", "monitor", "keyboard", "mouse",
        "docking station", "dock", "headset", "webcam", "screen",
        "battery", "charger", "broken",
    ],
    "onboarding": [
        "new hire", "onboarding", "new employee", "first day", "account setup",
        "welcome", "orientation", "new joiner",
    ],
    "cloud": [
        "cloud", "aws", "azure", "gcp", "google workspace", "office 365",
        "sharepoint", "onedrive", "google drive", "dropbox", "saas",
    ],
}


def _keyword_classify(query: str) -> Optional[str]:
    """
    Classify query using keyword matching. Returns category or None if ambiguous.
    """
    query_lower = query.lower()
    scores: dict[str, int] = {}

    for category, keywords in KEYWORD_MAP.items():
        score = 0
        for keyword in keywords:
            if keyword in query_lower:
                # Longer keyword matches are more specific.
                score += len(keyword.split())
        if score > 0:
            scores[category] = score

    if not scores:
        return None

    sorted_cats = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Return the top category only if it clearly wins.
    if len(sorted_cats) == 1:
        return sorted_cats[0][0]
    if sorted_cats[0][1] > sorted_cats[1][1]:
        return sorted_cats[0][0]

    # Ambiguous -- fall back to LLM.
    return None


def _llm_classify(query: str) -> str:
    """
    Use Claude to classify a query when keyword matching is ambiguous.
    Falls back to 'general' on any failure.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.warning("No ANTHROPIC_API_KEY set; defaulting to 'general'.")
        return "general"

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=50,
            temperature=0.0,
            system=(
                "You are a classifier. Classify the following IT support query into "
                f"exactly one category from this list: {', '.join(CATEGORIES)}. "
                "Respond with only the category name, nothing else."
            ),
            messages=[{"role": "user", "content": query}],
        )
        category = response.content[0].text.strip().lower()
        # Validate against known categories.
        if category in CATEGORIES:
            return category
        # Try partial match.
        for cat in CATEGORIES:
            if cat in category:
                return cat
        logger.warning("LLM returned unknown category '%s'; defaulting to general.", category)
        return "general"

    except Exception:
        logger.exception("LLM classification failed; defaulting to 'general'")
        return "general"


class RouterAgent:
    """Routes user queries to the appropriate IT support category."""

    def classify(self, query: str) -> str:
        """
        Classify a query into an IT support category.

        Uses fast keyword matching first, then falls back to LLM classification
        if the result is ambiguous.

        Args:
            query: The user's question.

        Returns:
            One of the CATEGORIES strings.
        """
        category = _keyword_classify(query)
        if category:
            logger.info("Keyword-classified query as '%s': %.80s", category, query)
            return category

        logger.info("Keyword match ambiguous; using LLM classification for: %.80s", query)
        category = _llm_classify(query)
        logger.info("LLM-classified query as '%s': %.80s", category, query)
        return category
