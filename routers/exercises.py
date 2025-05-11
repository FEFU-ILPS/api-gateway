from typing import Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, Body, Depends, HTTPException, Path

from configs import configs
from schemas.exercises import (
    CreateExerciseRequest,
    CreateExerciseResponse,
    DeleteExerciseResponse,
    DetailExerciseResponse,
    ExerciseResponse,
    UpdateExerciseRequest,
    UpdateExerciseResponse,
)

from .utils.embeded import Embeded, EmbededResponse
from .utils.pagination import PaginatedResponse, Pagination
from .utils.protection import AuthorizedUser, RouteProtection

router = APIRouter(prefix="/exercises")

protected = RouteProtection()
admin_protected = RouteProtection(only_admin=True)


@router.get("/", summary="Получить список всех упражнений", tags=["Exercises"])
async def get_exercises(
    pg: Annotated[Pagination, Depends()],
    _: Annotated[AuthorizedUser, Depends(protected)],
) -> PaginatedResponse[ExerciseResponse]:
    """Постранично возвращает список всех обучающих упражнений."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{configs.services.exercises.URL}/",
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

        return PaginatedResponse[ExerciseResponse](**response.json())


# TODO: рассмотерть вынесение функционала embed в отдельный роут `/{uuid}/embeded`
@router.get("/{uuid}", summary="Получить детальную информацию об упражнении", tags=["Exercises"])
async def get_exercise(
    uuid: Annotated[UUID, Path(...)],
    emb: Annotated[Embeded, Depends()],
    _: Annotated[AuthorizedUser, Depends(protected)],
) -> EmbededResponse[DetailExerciseResponse]:
    """Возвращает полную информацию о конкретном упражнении по его UUID."""

    embed = {}
    entities = emb.get_entities()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{configs.services.exercises.URL}/{uuid}")
            response.raise_for_status()
            item = DetailExerciseResponse(**response.json())

            if "text" in entities:
                response = await client.get(f"{configs.services.texts.URL}/{item.text_id}")
                response.raise_for_status()
                embed["text"] = response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return EmbededResponse[DetailExerciseResponse](item=item, embeded=embed)


@router.post("/", summary="Добавить упражнение в систему", tags=["Exercises"])
async def create_exercise(
    data: Annotated[CreateExerciseRequest, Body(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> CreateExerciseResponse:
    """Добавляет новое упражнение в систему."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.exercises.URL}/",
                content=data.model_dump_json(exclude_none=True),
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return CreateExerciseResponse(**response.json())


@router.delete("/{uuid}", summary="Удалить упражнение из системы", tags=["Exercises"])
async def delete_exercise(
    uuid: Annotated[UUID, Path(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> DeleteExerciseResponse:
    """Удаляет упражнение из системы по его UUID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{configs.services.exercises.URL}/{uuid}")
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return DeleteExerciseResponse(**response.json())


@router.patch("/{uuid}", summary="Обновить данные о тексте", tags=["Exercises"])
async def update_exercise(
    uuid: Annotated[UUID, Path(...)],
    data: Annotated[UpdateExerciseRequest, Body(...)],
    _: Annotated[AuthorizedUser, Depends(admin_protected)],
) -> UpdateExerciseResponse:
    """Обновляет данные текста по его UUID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(
                f"{configs.services.exercises.URL}/{uuid}",
                content=data.model_dump_json(exclude_none=True),
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return UpdateExerciseResponse(**response.json())
