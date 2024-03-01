from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api_v1.services import TokenService

http_bearer = HTTPBearer()


async def get_refresh_from_cookie(refresh_token: str = Cookie(alias="refresh_token")):
    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found",
        )
    return refresh_token


async def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    payload = await TokenService.validate_token(token=token)
    return payload


async def get_current_active_auth_user(user=Depends(get_current_auth_user)):
    if user["active"]:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
