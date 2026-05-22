"""Authentication router — login, guest access, token issuance, and logout."""

from app.config import settings
from app.models.usermodel import User
from app.utility.security import verify_password, create_access_token

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from datetime import timedelta
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])


def _build_token_response(access_token: str) -> JSONResponse:
    """Create a JSONResponse that sets the ``access_token`` cookie."""
    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,  # Set to True in production with HTTPS
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    return response


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> JSONResponse:
    """Authenticate a user and return a JWT access token."""
    existing_user = await User.find_one(User.username == form_data.username)
    if existing_user and existing_user.hashed_password and verify_password(
        form_data.password, existing_user.hashed_password
    ):
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={
                "sub": str(existing_user.public_id),
                "username": existing_user.username,
                "is_guest": existing_user.is_guest,
            },
            expires_delta=access_token_expires,
        )
        return _build_token_response(access_token)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/guest")
async def login_as_guest() -> JSONResponse:
    """Create a temporary guest account and return a JWT access token."""
    guest_id = uuid.uuid4()
    guest_username = f"guest_{guest_id.hex[:12]}"

    guest_user = User(
        public_id=guest_id,
        username=guest_username,
        is_guest=True,
        hashed_password=None,
    )
    await guest_user.insert()

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={
            "sub": str(guest_user.public_id),
            "username": guest_user.username,
            "is_guest": True,
        },
        expires_delta=access_token_expires,
    )
    return _build_token_response(access_token)


@router.post("/logout")
async def logout() -> JSONResponse:
    """Clear the ``access_token`` cookie, effectively logging the user out."""
    response = JSONResponse(content={"message": "Successfully logged out"})
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False,  # Match the flags used when setting the cookie
        path="/",
    )
    return response
