"""Interactive Story API entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from dotenv import load_dotenv

load_dotenv(override=True)
from app.routers import story, user, auth
from app.models import storymodel, usermodel

from beanie import init_beanie
from pymongo import AsyncMongoClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup (MongoDB/Beanie init) and shutdown."""
    client = AsyncMongoClient(os.getenv("MONGODB_URL"))
    await init_beanie(
        database=client[os.getenv("MONGODB_DB_NAME", "interactive_story")],
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
import json

def _get_cors_origins():
    val = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:3000")
    if val.strip().startswith("["):
        try:
            return json.loads(val)
        except Exception:
            pass
    return val.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(),
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
    """Root health-check endpoint."""
    return {"status": "healthy", "message": "Interactive Story API is running"}


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Detailed health-check endpoint."""
    return {
        "status": "healthy",
        "service": "Interactive Story API",
        "version": "1.0.0",
    }
