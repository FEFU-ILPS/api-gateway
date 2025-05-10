from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .examples.texts import (
    ID_EXAMPLES,
    TITLE_EXAMPLES,
    TRANSCRIPTION_EXAMPLES,
    VALUE_EXAMPLES,
)

TextID = Annotated[UUID, Field(description="Уникальный идентификатор", examples=ID_EXAMPLES)]
TextTitle = Annotated[str, Field(max_length=100, description="Название", examples=TITLE_EXAMPLES)]
TextValue = Annotated[str, Field(description="Содержание", examples=VALUE_EXAMPLES)]
TextTranscription = Annotated[
    str, Field(description="Транскрипционная запись", examples=TRANSCRIPTION_EXAMPLES)
]


class LearningTextResponse(BaseModel):
    """Данные, отправляемые в ответ на запрос получения всех текстов."""

    model_config = ConfigDict(from_attributes=True)

    id: TextID
    title: TextTitle


class DetailLearningTextResponse(LearningTextResponse):
    """Данные, отправляемые в ответ на запрос получения деталей о тексте."""

    value: TextValue
    transcription: TextTranscription


class CreateLearningTextRequest(BaseModel):
    """Данные, требующиеся для создания/добавления текста в систему."""

    title: TextTitle
    value: TextValue
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
    value: Optional[TextValue] = None
    transcription: Optional[TextTranscription] = None


class UpdateLearningTextResponse(DetailLearningTextResponse):
    """Данные, отправляемые в ответ на запрос обновления данных о тексте."""
