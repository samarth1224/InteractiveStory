"""User management router — profile retrieval."""

from app.models.usermodel import User, UserPublic
from app.utility.dependencies import verify_user_access_token

from fastapi import APIRouter, Depends
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserPublic)
async def get_user(
    user: Annotated[User, Depends(verify_user_access_token)],
) -> UserPublic:
    """Return the profile of the currently authenticated user."""
    return user

