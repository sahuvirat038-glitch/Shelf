from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from database import engine

from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.books import router as books_router
from app.api.reading_entries import router as reading_entries_router
from app.api.clubs import router as clubs_router
from app.api.reviews import router as reviews_router
from app.api.teachings import router as teachings_router
from app.api.comments import router as comments_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Complete Backend API for ShelfLife"
)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(books_router)
app.include_router(reading_entries_router)
app.include_router(clubs_router)
app.include_router(reviews_router)
app.include_router(teachings_router)
app.include_router(comments_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)