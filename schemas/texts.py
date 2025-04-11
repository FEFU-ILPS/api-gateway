from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from fastapi import Body
from pydantic import Field

from .examples.texts import (
    DIFFICULTY_EXAMPLES,
    ID_EXAMPLES,
    PREVIEW_EXAMPLES,
    TITLE_EXAMPLES,
    TRANSCRIPTION_EXAMPLES,
    VALUE_EXAMPLES,
)

TextID = Annotated[UUID, Field(description="Уникальный идентификатор", examples=ID_EXAMPLES)]
TextTitle = Annotated[str, Field(max_length=100, description="Название", examples=TITLE_EXAMPLES)]
TextValue = Annotated[str, Field(description="Содержание", examples=VALUE_EXAMPLES)]

TextPreview = Annotated[
    str, Field(max_length=500, description="Краткое описание", examples=PREVIEW_EXAMPLES)
]
TextDifficulty = Annotated[
    int, Field(ge=0, le=10, description="Сложность", examples=DIFFICULTY_EXAMPLES)
]
TextTranscription = Annotated[
    str, Field(description="Транскрипционная запись", examples=TRANSCRIPTION_EXAMPLES)
]


class LearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос получения всех текстов."""

    model_config = ConfigDict(from_attributes=True)

    id: TextID
    title: TextTitle
    difficulty: Optional[TextDifficulty] = Body(default=0)
    preview: TextPreview


class DetailLearningTextResponse(LearningTextResponse):
    """Данные, отправляемые в ответ на запрос получения деталей о тексте."""

    value: TextValue
    transcription: TextTranscription


class CreateLearningTextRequest(BaseModel):
    """Данные, требующиеся для создания/добавления текста в систему."""

    title: TextTitle
    difficulty: Optional[TextDifficulty] = Body(default=0)
    preview: Optional[TextPreview]
    value: TextValue

    # TODO: Разработать алгоритм, позволяющий создать default factory преобразования текста в транскрипцию
    # ! Позже можно сделать Optional
    transcription: TextTranscription


class CreateLearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос добавления текста."""

    model_config = ConfigDict(from_attributes=True)

    id: TextID


class DeleteLearningTextResponse(CreateLearningTextResponse):
    """Данные, отправляемые в ответ на запрос удаления текста."""


class UpdateLearningTextRequest(BaseModel):
    """Данные, требующиеся для обновления данных о тексте."""

    title: Optional[TextTitle] = None
    difficulty: Optional[TextDifficulty] = None
    preview: Optional[TextPreview] = None
    value: Optional[TextValue] = None
    transcription: Optional[TextTranscription] = None


class UpdateLearningTextResponse(DetailLearningTextResponse):
    """Данные, отправляемые в ответ на запрос обновления данных о тексте."""
