"""User management router — registration and profile retrieval."""

from app.config import settings
from app.models.usermodel import User, UserPublic, UserCreate
from app.utility.security import create_access_token, get_password_hash
from app.utility.dependencies import verify_user_access_token

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user(user: UserCreate) -> JSONResponse:
    """Register a new user account and return an access token."""
    existing_user = await User.find_one(User.username == user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password=user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        is_guest=False,
    )
    await new_user.insert()

    access_token = create_access_token(
        data={
            "sub": str(new_user.public_id),
            "username": new_user.username,
            "is_guest": False,
        },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return response


@router.get("/me", response_model=UserPublic)
async def get_user(
    user: Annotated[User, Depends(verify_user_access_token)],
) -> UserPublic:
    """Return the profile of the currently authenticated user."""
    return user
