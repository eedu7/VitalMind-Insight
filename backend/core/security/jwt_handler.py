from typing import Any, Dict, Literal
from uuid import uuid4

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from utils import get_timestamp

JWTTokenType = Literal["access", "refresh"]


class JwtHandler:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        issuer: str = "myapp",
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.issuer = issuer

    def encode(
        self,
        payload: Dict[str, Any],
        token_type: JWTTokenType,
        expire_minutes: int = 1440,
        expire_seconds: int = 0,
    ) -> str:
        expire_time = get_timestamp(minutes=expire_minutes, seconds=expire_seconds)
        payload.update(
            {
                "exp": expire_time,
                "type": token_type,
                "iss": self.issuer,
                "iat": get_timestamp(),
                "jti": str(uuid4()),
            }
        )
        return jwt.encode(  # type: ignore
            payload,
            self.secret_key,
            self.algorithm,
        )

    def decode(
        self, token: str, expected_type: JWTTokenType, verify_exp: bool = True
    ) -> Dict[str, Any]:
        try:
            payload = jwt.decode(  # type: ignore
                jwt=token,
                key=self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": verify_exp},
            )

            if payload.get("type") != expected_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type",
                )

            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
