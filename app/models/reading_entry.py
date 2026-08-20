from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, Text, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.enums import ReadingStatus

class ReadingEntry(Base):
    __tablename__ = "reading_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[ReadingStatus] = mapped_column(Enum(ReadingStatus), default=ReadingStatus.WANT_TO_READ, nullable=False)
    current_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1–5
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    private_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="uq_user_book_reading_entry"),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="reading_entries")
    book: Mapped["Book"] = relationship("Book", back_populates="reading_entries")