from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from math import ceil

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi_limiter import FastAPILimiter
from redis.asyncio.client import Redis

from core.config import settings


async def rate_limit_callback(request: Request, response: Response, pexpire: int):
    expire: int = ceil(pexpire / 1000)

    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=f"Rate limit exceeded. Please try again in {expire} seconds.",
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis_connection: Redis = redis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)  # type: ignore
    await FastAPILimiter.init(redis_connection, http_callback=rate_limit_callback)  # type: ignore
    try:
        yield
    finally:
        await FastAPILimiter.close()
