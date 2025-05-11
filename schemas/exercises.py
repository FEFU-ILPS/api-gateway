from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExerciseLang(Enum):
    """Перечисление языков упражнения."""

    ENGLISH = "english"


class ExerciseTag(Enum):
    """Теги для упражнения"""

    TIMIT = "TIMIT"


class BaseSchema(BaseModel):
    """Базовая схема данных."""

    model_config = ConfigDict(from_attributes=True)


class ExerciseResponse(BaseSchema):
    """Данные, отправляемые в ответ на запрос получения списка упражнений."""

    id: UUID = Field(description="Идентификатор упражнения")
    seq_number: int = Field(description="Номер упражнения", gt=0)
    difficulty: int = Field(description="Сложность упражнения", ge=0)
    preview_image: str | None = Field(description="Изображение превью", default=None)
    lang: ExerciseLang = Field(description="Язык упражнения")
    tags: list[ExerciseTag] = Field(description="Теги упражнения", default=[])


class DetailExerciseResponse(BaseSchema):
    """Данные, отправляемые в ответ на запрос получения деталей об упражнении."""

    id: UUID = Field(description="Идентификатор упражнения")
    seq_number: int = Field(description="Номер упражнения", gt=0)
    difficulty: int = Field(description="Сложность упражнения", ge=0)
    preview_image: str | None = Field(description="Изображение превью", default=None)
    background_image: str | None = Field(description="Изображение фона", default=None)
    text_id: UUID = Field(description="Идентификатор текста")
    lang: ExerciseLang = Field(description="Язык упражнения")
    tags: list[ExerciseTag] = Field(description="Теги упражнения", default=[])


class CreateExerciseRequest(BaseSchema):
    """Данные, отправляемые в ответ на запрос добавления нового упражнения."""

    difficulty: int = Field(description="Сложность упражнения", ge=0)
    preview_image: str | None = Field(description="Изображение превью", default=None)
    background_image: str | None = Field(description="Изображение фона", default=None)
    text_id: UUID = Field(description="Идентификатор текста")
    lang: ExerciseLang = Field(description="Язык упражнения")
    tags: list[ExerciseTag] = Field(description="Теги упражнения", default=[])


class CreateExerciseResponse(BaseSchema):
    """Данные, требующиеся для создания/добавления нового упражнения."""

    id: UUID = Field(description="Идентификатор упражнения")
    seq_number: int = Field(description="Номер упражнения", gt=0)


class DeleteExerciseResponse(BaseSchema):
    """Данные, отправляемые в ответ на запрос добавления нового упражнения."""

    id: UUID = Field(description="Идентификатор упражнения")


class UpdateExerciseRequest(BaseSchema):
    """Данные, для обновления информации об упражнении."""

    difficulty: int | None = Field(description="Сложность упражнения", ge=0, default=None)
    preview_image: str | None = Field(description="Изображение превью", default=None)
    background_image: str | None = Field(description="Изображение фона", default=None)
    lang: ExerciseLang | None = Field(description="Язык упражнения", default=None)
    tags: list[ExerciseTag] | None = Field(description="Теги упражнения", default=None)
    text_id: UUID | None = Field(description="Идентификатор текста", default=None)


class UpdateExerciseResponse(BaseSchema):
    """Данные, отправляемые в ответ на запрос изменения информации об упражнении."""

    id: UUID = Field(description="Идентификатор упражнения")
    seq_number: int = Field(description="Номер упражнения", gt=0)
    difficulty: int = Field(description="Сложность упражнения", ge=0)
    preview_image: str | None = Field(description="Изображение превью", default=None)
    background_image: str | None = Field(description="Изображение фона", default=None)
    text_id: UUID = Field(description="Идентификатор текста")
    lang: ExerciseLang = Field(description="Язык упражнения")
    tags: list[ExerciseTag] = Field(description="Теги упражнения", default=[])
