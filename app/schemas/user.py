from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserRead(UserBase):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)