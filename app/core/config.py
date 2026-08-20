from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, EmailStr, PostgresDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "ShelfLife API"

    # Security
    SECRET_KEY: str  # e.g., run `openssl rand -hex 32` to generate
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str  # e.g., postgresql+asyncpg://user:password@localhost:5432/shelflife

    # OAuth: Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # OAuth: GitHub
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    # Session (Authlib needs this for temporary state storage during OAuth flow)
    SESSION_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


settings = Settings()