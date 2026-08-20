from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.club import Club, ClubMembership
from app.models.enums import ClubRole
from app.schemas.club import ClubCreate


async def create_club(db: AsyncSession, user_id: int, club_in: ClubCreate) -> Club:
    # 1. Create the Club
    new_club = Club(
        name=club_in.name,
        description=club_in.description,
        cover_url=club_in.cover_url,
        is_public=club_in.is_public,
        owner_id=user_id,
        current_book_id=club_in.current_book_id
    )
    db.add(new_club)
    await db.flush()  # Flush to get the new_club.id without committing the transaction yet

    # 2. Add the owner as a member
    membership = ClubMembership(
        club_id=new_club.id,
        user_id=user_id,
        role=ClubRole.OWNER
    )
    db.add(membership)

    # Commit both together
    await db.commit()
    await db.refresh(new_club)
    return new_club


async def join_club(db: AsyncSession, user_id: int, club_id: int) -> ClubMembership:
    # Check if club exists
    club = await db.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    # Check if already a member
    query = select(ClubMembership).where(
        ClubMembership.club_id == club_id,
        ClubMembership.user_id == user_id
    )
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="You are already a member of this club.")

    new_membership = ClubMembership(
        club_id=club_id,
        user_id=user_id,
        role=ClubRole.MEMBER
    )
    db.add(new_membership)
    await db.commit()
    await db.refresh(new_membership)
    return new_membership