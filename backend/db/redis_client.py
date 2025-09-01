import redis.asyncio as redis
from redis.asyncio.client import Redis

from core.config import settings

redis_client: Redis = redis.from_url(
    settings.REDIS_URL, encoding="utf8", decode_responses=True
)  # type: ignore
