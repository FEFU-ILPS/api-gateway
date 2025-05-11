from typing import Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, Body, Depends, HTTPException, Path

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

from .utils.pagination import PaginatedResponse, Pagination
from .utils.protection import AuthorizedUser, RouteProtection
from .utils.embeded import Embeded, EmbededResponse

router = APIRouter(prefix="/texts")

protected = RouteProtection()
admin_protected = RouteProtection(only_admin=True)


@router.get("/", summary="Получить список всех текстов", tags=["Texts"])
async def get_texts(
    pg: Annotated[Pagination, Depends()],
    _: Annotated[AuthorizedUser, Depends(protected)],
) -> PaginatedResponse[LearningTextResponse]:
    """Возвращает полный список всех обучающих текстов с краткой информацией."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{configs.services.texts.URL}/",
                params={
                    "page": pg.page,
                    "size": pg.size,
                },
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

        return PaginatedResponse[LearningTextResponse](**response.json())


@router.get("/{uuid}", summary="Получить детальную информацию о тексте", tags=["Texts"])
async def get_text(
    uuid: Annotated[UUID, Path(...)],
    emb: Annotated[Embeded, Depends()],
    _: Annotated[AuthorizedUser, Depends(protected)],
) -> EmbededResponse[DetailLearningTextResponse]:
    """Возвращает полную информацию о конкретном тексте по его UUID."""

    embed = {}
    entities = emb.get_entities()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{configs.services.texts.URL}/{uuid}")
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    item = DetailLearningTextResponse(**response.json())
    return EmbededResponse[DetailLearningTextResponse](item=item, embeded=embed)


@router.post("/", summary="Добавить текст в систему", tags=["Texts"])
async def create_text(
    data: Annotated[CreateLearningTextRequest, Body(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> CreateLearningTextResponse:
    """Добавляет новый текст в систему."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.texts.URL}/",
                content=data.model_dump_json(exclude_none=True),
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return CreateLearningTextResponse(**response.json())


@router.delete("/{uuid}", summary="Удалить текст из системы", tags=["Texts"])
async def delete_text(
    uuid: Annotated[UUID, Path(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> DeleteLearningTextResponse:
    """Удаляет текст из системы по его UUID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{configs.services.texts.URL}/{uuid}")
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return DeleteLearningTextResponse(**response.json())


@router.patch("/{uuid}", summary="Обновить данные о тексте", tags=["Texts"])
async def update_text(
    uuid: Annotated[UUID, Path(...)],
    data: Annotated[UpdateLearningTextRequest, Body(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> UpdateLearningTextResponse:
    """Обновляет данные текста по его UUID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(
                f"{configs.services.texts.URL}/{uuid}",
                content=data.model_dump_json(exclude_none=True),
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return UpdateLearningTextResponse(**response.json())
