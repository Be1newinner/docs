from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from model import Todo


@asynccontextmanager
async def lifespan(app: FastAPI):
    """start this function with FastAPI Server

    Args:
        app (FastAPI): This will setup the postgres database as soon the FastAPI starts
    """
    async with engine.begin() as conn:
        table_exists = await conn.run_sync(
            lambda sync_conn: engine.dialect.has_table(sync_conn, Todo.__tablename__)
        )
    if not table_exists:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(debug=True, lifespan=lifespan)
