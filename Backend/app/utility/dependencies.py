"""FastAPI dependency functions for request-level authorization."""

from app import config
from app.models.securitymodel import TokenData
from app.models.usermodel import User
from app.utility.security import extract_token_from_request

from fastapi import HTTPException, Request, status

import jwt
from jwt.exceptions import InvalidTokenError


async def verify_user_access_token(request: Request) -> User:
    """Validate a JWT token and return the corresponding user."""
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
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
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
