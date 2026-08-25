import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Enum, DateTime, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.enums import OAuthProvider

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oauth_provider: Mapped[OAuthProvider] = mapped_column(Enum(OAuthProvider), nullable=False)
    oauth_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    reading_entries: Mapped[List["ReadingEntry"]] = relationship("ReadingEntry", back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    teachings: Mapped[List["Teaching"]] = relationship("Teaching", back_populates="user", cascade="all, delete-orphan")
    club_memberships: Mapped[List["ClubMembership"]] = relationship("ClubMembership", back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")