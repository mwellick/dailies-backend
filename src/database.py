import contextlib

from typing import Any, AsyncIterator

from src.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseSessionmanager:

    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception('DatabaseSessionmanager is not initialized.')

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    async def close(self):
        if self._engine is None:
            raise Exception('DatabaseSessionmanager is not initialized.')

        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception('DatabaseSessionmanager is not initialized.')

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


sessionmanager = DatabaseSessionmanager(settings.database_url, engine_kwargs={"echo": settings.ECHO_SQL})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session
