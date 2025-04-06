from pydantic import BaseModel, Field
from typing import Annotated, Optional
from uuid import UUID


class LearningTextResponse(BaseModel):
    id: Annotated[UUID, Field(..., description="Уникальный идентификатор")]
    title: Annotated[str, Field(max_length=100, description="Название")]
    difficulty: Annotated[Optional[int], Field(ge=0, le=10, description="Сложность")]
    preview: Annotated[Optional[str], Field(max_length=500, description="Краткое описание")]


class DetailLearningTextResponse(LearningTextResponse):
    value: Annotated[str, Field(..., description="Содержание")]
    transcription: Annotated[str, Field(..., description="Транскрипционная запись")]
