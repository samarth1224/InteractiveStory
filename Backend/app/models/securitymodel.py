"""
Security-related Pydantic models for JWT token handling.

These models are used as request/response schemas for authentication
endpoints and for internal token data validation.
"""

from pydantic import BaseModel, Field
import uuid


class Token(BaseModel):
    """Schema returned to clients after successful authentication.

    Attributes:
        access_token: The encoded JWT access token string.
        token_type: The token scheme, typically ``"bearer"``.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Internal representation of the claims extracted from a JWT.

    Used during token verification to carry validated identity
    information before looking up the full ``User`` document.

    Attributes:
        username: The username claim from the token payload.
        public_id: The user's public UUID extracted from the ``sub`` claim.
    """

    username: str | None = None
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)