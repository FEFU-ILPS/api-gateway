from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Path, UploadFile
from sse_starlette.sse import EventSourceResponse

from configs import configs
from schemas.tasks import CreateTaskResponse, DetailTaskResponse, TasksResponse

from .utils.http_proxy import proxy_request, proxy_sse_request
from .utils.protection import AuthorizedUser, RouteProtection

router = APIRouter(prefix="/tasks")

protected = RouteProtection()


@router.post("/", summary="Создать задачу на обработку аудио файла", tags=["Tasks"])
async def create_task(
    file: Annotated[UploadFile, File(...)],
    title: Annotated[str, Form(...)],
    text_id: Annotated[UUID, Form(...)],
    auth: Annotated[AuthorizedUser, Depends(protected)],
) -> CreateTaskResponse:
    """Создаёт задачу на предобработку и транскрибирование аудиофайла.
    Возвращает UUID созданой задачи с ответом 200, выполняя её в фоне.
    """
    async with proxy_request(configs.services.manager.URL) as client:
        response = await client.post(
            "/transcribe",
            data={"title": title, "text_id": str(text_id), "user_id": str(auth.id)},
            files={"file": (file.filename, file.file, file.content_type)},
        )
        response.raise_for_status()

    return CreateTaskResponse(**response.json())


@router.get("/", summary="Получить список задач", tags=["Tasks"])
async def get_tasks(auth: Annotated[AuthorizedUser, Depends(protected)]) -> list[TasksResponse]:
    """Получает список всех задач, когда либо созданных в системе ILPS."""
    async with proxy_request(configs.services.manager.URL) as client:
        response = await client.post("/", json={"user_id": str(auth.id)})
        response.raise_for_status()

    return [TasksResponse(**task) for task in response.json()]


@router.get("/{uuid}", summary="Получить актуальную информацию о задаче", tags=["Tasks"])
async def get_task(
    uuid: Annotated[UUID, Path(...)],
    auth: Annotated[AuthorizedUser, Depends(protected)],
) -> DetailTaskResponse:
    """Получает текущую информацию по UUID указаной задачи.
    Возвращает полную информацию о задача.
    """
    async with proxy_request(configs.services.manager.URL) as client:
        response = await client.post(f"/{uuid}", json={"user_id": str(auth.id)})
        response.raise_for_status()

    return DetailTaskResponse(**response.json())


@router.get("/{uuid}/stream", summary="Получать обновления статуса задачи потоком", tags=["Tasks"])
async def monitor_task(
    uuid: Annotated[UUID, Path(...)],
    auth: Annotated[AuthorizedUser, Depends(protected)],
) -> EventSourceResponse:
    """Получает информацию об обновлениях статуса задачи
    в реальном времени, используя протокол SSE стриминга.
    """
    event_generator = proxy_sse_request(str(uuid), str(auth.id))
    return EventSourceResponse(event_generator)
