"""
Interactive Story API — application entry point.

Creates the FastAPI application instance, configures CORS middleware,
registers all routers, and handles the MongoDB/Beanie lifecycle.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import story, user, auth
from app.models import storymodel, usermodel

from beanie import init_beanie
from pymongo import AsyncMongoClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events.

    On startup, establishes an async MongoDB connection and initialises
    Beanie with the registered document models.  The connection is kept
    alive for the duration of the application and cleaned up on
    shutdown.

    Args:
        app: The FastAPI application instance (provided by the
            framework).

    Yields:
        Control back to the framework while the application is running.
    """
    client = AsyncMongoClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[storymodel.Story, usermodel.User],
    )
    yield


app = FastAPI(
    title="Interactive Story API",
    description="API for creating and playing AI-generated interactive stories",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(story.router)


@app.get("/", tags=["Health"])
def read_root() -> dict:
    """Root health-check endpoint.

    Returns a minimal JSON payload confirming the API is reachable.

    Returns:
        A dict with ``status`` and ``message`` keys.
    """
    return {"status": "healthy", "message": "Interactive Story API is running"}


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Detailed health-check endpoint.

    Returns service metadata useful for monitoring dashboards and
    container orchestrators.

    Returns:
        A dict with ``status``, ``service``, and ``version`` keys.
    """
    return {
        "status": "healthy",
        "service": "Interactive Story API",
        "version": "1.0.0",
    }
