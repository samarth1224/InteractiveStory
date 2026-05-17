"""
Authentication router — login, guest access, token issuance, and logout.

Provides the OAuth2-compatible ``/auth/token`` endpoint that clients
use to exchange credentials for a JWT bearer token, as well as
``/auth/guest`` for anonymous guest sessions and ``/auth/logout`` to
clear the token cookie.

All token endpoints set the JWT in an HTTP-only cookie (``access_token``)
in addition to returning it in the response body for backwards
compatibility.
"""

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
    """Create a JSONResponse that sets the ``access_token`` cookie.

    The cookie is configured as:
    - **httponly**: prevents client-side JS access.
    - **samesite=lax**: CSRF-safe while allowing top-level navigations.
    - **secure=False**: set to ``True`` in production behind HTTPS.

    Args:
        access_token: The encoded JWT string.

    Returns:
        A :class:`JSONResponse` with the token in the body *and* as an
        HTTP-only cookie.
    """
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
    """Authenticate a user and return a JWT access token.

    Accepts standard OAuth2 password-grant form data (``username`` and
    ``password``).  On success, returns a :class:`Token` with a signed
    JWT set both in the response body and as an HTTP-only cookie.
    On failure, returns **401 Unauthorized**.

    To prevent timing-based user-enumeration attacks the password
    verifier is always invoked even when the user is not found (see
    ``DUMMY_HASH`` in :mod:`app.utility.security`).

    Args:
        form_data: OAuth2 password request containing ``username`` and
            ``password`` fields.

    Returns:
        A :class:`JSONResponse` containing the encoded JWT and token type,
        with the token also set as an HTTP-only cookie.

    Raises:
        HTTPException: 401 if the username does not exist or the
            password is incorrect.
    """
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
    """Create a temporary guest account and return a JWT access token.

    Generates a new :class:`User` with ``is_guest=True`` and a
    ``guest_<uuid>`` username.  The guest user has no password, but
    receives a fully functional JWT that grants access to protected
    endpoints.

    Returns:
        A :class:`JSONResponse` containing the encoded JWT and token type,
        with the token also set as an HTTP-only cookie.
    """
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
    """Clear the ``access_token`` cookie, effectively logging the user out.

    Returns:
        A :class:`JSONResponse` confirming the logout.
    """
    response = JSONResponse(content={"message": "Successfully logged out"})
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False,  # Match the flags used when setting the cookie
        path="/",
    )
    return response
