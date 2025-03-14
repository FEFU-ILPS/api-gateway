import json

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from configs import configs
from schemas.auth import AuthorizedUser


# ! На данный момент это не будет работать непостредственно в Swagger
# ! URL /auth/login принимает JSON, а не URL-Encoded, что подразумевается
# ! в использовании OAuthPasswordBearer.
# TODO: Рассмотреть варианты
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def protected(token: str = Depends(oauth2_scheme)) -> AuthorizedUser:
    """Зависимость FastAPI, которая парсит токен доступа из заголовка Authorization.
    Производит авторизацию пользователя, возвращает информацию о нем и его правах в системе.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.auth.URL}/verify",
                content=json.dumps({"access_token": token}),
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error."),
                headers={"WWW-Authenticate": "Bearer"},
            )

    return AuthorizedUser(**response.json())
