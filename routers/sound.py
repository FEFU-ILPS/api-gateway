from typing import Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile

from configs import configs
from schemas.audio import CreateTaskResponse, TasksResponse, DetailTaskResponse

from .utils.protection import AuthorizedUser, RouteProtection

router = APIRouter(prefix="/sound")

protected = RouteProtection()


@router.post("/", summary="Создать задачу на обработку аудио файла", tags=["Sound"])
async def create_task(
    file: Annotated[UploadFile, File(...)],
    text_id: Annotated[UUID, Form(...)],
    auth: Annotated[AuthorizedUser, Depends(protected)],
) -> CreateTaskResponse:
    """Создаёт задачу на предобработку и транскрибирование аудиофайла.
    Возвращает UUID созданой задачи с ответом 200, выполняя её в фоне.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.manager.URL}/transcribe",
                data={"text_id": str(text_id), "user_id": str(auth.id)},
                files={"file": (file.filename, file.file, file.content_type)},
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return CreateTaskResponse(**response.json())


@router.get("/", summary="Получить список задач", tags=["Sound"])
async def get_tasks(auth: Annotated[AuthorizedUser, Depends(protected)]) -> list[TasksResponse]:
    """Получает список всех задач, когда либо созданных в системе ILPS."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.manager.URL}/",
                json={"user_id": str(auth.id)},
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return [TasksResponse(**task) for task in response.json()]


@router.get("/{uuid}", summary="Получить актуальную информацию о задаче", tags=["Sound"])
async def get_task(
    uuid: Annotated[UUID, Path(...)],
    auth: Annotated[AuthorizedUser, Depends(protected)],
) -> DetailTaskResponse:
    """Получает текущую информацию по UUID указаной задачи.
    Возвращает полную информацию о задача.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{configs.services.manager.URL}/{uuid}",
                json={"user_id": str(auth.id)},
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )

    return DetailTaskResponse(**response.json())
