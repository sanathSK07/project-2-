"""
IT Helpdesk AI Chatbot - FastAPI Application Entry Point.

Initializes the FastAPI app with middleware, routes, and conversation
management. Run with:
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
"""

import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from backend.api.middleware import logging_and_rate_limit_middleware, setup_cors
from backend.api.routes import router

# Load environment variables from .env file.
load_dotenv()

# Configure logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Create FastAPI application.
app = FastAPI(
    title="IT Helpdesk AI Chatbot",
    description="RAG-powered IT support chatbot with intelligent routing, "
    "escalation detection, and feedback collection.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Setup middleware.
setup_cors(app)
app.middleware("http")(logging_and_rate_limit_middleware)

# Include API routes.
app.include_router(router)


@app.on_event("startup")
async def startup_event() -> None:
    """Log application startup."""
    logger.info("IT Helpdesk AI Chatbot starting up...")
    logger.info("API documentation available at /docs")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Log application shutdown."""
    logger.info("IT Helpdesk AI Chatbot shutting down...")


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"

    logger.info("Starting server on %s:%d (reload=%s)", host, port, reload)

    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
