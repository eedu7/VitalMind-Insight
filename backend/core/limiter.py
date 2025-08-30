from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from redis.asyncio.client import Redis

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis_conntection: Redis = redis.from_url(settings.REDIS_URL, encoding="utf8", decoded_responses=True)  # type: ignore
    await FastAPILimiter.init(redis_conntection)  # type: ignore
    try:
        yield
    finally:
        await FastAPILimiter.close()
