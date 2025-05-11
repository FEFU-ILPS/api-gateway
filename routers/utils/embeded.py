from typing import Generic, TypeVar, Any

from pydantic import BaseModel, Field

M = TypeVar("M", bound=BaseModel)


class Embeded(BaseModel):
    """Класс Query параметров, необходимых для указания расширения запроса"""

    embed: str = Field(description="Список сущностей для расширения запроса", default="")

    def get_entities(self) -> list[str]:
        """Возвращает распаршеный список сущностей для расширение запроса.

        Returns:
            list[str]: Список сущностей.
        """
        return [entity.strip() for entity in self.embed.split(",")]


class EmbededResponse(BaseModel, Generic[M]):
    """Класс ответа с расширением."""

    item: M = Field(description="Целевой объект")
    embeded: dict[str, dict[str, Any]] = Field(description="Расширение запроса", default={})
