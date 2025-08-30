from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from math import ceil

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi_limiter import FastAPILimiter

from db import redis_client


async def rate_limit_callback(request: Request, response: Response, pexpire: int):
    expire: int = ceil(pexpire / 1000)

    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=f"Rate limit exceeded. Please try again in {expire} seconds.",
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await FastAPILimiter.init(redis_client, http_callback=rate_limit_callback)  # type: ignore
    try:
        yield
    finally:
        await FastAPILimiter.close()
