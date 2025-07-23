from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# engine = create_asyncengine()

DATABASE_URL = "postgresql+asyncpg://admin:admin123@localhost:5432/postgres"

engine = create_async_engine(url=DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine=engine, _class=AsyncSession, autoflush=False, expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
