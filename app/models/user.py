from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, utc_now
from app.models.enums import OAuthProvider

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    oauth_provider: Mapped[OAuthProvider] = mapped_column(Enum(OAuthProvider), nullable=False)
    oauth_id: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        UniqueConstraint("oauth_provider", "oauth_id", name="uq_oauth_provider_id"),
    )

    # Relationships
    reading_entries: Mapped[List["ReadingEntry"]] = relationship("ReadingEntry", back_populates="user", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    teachings: Mapped[List["Teaching"]] = relationship("Teaching", back_populates="user", cascade="all, delete-orphan")
    clubs_owned: Mapped[List["Club"]] = relationship("Club", back_populates="owner", foreign_keys="Club.owner_id")
    club_memberships: Mapped[List["ClubMembership"]] = relationship("ClubMembership", back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")