from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from .config import settings
import logging

# Async connection string for asyncpg
# Neon DATABASE_URL usually starts with postgresql://, needs to be postgresql+asyncpg://
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# asyncpg uses 'ssl' instead of 'sslmode'
if "sslmode=" in database_url:
    database_url = database_url.replace("sslmode=", "ssl=", 1)

# Remove other Neon-specific params that asyncpg doesn't like
for param in ["channel_binding="]:
    if f"{param}" in database_url:
        # This is a bit naive but works for the current .env format
        import re
        database_url = re.sub(f"{param}[^&]+&?", "", database_url)
        database_url = database_url.rstrip("&?")

engine = create_async_engine(
    database_url,
    echo=True,
    future=True
)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def init_db():
    try:
        async with engine.begin() as conn:
            # Import models here to ensure they are registered with SQLModel.metadata
            from .models.user import User
            from .models.task import Task
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        # In production, we might want to handle this differently
