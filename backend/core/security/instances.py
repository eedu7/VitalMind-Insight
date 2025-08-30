from core.config import settings
from db import redis_client

from .blacklist import TokenBlacklist
from .jwt_handler import JwtHandler

jwt_handler: JwtHandler = JwtHandler(secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

token_blacklist: TokenBlacklist = TokenBlacklist(redis_client=redis_client)
