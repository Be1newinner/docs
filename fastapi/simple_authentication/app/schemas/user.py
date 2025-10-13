from pydantic import BaseModel, EmailStr, Field, ConfigDict, UUID4
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    fullname: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    gender: str | None = Field(None, max_length=10)
    contact: str | None = Field(None, min_length=10, max_length=13)
    password: str = Field(min_length=8, max_length=18)


class UserUpdate(BaseModel):
    fullname: Optional[str] = Field(None, min_length=3, max_length=100)
    username: Optional[str] = Field(min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    gender: Optional[str] = Field(None, max_length=10)
    contact: Optional[str] = Field(None, min_length=10, max_length=13)
    is_active: Optional[bool] = None

class UserInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID4
    fullname: str
    username: str
    email: EmailStr
    gender: Optional[str] = None
    contact: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

