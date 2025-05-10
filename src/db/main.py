from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config

# async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))


async_engine = create_async_engine(
    Config.DATABASE_URL,
    pool_size=20,  # Number of connections to keep open inside the connection pool
    max_overflow=10,  # Number of connections to allow in overflow
    pool_timeout=30,  # Maximum number of seconds to wait for a connection to become available
    pool_recycle=1800,  # Number of seconds after which a connection is automatically recycled
)



async def init_db() -> None:
    async with async_engine.begin() as conn:
        from src.db.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession: # type: ignore
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session