import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Boolean, Enum, DateTime, Uuid, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.enums import ClubRole

class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    current_book_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid(as_uuid=True), ForeignKey("books.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner: Mapped["User"] = relationship("User")
    current_book: Mapped[Optional["Book"]] = relationship("Book", back_populates="clubs_reading", lazy="selectin")
    memberships: Mapped[List["ClubMembership"]] = relationship("ClubMembership", back_populates="club", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="club", cascade="all, delete-orphan")


class ClubMembership(Base):
    __tablename__ = "club_memberships"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    club_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("clubs.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[ClubRole] = mapped_column(Enum(ClubRole), default=ClubRole.MEMBER)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("club_id", "user_id", name="uq_club_user_membership"),)

    club: Mapped["Club"] = relationship("Club", back_populates="memberships")
    user: Mapped["User"] = relationship("User", back_populates="club_memberships", lazy="selectin")