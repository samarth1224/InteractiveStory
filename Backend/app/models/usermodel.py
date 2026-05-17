"""
User-related Beanie document and Pydantic models.

Defines the ``User`` document stored in MongoDB and companion schemas
for public responses and user registration requests.
"""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
import uuid


class UserBase(BaseModel):
    """Common fields shared across user representations.

    Attributes:
        public_id: Externally-visible UUID for the user.
        username: Unique username chosen during registration.
        is_guest: Whether this account is a temporary guest session.
        created_at: Timestamp when the account was created (UTC).
    """

    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str
    is_guest: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class User(Document, UserBase):
    """MongoDB document representing an application user.

    Extends :class:`UserBase` with the password hash that is never
    exposed through public API responses.  Guest users have no password,
    so ``hashed_password`` is ``None`` for them.

    Attributes:
        hashed_password: Argon2-hashed password string, or ``None`` for
            guest accounts.
    """

    hashed_password: Optional[str] = None


class UserPublic(UserBase):
    """Public-facing user profile returned by the API.

    Identical to :class:`UserBase` — excludes ``hashed_password``.
    """

    pass


class UserCreate(BaseModel):
    """Schema for user registration requests.

    Attributes:
        username: Desired username.
        password: Plain-text password (will be hashed before storage).
    """

    username: str
    password: str
