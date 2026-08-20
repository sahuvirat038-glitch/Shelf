from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, utc_now

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    author: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    cover_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    genre: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship("User")
    reading_entries: Mapped[List["ReadingEntry"]] = relationship("ReadingEntry", back_populates="book", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="book", cascade="all, delete-orphan")
    teachings: Mapped[List["Teaching"]] = relationship("Teaching", back_populates="book", cascade="all, delete-orphan")
    clubs_reading: Mapped[List["Club"]] = relationship("Club", back_populates="current_book")