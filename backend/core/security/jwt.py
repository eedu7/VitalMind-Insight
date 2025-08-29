from typing import Any, Dict, Literal

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from utils import get_timestamp

TokenType = Literal["access", "refresh"]


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

    def encode(self, payload: Dict[str, Any], token_type: TokenType, expire_minutes: int = 1440) -> str:
        expire_time = get_timestamp(minutes=expire_minutes)
        payload.update({"exp": expire_time, "type": token_type, "iss": self.issuer, "iat": get_timestamp()})
        return jwt.encode(  # type: ignore
            payload,
            self.secret_key,
            self.algorithm,
        )

    def decode(self, token: str, expected_type: TokenType, verify_exp: bool = True) -> Dict[str, Any]:
        try:
            payload = jwt.decode(  # type: ignore
                jwt=token, key=self.secret_key, algorithms=[self.algorithm], options={"verify_exp": verify_exp}
            )

            if payload.get("type") != expected_type:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
