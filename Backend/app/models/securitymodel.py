"""Security-related Pydantic models for JWT token handling."""

from pydantic import BaseModel, Field
import uuid


class Token(BaseModel):
    """Schema returned to clients after successful authentication."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Internal representation of the claims extracted from a JWT."""

    username: str | None = None
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    is_guest: bool = False