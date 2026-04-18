"""
User management router — registration and profile retrieval.

Provides endpoints for creating new user accounts and querying the
authenticated user's profile.
"""

from app.config import settings
from app.models.usermodel import User, UserPublic, UserCreate
from app.models.securitymodel import Token
from app.utility.security import create_access_token, get_password_hash
from app.utility.dependencies import verify_user_access_token

from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=Token)
async def create_user(user: UserCreate) -> Token:
    """Register a new user account and return an access token.

    Checks that the requested username is not already taken, hashes the
    password, persists the new :class:`User` document, and immediately
    returns a signed JWT so the client can authenticate subsequent
    requests without a separate login step.

    Args:
        user: Registration payload containing ``username`` and
            ``password``.

    Returns:
        A :class:`Token` with the encoded JWT and token type.

    Raises:
        HTTPException: 400 if the username is already registered.
    """
    existing_user = await User.find_one(User.username == user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password=user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
    )
    await new_user.insert()
    access_token = create_access_token(
        data={"sub": str(new_user.public_id), "username": new_user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPublic)
async def get_user(
    user: Annotated[User, Depends(verify_user_access_token)],
) -> UserPublic:
    """Return the profile of the currently authenticated user.

    Requires a valid JWT bearer token. The token is validated by the
    :func:`~app.utility.dependencies.verify_user_access_token`
    dependency which resolves the :class:`User` document.

    Args:
        user: The authenticated user, injected by FastAPI's dependency
            system.

    Returns:
        The user's public profile (excludes ``hashed_password``).
    """
    return user
