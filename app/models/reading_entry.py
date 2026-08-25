import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Enum, DateTime, Uuid, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.enums import ReadingStatus

class ReadingEntry(Base):
    __tablename__ = "reading_entries"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[ReadingStatus] = mapped_column(Enum(ReadingStatus), nullable=False)
    current_page: Mapped[int] = mapped_column(Integer, default=0)
    total_pages: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="reading_entries")
    book: Mapped["Book"] = relationship("Book", back_populates="reading_entries", lazy="selectin")