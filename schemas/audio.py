from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

from .examples.audio import (
    ID_EXAMPLES,
    STATUS_EXAMPLES,
    RESULT_EXAMPLES,
    ACCURACY_EXAMPLES,
    ERRORS_EXAMPLES,
    COMMENTS_EXAMPLES,
)


class Status(Enum):
    """Перечисление возможных значений статусов задачи."""

    CREATED = "created"
    STARTED = "started"
    PREPROCESSING = "preprocessing"
    TRANSCRIBING = "transcribing"
    COMPLETED = "completed"
    FAILED = "failed"
    UNKNOWN = "unknown"


TaskID = Annotated[UUID, Field(description="Уникальный идентификатор", examples=ID_EXAMPLES)]
TaskUserID = Annotated[UUID, Field(description="Идентификатор пользователя", examples=ID_EXAMPLES)]
TaskTextID = Annotated[UUID, Field(description="Идентификатор текста", examples=ID_EXAMPLES)]
TaskStatus = Annotated[Status, Field(description="Статуст выполнения", examples=STATUS_EXAMPLES)]
TaskResult = Annotated[
    str | None, Field(description="Результат транскрибирования", examples=RESULT_EXAMPLES)
]
TaskResultAccuracy = Annotated[
    float | None,
    Field(description="Точность произношения", ge=0, le=100, examples=ACCURACY_EXAMPLES),
]
TaskResultErrors = Annotated[
    list[dict[str, int | str | None]] | None,
    Field(description="Ошибки произношения", examples=ERRORS_EXAMPLES),
]
TaskComment = Annotated[
    str | None, Field(description="Комментарий к задаче", examples=COMMENTS_EXAMPLES)
]


class TasksRequest(BaseModel):
    """Данные, необходимые для получения задач."""

    user_id: TaskUserID


# *Не используется. Пришлось отказаться из-за особенностей загрузки файлов.
class CreateTaskRequest(TasksRequest):
    """Данные, необходимые для создания задачи."""

    text_id: TaskTextID


class DetailTaskRequest(TasksRequest):
    """Данные, необходимые для получения задач."""


class CreateTaskResponse(BaseModel):
    """Данные, отправляемые в ответ на создание задачи."""

    model_config = ConfigDict(from_attributes=True)

    id: TaskID


class TasksResponse(CreateTaskResponse):
    """Данные, отправляемые в ответ на получение задач."""

    user_id: TaskUserID
    status: TaskStatus


class DetailTaskResponse(CreateTaskResponse):
    """Данные, отправляемые в ответ на получение информации
    по конкретной задаче.
    """

    user_id: TaskUserID
    text_id: TaskTextID
    status: TaskStatus
    result: TaskResult
    accuracy: TaskResultAccuracy
    errors: TaskResultErrors
    comment: TaskComment
