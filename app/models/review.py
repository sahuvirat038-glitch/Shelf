import uuid
from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, Uuid, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("user_id", "book_id", name="uq_user_book_review"),)

    user: Mapped["User"] = relationship("User", back_populates="reviews", lazy="selectin")
    book: Mapped["Book"] = relationship("Book", back_populates="reviews")