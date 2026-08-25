import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.club import Club, ClubMembership
from app.schemas.club import ClubCreate, ClubRead, ClubUpdate, ClubMembershipRead
from app.services.club import create_club

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.post("", response_model=ClubRead)
async def create_new_club(
        club_in: ClubCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await create_club(db, current_user.id, club_in)


@router.get("", response_model=List[ClubRead])
async def list_public_clubs(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    query = (
        select(Club, func.count(ClubMembership.id))
        .outerjoin(ClubMembership, ClubMembership.club_id == Club.id)
        .where(Club.is_public == True)
        .group_by(Club.id)
        .offset(skip).limit(limit)
    )
    results = await db.execute(query)

    clubs = []
    for club, count in results.all():
        club.member_count = count
        clubs.append(club)
    return clubs


@router.get("/{club_id}", response_model=ClubRead)
async def get_club_details(club_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    query = (
        select(Club, func.count(ClubMembership.id))
        .outerjoin(ClubMembership, ClubMembership.club_id == Club.id)
        .where(Club.id == club_id)
        .group_by(Club.id)
    )
    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail="Club not found")

    club, count = row
    club.member_count = count
    return club


@router.post("/{club_id}/join", response_model=ClubMembershipRead)
async def join_club(club_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    club = await db.get(Club, club_id)
    if not club or not club.is_public:
        raise HTTPException(status_code=404, detail="Public club not found")

    mem_query = select(ClubMembership).where(ClubMembership.club_id == club_id,
                                             ClubMembership.user_id == current_user.id)
    mem_result = await db.execute(mem_query)
    if mem_result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already a member")

    membership = ClubMembership(club_id=club_id, user_id=current_user.id)
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership