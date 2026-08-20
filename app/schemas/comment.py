from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserRead

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)
    is_spoiler: bool = False

class CommentCreate(CommentBase):
    book_id: Optional[int] = None

class CommentRead(CommentBase):
    id: int
    club_id: int
    user_id: int
    book_id: Optional[int] = None
    created_at: datetime
    user: Optional[UserRead] = None

    model_config = ConfigDict(from_attributes=True)