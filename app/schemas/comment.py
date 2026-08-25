import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserPublic

class CommentBase(BaseModel):
    book_id: Optional[uuid.UUID] = None
    content: str
    is_spoiler: bool = False

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: uuid.UUID
    club_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    user: Optional[UserPublic] = None

    model_config = ConfigDict(from_attributes=True)