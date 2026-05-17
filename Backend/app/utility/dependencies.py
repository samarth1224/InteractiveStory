"""
FastAPI dependency functions for request-level authorization.

This module houses reusable ``Depends()``-compatible callables.  Other
modules should import from here when they need to declare authenticated
endpoints, e.g.::

    from app.utility.dependencies import verify_user_access_token

    @router.get("/protected")
    async def protected(user: Annotated[User, Depends(verify_user_access_token)]):
        ...
"""

from app.config import settings
from app.models.securitymodel import TokenData
from app.models.usermodel import User
from app.utility.security import extract_token_from_request

from fastapi import HTTPException, Request, status

import jwt
from jwt.exceptions import InvalidTokenError


async def verify_user_access_token(request: Request) -> User:
    """Validate a JWT token and return the corresponding user.

    Supports both registered and guest users.  The token is first
    extracted from the ``access_token`` HTTP-only cookie; if absent,
    the ``Authorization: Bearer`` header is checked as a fallback.

    This function is designed to be used as a FastAPI dependency via
    ``Depends(verify_user_access_token)``.  It:

    1. Extracts the JWT from the cookie or header.
    2. Decodes and validates the JWT token.
    3. Extracts the ``sub`` (public_id), ``username``, and ``is_guest``
       claims.
    4. Looks up the :class:`~app.models.usermodel.User` document in
       MongoDB.
    5. Returns the user or raises **401 Unauthorized**.

    Args:
        request: The incoming :class:`~fastapi.Request` (injected
            automatically by FastAPI).

    Returns:
        The authenticated :class:`~app.models.usermodel.User` document.

    Raises:
        HTTPException: 401 if no token is present, the token is invalid
            or expired, or the user no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = extract_token_from_request(request)
    if token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
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
