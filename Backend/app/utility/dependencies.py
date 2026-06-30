"""FastAPI dependency functions for request-level authorization."""

import os
from app.models.securitymodel import TokenData
from app.models.usermodel import User
from app.utility.security import extract_token_from_request, oauth2_scheme

from fastapi import Depends, HTTPException, Request, status

import jwt
from jwt.exceptions import InvalidTokenError

from typing import Annotated


async def verify_user_access_token(
    request: Request,
    bearer_token: Annotated[str | None, Depends(oauth2_scheme)] = None,
) -> User:
    """Validate a JWT token and return the corresponding user.

    The ``bearer_token`` parameter is populated by FastAPI's
    ``OAuth2PasswordBearer`` dependency when an ``Authorization: Bearer``
    header is present.  Including it here also ensures that FastAPI
    auto-generates the correct ``oauth2`` security scheme in the
    OpenAPI specification — no custom class needed.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = extract_token_from_request(request, bearer_token)
    if token is None:
        raise credentials_exception

    

    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production-abc123xyz789"),
            algorithms=[os.getenv("JWT_ALGORITHM", "HS256")],
        )
        public_id = payload.get("sub")
        username = payload.get("username")
        is_guest = payload.get("is_guest", False)
        if public_id is None:
            raise credentials_exception
        token_data = TokenData(
            public_id=public_id,
            username=username,
            is_guest=is_guest,
        )
    except InvalidTokenError:
        raise credentials_exception

    user = await User.find_one(User.public_id == token_data.public_id)
    if user is None:
        raise credentials_exception
    return user



