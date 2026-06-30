"""Core security utilities for password hashing and JWT management."""

import os

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

# pyrefly: ignore [missing-import]
import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

# Password hashing
password_hash = PasswordHash.recommended()

# Pre-computed dummy hash used to prevent timing-based user-enumeration
# attacks.  When a login attempt references a non-existent user we still
# run the hash verifier against this value so the response time is
# indistinguishable from a real verification.
DUMMY_HASH = password_hash.hash("dummypassword")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored Argon2 hash."""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain-text password """
    return password_hash.hash(password)


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate a signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production-abc123xyz789"),
        algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    )
    return encoded_jwt


# ---------------------------------------------------------------------------
# Cookie-first token extraction
# ---------------------------------------------------------------------------
def extract_token_from_request(
    request: Request,
    bearer_token: str | None = None,
) -> str | None:
    """Extract the JWT token from the request.
    Resolution order:
      1. ``Authorization: Bearer <token>`` header (provided by FastAPI's
         ``OAuth2PasswordBearer`` dependency via *bearer_token*).
      2. ``access_token`` HTTP-only cookie (frontend flow).
    This dual strategy means:
      - Swagger UI / Specmatic / any standard client can use the header.
      - The browser frontend continues to work via cookies.
    """
    # 1. Header (OAuth2 Bearer)
    if bearer_token:
        return bearer_token
    # 2. Cookie fallback
    token = request.cookies.get("access_token")
    if token:
        return token

    return None
