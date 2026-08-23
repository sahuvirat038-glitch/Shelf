import asyncio
from app.db.session import engine
from app.models.base import Base

# Import every model so SQLAlchemy knows about all tables
from app.models import user, book, reading_entry, review, teaching, club, comment  # noqa

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

if __name__ == "__main__":
    asyncio.run(create_tables())