from enum import Enum
from typing import Annotated, List
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

from .utils.query_params import ListingPagination, ListingSearch, ListingSort

router = APIRouter(prefix="/texts")


class SortFields(str, Enum):
    TITLE = "title"
    DIFFICULTY = "difficulty"


class SearchFields(str, Enum):
    TITLE = "title"
    DIFFICULTY = "difficulty"
    PREVIEW = "preview"


@router.get("/", summary="Получить список всех текстов")
async def get_texts(
    search: ListingSearch[SearchFields] = Depends(),
    sort: ListingSort[SortFields] = Depends(),
    pagination: ListingPagination = Depends(),
) -> List[LearningTextResponse]:
    """Возвращает полный список всех обучающих текстов с краткой информацией."""
    async with httpx.AsyncClient() as client:
        try:
            response_params = {}
            request_params = (search, sort, pagination)

            for group in request_params:
                response_params.update(group.model_dump(exclude_none=True))

            response = await client.get(
                f"{configs.services.texts.URL}/",
                params=response_params,
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

        return [LearningTextResponse(**text) for text in response.json()]


@router.get("/{uuid}", summary="Получить детальную информацию о тексте")
async def get_text(uuid: Annotated[UUID, Path(...)]) -> DetailLearningTextResponse:
    """Возвращает полную информацию о конкретном тексте по его UUID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{configs.services.texts.URL}/{uuid}")
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return DetailLearningTextResponse(**response.json())


@router.post("/", summary="Добавить текст в систему")
async def create_text(
    data: Annotated[CreateLearningTextRequest, Body(...)],
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


@router.delete("/{uuid}", summary="Удалить текст из системы")
async def delete_text(uuid: Annotated[UUID, Path(...)]) -> DeleteLearningTextResponse:
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

    return DetailLearningTextResponse(**response.json())


@router.patch("/{uuid}", summary="Обновить данные о тексте")
async def update_text(
    uuid: Annotated[UUID, Path(...)],
    data: Annotated[UpdateLearningTextRequest, Body(...)],
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
