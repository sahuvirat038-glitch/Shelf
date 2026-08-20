from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.club import Club, ClubMembership
from app.schemas.club import ClubCreate, ClubRead, ClubUpdate, ClubMembershipRead
from app.services.club import create_club, join_club

router = APIRouter(prefix="/clubs", tags=["clubs"])

@router.post("", response_model=ClubRead)
async def start_new_club(
    club_in: ClubCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new book club (you become the owner)."""
    return await create_club(db, current_user.id, club_in)

@router.get("", response_model=List[ClubRead])
async def list_public_clubs(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Browse public book clubs."""
    query = select(Club).where(Club.is_public == True).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{club_id}", response_model=ClubRead)
async def get_club_details(club_id: int, db: AsyncSession = Depends(get_db)):
    """Get details of a specific club."""
    club = await db.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return club

@router.post("/{club_id}/join", response_model=ClubMembershipRead)
async def join_existing_club(
    club_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Join a public book club."""
    return await join_club(db, current_user.id, club_id)