"""
Authentication router — login and token issuance.

Provides the OAuth2-compatible ``/auth/token`` endpoint that clients
use to exchange credentials for a JWT bearer token.
"""

from app.config import settings
from app.models.usermodel import User
from app.models.securitymodel import Token
from app.utility.security import verify_password, create_access_token

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Authenticate a user and return a JWT access token.

    Accepts standard OAuth2 password-grant form data (``username`` and
    ``password``).  On success, returns a :class:`Token` with a signed
    JWT.  On failure, returns **401 Unauthorized**.

    To prevent timing-based user-enumeration attacks the password
    verifier is always invoked even when the user is not found (see
    ``DUMMY_HASH`` in :mod:`app.utility.security`).

    Args:
        form_data: OAuth2 password request containing ``username`` and
            ``password`` fields.

    Returns:
        A :class:`Token` containing the encoded JWT and token type.

    Raises:
        HTTPException: 401 if the username does not exist or the
            password is incorrect.
    """
    existing_user = await User.find_one(User.username == form_data.username)
    if existing_user and verify_password(
        form_data.password, existing_user.hashed_password
    ):
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = create_access_token(
            data={
                "sub": str(existing_user.public_id),
                "username": existing_user.username,
            },
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
