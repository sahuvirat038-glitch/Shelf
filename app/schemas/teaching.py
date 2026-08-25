import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserPublic

class TeachingBase(BaseModel):
    book_id: uuid.UUID
    content: str
    is_public: bool = True

class TeachingCreate(TeachingBase):
    pass

class TeachingUpdate(BaseModel):
    content: Optional[str] = None
    is_public: Optional[bool] = None

class TeachingRead(TeachingBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    user: Optional[UserPublic] = None

    model_config = ConfigDict(from_attributes=True)