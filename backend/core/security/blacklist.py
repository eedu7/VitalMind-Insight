from redis.asyncio.client import Redis


class TokenBlacklist:
    def __init__(self, redis_client: Redis, prefix: str = "blacklist") -> None:
        self.redis = redis_client
        self.prefix = prefix

    def _generate_key(self, jti: str) -> str:
        return f"{self.prefix}/{jti}"

    async def add(self, jti: str, expires_in: int) -> None:
        await self.redis.set(self._generate_key(jti), "true", ex=expires_in)

    async def is_blacklisted(self, jti: str) -> bool:
        return await self.redis.exists(self._generate_key(jti)) > 0
