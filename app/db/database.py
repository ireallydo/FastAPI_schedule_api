from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from asyncio import sleep
from db.models import BaseModel
from settings import Settings
from httpx import AsyncClient
from loguru import logger


settings = Settings()

db_connection_str = f"postgresql+asyncpg://"\
                 f"{settings.DB_USER}:{settings.DB_PASSWORD}@" \
                 f"{settings.DB_HOST}/{settings.DB_NAME}"
logger.debug(f"DB Connection string: {db_connection_str }")
engine = create_async_engine(db_connection_str, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession)
session = AsyncClient()


async def init_db():
    await sleep(20)
    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        await connection.run_sync(BaseModel.metadata.create_all)
