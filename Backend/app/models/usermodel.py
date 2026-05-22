"""User-related Beanie document and Pydantic models."""

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
import uuid


class UserBase(BaseModel):
    """Common fields shared across user representations."""

    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str
    is_guest: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class User(Document, UserBase):
    """MongoDB document representing an application user."""
    public_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    hashed_password: Optional[str] = None


class UserPublic(UserBase):
    """Public-facing user profile returned by the API."""
    pass



class UserCreate(BaseModel):
    """Schema for user registration requests."""

    username: str
    password: str
