"""Core security utilities for password hashing and JWT management."""

from app import config

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

# pyrefly: ignore [missing-import]
import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash


# ---------------------------------------------------------------------------
# OAuth2 scheme — used as a fallback; primary extraction is from cookies.
# The ``auto_error=False`` flag prevents 401 when no Authorization header
# is present so the cookie path can be tried instead.
# ---------------------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

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
    """Verify a plain-text password against a stored Argon2 hash."""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain-text password using Argon2."""
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
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return encoded_jwt


# ---------------------------------------------------------------------------
# Cookie-first token extraction
# ---------------------------------------------------------------------------
def extract_token_from_request(request: Request) -> str | None:
    """Extract the JWT token from the request cookie."""
    #HTTP-only cookie
    token = request.cookies.get("access_token")
    if token:
        return token

    return None
