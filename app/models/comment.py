import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Text, Boolean, DateTime, Uuid, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    club_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("books.id", ondelete="SET NULL"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_spoiler: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    club: Mapped["Club"] = relationship("Club", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="comments", lazy="selectin")
    book: Mapped[Optional["Book"]] = relationship("Book")