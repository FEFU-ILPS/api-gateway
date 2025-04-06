from typing import Annotated, List
from uuid import UUID

import httpx
from fastapi import APIRouter, Path, HTTPException

from configs import configs
from schemas.texts import DetailLearningTextResponse, LearningTextResponse

router = APIRouter(prefix="/texts")


@router.get("/", summary="Получить список всех текстов")
async def get_texts() -> List[LearningTextResponse]:
    """Возвращает полный список всех обучающих текстов с краткой информацией."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{configs.services.texts.URL}/")
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
