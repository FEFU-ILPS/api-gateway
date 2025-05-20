import httpx
from fastapi import APIRouter, Body, HTTPException

from configs import configs
from schemas.auth import (
    AuthenticateUserRequest,
    AuthenticateUserResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)

from .utils.http_proxy import proxy_request

router = APIRouter(prefix="/auth")


@router.post("/login", summary="Аутентификация пользователя", tags=["Auth"])
async def athenticate_user(user_data: AuthenticateUserRequest) -> AuthenticateUserResponse:
    """Аутентифицирует пользователя в системе ILPS. Возвращает JWT токен доступа в случае успеха."""
    async with proxy_request(configs.services.auth.URL) as client:
        response = await client.post("/login", content=user_data.model_dump_json())
        response.raise_for_status()

    return AuthenticateUserResponse(**response.json())


@router.post("/register", summary="Регистрация пользователя", tags=["Auth"])
async def register_user(user_data: RegisterUserRequest = Body()) -> RegisterUserResponse:
    """Регистрирует нового пользователя в системе ILPS."""
    async with proxy_request(configs.services.auth.URL) as client:
        response = await client.post("/register", content=user_data.model_dump_json())
        response.raise_for_status()

    return RegisterUserResponse(**response.json())
