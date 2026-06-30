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


    # // {
# //   "http-request": {
# //     "method": "POST",
# //     "path": "/auth/token",
# //     "headers": {
# //       "Content-Type": "application/x-www-form-urlencoded"
# //     },
# //     "form-fields": {
# //       "username": "test_user",
# //       "password": "SecureP@ssw0rd!",
# //       "grant_type": "password",
# //       "scope": "",
# //       "client_id": "",
# //       "client_secret": ""
# //     }
# //   },
# //   "http-response": {
# //     "status": 200,
# //     "body": {
# //       "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
# //       "token_type": "bearer"
# //     }
# //   }
# // }