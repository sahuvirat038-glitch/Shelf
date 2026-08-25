import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Uuid, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, unique=True)
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    reading_entries: Mapped[List["ReadingEntry"]] = relationship("ReadingEntry", back_populates="book")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="book")
    teachings: Mapped[List["Teaching"]] = relationship("Teaching", back_populates="book")
    clubs_reading: Mapped[List["Club"]] = relationship("Club", back_populates="current_book")