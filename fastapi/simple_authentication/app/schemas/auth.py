from pydantic import BaseModel, Field, EmailStr, UUID4
from typing import Optional


class UserLogin(BaseModel):
    username_or_email: str = Field(..., description="Username or Email")
    password: str = Field(..., min_length=8, max_length=18)


class TokenPayload(BaseModel):
    sub: UUID4
    exp: int
    iat: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
