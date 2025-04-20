import json

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from configs import configs
from schemas.auth import AuthorizedUser


# ! На данный момент это не будет работать непостредственно в Swagger
# ! URL /auth/login принимает JSON, а не URL-Encoded, что подразумевается
# ! в использовании OAuthPasswordBearer.
# TODO: Рассмотреть варианты
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class RouteProtection:
    """Класс, предоставляющий интерфейс зависимости FastAPI для защиты
    роутов от неавторизованного доступа.
    """

    def __init__(self, only_admin: bool = False) -> None:
        """Конструктор класса.

        Args:
            only_admin (bool, optional): Доступ только администраторам. Defaults to False.
        """
        self.only_admin = only_admin

    async def __call__(self, token: str = Depends(oauth2_scheme)) -> AuthorizedUser:
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

        authorized = AuthorizedUser(**response.json())
        self.__check_rights(authorized)

        return authorized

    def __check_rights(self, authorized: AuthorizedUser) -> None:
        """Проверка необходимых прав у авторизованного пользователя.

        Args:
            authorized (AuthorizedUser): Данные авторизованного пользователя.

        Raises:
            HTTPException: 403. Доступ запрещён из-за нехватки прав.
        """
        if not authorized.is_admin and self.only_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Action is unavailable",
            )
