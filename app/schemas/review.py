from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserPublic

class ReviewBase(BaseModel):
    book_id: int
    rating: int = Field(..., ge=1, le=5)
    content: str

class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    content: Optional[str] = None

class ReviewRead(ReviewBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[UserPublic] = None

    model_config = ConfigDict(from_attributes=True)