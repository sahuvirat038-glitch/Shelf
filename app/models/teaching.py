import uuid
from datetime import datetime
from sqlalchemy import Text, Boolean, DateTime, Uuid, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Teaching(Base):
    __tablename__ = "teachings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="teachings")
    book: Mapped["Book"] = relationship("Book", back_populates="teachings")