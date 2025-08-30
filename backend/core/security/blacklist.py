from datetime import UTC, datetime
from typing import Any, Dict

from redis.asyncio.client import Redis


class TokenBlacklist:
    def __init__(self, redis_client: Redis, prefix: str = "blacklist") -> None:
        self.redis = redis_client
        self.prefix = prefix

    def _generate_key(self, jti: str) -> str:
        return f"{self.prefix}::{jti}"

    async def add(self, payload: Dict[str, Any]) -> None:
        jti: str | None = payload.get("jti", None)
        exp: int | None = payload.get("exp", None)

        if not jti or not exp:
            raise ValueError("Token missing jti or exp claim.")

        expires_in = exp - int(datetime.now(UTC).timestamp())

        if expires_in <= 0:
            return

        await self.redis.set(self._generate_key(jti), "true", ex=expires_in)

    async def is_blacklisted(self, jti: str) -> bool:
        return await self.redis.exists(self._generate_key(jti)) > 0
