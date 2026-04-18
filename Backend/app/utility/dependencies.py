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
from app.utility.security import oauth2_scheme

from fastapi import HTTPException, Depends, status
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError


async def verify_user_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """Validate a JWT bearer token and return the corresponding user.

    This function is designed to be used as a FastAPI dependency via
    ``Depends(verify_user_access_token)``.  It:

    1. Decodes and validates the JWT token.
    2. Extracts the ``sub`` (public_id) and ``username`` claims.
    3. Looks up the :class:`~app.models.usermodel.User` document in
       MongoDB.
    4. Returns the user or raises **401 Unauthorized**.

    Args:
        token: The raw JWT string extracted from the ``Authorization:
            Bearer <token>`` header by the ``oauth2_scheme``.

    Returns:
        The authenticated :class:`~app.models.usermodel.User` document.

    Raises:
        HTTPException: 401 if the token is invalid, expired, or the
            user no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        public_id = payload.get("sub")
        username = payload.get("username")
        if public_id is None:
            raise credentials_exception
        token_data = TokenData(public_id=public_id, username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = await User.find_one(User.public_id == token_data.public_id)
    if user is None:
        raise credentials_exception
    return user
