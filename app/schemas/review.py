from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserRead

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    body: str = Field(..., min_length=1)

class ReviewCreate(ReviewBase):
    book_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    body: Optional[str] = Field(None, min_length=1)

class ReviewRead(ReviewBase):
    id: int
    user_id: int
    book_id: int
    created_at: datetime
    user: Optional[UserRead] = None

    model_config = ConfigDict(from_attributes=True)