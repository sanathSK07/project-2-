"""
FastAPI middleware for the IT Helpdesk API.

Provides request logging, rate limiting, and CORS configuration.
"""

import logging
import time
from collections import defaultdict
from typing import Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# Rate limiting: max requests per window per IP.
RATE_LIMIT_MAX_REQUESTS = 10
RATE_LIMIT_WINDOW_SECONDS = 60

# In-memory rate limit tracker: {ip: [timestamp, ...]}
_rate_limit_store: dict[str, list[float]] = defaultdict(list)

# CORS allowed origins (adjust for production).
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]


def setup_cors(app: FastAPI) -> None:
    """Add CORS middleware to the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _get_client_ip(request: Request) -> str:
    """Extract client IP from the request, respecting X-Forwarded-For."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _is_rate_limited(client_ip: str) -> bool:
    """Check whether the client IP has exceeded the rate limit."""
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    # Prune old entries.
    _rate_limit_store[client_ip] = [
        ts for ts in _rate_limit_store[client_ip] if ts > window_start
    ]

    if len(_rate_limit_store[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        return True

    _rate_limit_store[client_ip].append(now)
    return False


async def logging_and_rate_limit_middleware(
    request: Request, call_next: Callable
) -> Response:
    """
    Combined middleware for request logging and rate limiting.

    Logs: timestamp, method, endpoint, response time, status code.
    Rate limits: 10 requests per minute per client IP.
    """
    client_ip = _get_client_ip(request)
    start_time = time.time()

    # Skip rate limiting for health checks.
    if request.url.path == "/health":
        response = await call_next(request)
        return response

    # Rate limit check.
    if _is_rate_limited(client_ip):
        elapsed = time.time() - start_time
        logger.warning(
            "Rate limited: ip=%s method=%s path=%s elapsed=%.3fs",
            client_ip,
            request.method,
            request.url.path,
            elapsed,
        )
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": "Rate limit exceeded. Maximum 10 requests per minute.",
            },
        )

    # Process request.
    response = await call_next(request)
    elapsed = time.time() - start_time

    logger.info(
        "Request: ip=%s method=%s path=%s status=%d elapsed=%.3fs",
        client_ip,
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )

    response.headers["X-Response-Time"] = f"{elapsed:.3f}s"
    return response
