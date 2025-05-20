from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path

from configs import configs
from schemas.texts import (
    CreateLearningTextRequest,
    CreateLearningTextResponse,
    DeleteLearningTextResponse,
    DetailLearningTextResponse,
    LearningTextResponse,
    UpdateLearningTextRequest,
    UpdateLearningTextResponse,
)

from .utils.http_proxy import proxy_request
from .utils.pagination import PaginatedResponse, Pagination
from .utils.protection import AuthorizedUser, RouteProtection

router = APIRouter(prefix="/texts")

protected = RouteProtection()
admin_protected = RouteProtection(only_admin=True)


@router.get("/", summary="Получить список всех текстов", tags=["Texts"])
async def get_texts(
    pg: Annotated[Pagination, Depends()],
    _: Annotated[AuthorizedUser, Depends(protected)],
) -> PaginatedResponse[LearningTextResponse]:
    """Возвращает полный список всех обучающих текстов с краткой информацией."""
    async with proxy_request(configs.services.texts.URL) as client:
        response = await client.get("/", params={"page": pg.page, "size": pg.size})
        response.raise_for_status()

    return PaginatedResponse[LearningTextResponse](**response.json())


@router.get("/{uuid}", summary="Получить детальную информацию о тексте", tags=["Texts"])
async def get_text(
    uuid: Annotated[UUID, Path(...)],
    _: Annotated[AuthorizedUser, Depends(protected)],
) -> DetailLearningTextResponse:
    """Возвращает полную информацию о конкретном тексте по его UUID."""
    async with proxy_request(configs.services.texts.URL) as client:
        response = await client.get(f"/{uuid}")
        response.raise_for_status()

    return DetailLearningTextResponse(**response.json())


@router.post("/", summary="Добавить текст в систему", tags=["Texts"])
async def create_text(
    data: Annotated[CreateLearningTextRequest, Body(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> CreateLearningTextResponse:
    """Добавляет новый текст в систему."""
    async with proxy_request(configs.services.texts.URL) as client:
        response = await client.post("/", content=data.model_dump_json(exclude_none=True))
        response.raise_for_status()

    return CreateLearningTextResponse(**response.json())


@router.delete("/{uuid}", summary="Удалить текст из системы", tags=["Texts"])
async def delete_text(
    uuid: Annotated[UUID, Path(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> DeleteLearningTextResponse:
    """Удаляет текст из системы по его UUID."""
    async with proxy_request(configs.services.texts.URL) as client:
        response = await client.delete(f"/{uuid}")
        response.raise_for_status()

    return DeleteLearningTextResponse(**response.json())


@router.patch("/{uuid}", summary="Обновить данные о тексте", tags=["Texts"])
async def update_text(
    uuid: Annotated[UUID, Path(...)],
    data: Annotated[UpdateLearningTextRequest, Body(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> UpdateLearningTextResponse:
    """Обновляет данные текста по его UUID."""
    async with proxy_request(configs.services.texts.URL) as client:
        response = await client.patch(f"/{uuid}", content=data.model_dump_json(exclude_none=True))
        response.raise_for_status()

    return UpdateLearningTextResponse(**response.json())
