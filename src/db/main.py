


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, text
from src.config import Config
from sqlmodel import SQLModel
from src.books.models import Book


engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def initdb():
    """create our database models in the database"""

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Dependency Injections

# async def get_session() -> AsyncSession: # type: ignore
#     ''' Dependency to provide session object '''
#     async_session = sessionmaker(
#         bind = create_async_engine, class_=AsyncSession, expire_on_commit= False
#     )

#     async with async_session() as session:
#         yield session