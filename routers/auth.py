import httpx
from fastapi import APIRouter, Body, HTTPException

from configs import configs
from schemas.auth import (
    AuthenticateUserRequest,
    AuthenticateUserResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)

router = APIRouter(prefix="/auth")


@router.post("/login", summary="Аутентификация пользователя", tags=["Auth"])
async def athenticate_user(user_data: AuthenticateUserRequest) -> AuthenticateUserResponse:
    """Аутентифицирует пользователя в системе ILPS. Возвращает JWT токен доступа в случае успеха."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.auth.URL}/login",
                content=user_data.model_dump_json(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

        return AuthenticateUserResponse(**response.json())


@router.post("/register", summary="Регистрация пользователя", tags=["Auth"])
async def register_user(user_data: RegisterUserRequest = Body()) -> RegisterUserResponse:
    """Регистрирует нового пользователя в системе ILPS."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.auth.URL}/register",
                content=user_data.model_dump_json(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

        return RegisterUserResponse(**response.json())
