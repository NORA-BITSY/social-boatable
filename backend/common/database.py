from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

settings = get_settings()

SYNC_ENGINE = create_engine(
    settings.database_url, pool_pre_ping=True,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
)

ASYNC_ENGINE = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    pool_size=10, max_overflow=5, pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=SYNC_ENGINE, autocommit=False, autoflush=False)
AsyncSessionLocal = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass
