"""
Core security utilities for password hashing and JWT management.

This module provides:
- Password hashing and verification via Argon2 (``pwdlib``).
- JWT access-token creation and encoding.
- A shared ``oauth2_scheme`` instance used by FastAPI dependency
  injection across all routers.

All cryptographic parameters (secret key, algorithm, expiry) are read
from :pydata:`app.config.settings` which in turn loads them from
environment variables.
"""

from app.config import settings

from fastapi.security import OAuth2PasswordBearer

import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash


# ---------------------------------------------------------------------------
# OAuth2 scheme — single source of truth, imported by dependencies.py
# ---------------------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# ---------------------------------------------------------------------------
# Password hashing (Argon2)
# ---------------------------------------------------------------------------
password_hash = PasswordHash.recommended()

# Pre-computed dummy hash used to prevent timing-based user-enumeration
# attacks.  When a login attempt references a non-existent user we still
# run the hash verifier against this value so the response time is
# indistinguishable from a real verification.
DUMMY_HASH = password_hash.hash("dummypassword")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored Argon2 hash.

    Args:
        plain_password: The password supplied by the user.
        hashed_password: The Argon2 hash stored in the database.

    Returns:
        ``True`` if the password matches, ``False`` otherwise.
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain-text password using Argon2.

    Args:
        password: The plain-text password to hash.

    Returns:
        The Argon2-encoded hash string suitable for database storage.
    """
    return password_hash.hash(password)


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate a signed JWT access token.

    The token payload is a shallow copy of *data* with an ``exp`` claim
    appended.  If *expires_delta* is not provided the default expiry
    from ``settings.ACCESS_TOKEN_EXPIRE_MINUTES`` is used.

    Args:
        data: Arbitrary claims to include in the token payload (e.g.
            ``{"sub": public_id, "username": name}``).
        expires_delta: Optional custom lifetime.  Defaults to the
            value configured in environment variables.

    Returns:
        The encoded JWT string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt
