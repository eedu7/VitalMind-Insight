from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from httpx import ASGITransport, AsyncClient
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings
from core.server import app
from db.models import Base
from db.session import get_session

test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False, future=True)
TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def redis_client():
    client: Redis = redis.from_url(settings.TEST_REDIS_URL, encoding="utf8", decode_responses=True)  # type: ignore
    await FastAPILimiter.init(client)  # type: ignore
    yield client
    await client.aclose()


@pytest_asyncio.fixture()
async def client(redis_client: Redis) -> AsyncGenerator[AsyncClient, Any]:
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
