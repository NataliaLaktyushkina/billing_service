import http
from datetime import datetime
from typing import List, Optional

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_decoder import jwt_decoder


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> List[str]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request=request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authentication scheme.')
            if not self.verify_jwt(jwt_token=credentials.credentials):
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid token or expired token.')
            return jwt_decoder(token=credentials.credentials).get("user_id")

        raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        try:
            payload: Optional[dict] = jwt_decoder(jwt_token)
            expire_time: Optional[int] = payload.get('exp')
            current_time: int = int(datetime.now().timestamp())
        except:
            return False
        return expire_time > current_time
