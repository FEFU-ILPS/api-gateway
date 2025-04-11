from datetime import date, datetime
from enum import Enum
from typing import Annotated, Generic, Optional, TypeVar, Union

from fastapi import Query
from pydantic import BaseModel, field_validator

# SearchFields
_SF = TypeVar("_SF", bound=Union[str, Enum])
# OrderingFeilds
_OF = TypeVar("_OF", bound=Union[str, Enum])


class SortOrder(str, Enum):
    """Перечисление доступных режимов сортировки."""

    ASC = "asc"
    DESC = "desc"


class SearchMode(str, Enum):
    """Перечисление доступных режимов поиска."""

    SIMMILAR = "simmilar"
    EQ = "equal"
    LT = "less_than"
    GT = "greater_than"
    LTE = "less_than_or_equal"
    GTE = "greater_than_or_equal"

    def get_operator(self) -> str:
        """Ввозвращает строку с оператором, в зависимости от режима поиска."""
        return {
            SearchMode.SIMMILAR: "ILIKE",
            SearchMode.EQ: "=",
            SearchMode.LT: "<",
            SearchMode.GT: ">",
            SearchMode.LTE: "<=",
            SearchMode.GTE: ">=",
        }[self]


class ListingPagination(BaseModel):
    """Предоставляет группу query-параметров для пагинации в листинге."""

    skip: Annotated[int, Query(0, ge=0, example=0, description="Skipping entries")]
    limit: Annotated[int, Query(50, le=200, example=50, description="Total entries")]


class ListingSearch(BaseModel, Generic[_SF]):
    """Предоставляет группу query-параметров для поиска в листинге."""

    search_by: Annotated[Optional[_SF], Query(None, description="Search field")]
    search_mode: Annotated[SearchMode, Query(SearchMode.EQ, description="Search Mode")]
    search_value: Annotated[
        Optional[Union[str, int, float, date]], Query(None, description="Search value")
    ]

    @field_validator("search_value")
    def cast_search_value(cls, v):
        """Пытается привести поле к одному из ожидаемых типов."""
        if isinstance(v, str):
            if v.isdigit():
                return int(v)

            try:
                return float(v)
            except ValueError:
                try:
                    return datetime.strptime(v, "%Y-%m-%d").date()
                except ValueError:
                    return v

        return v


class ListingSort(BaseModel, Generic[_OF]):
    """Предоставляет группу query-параметров для сортировки в листинге."""

    sort_by: Annotated[Optional[_OF], Query(None, description="Sorting field")]
    sort_order: Annotated[SortOrder, Query(SortOrder.ASC, description="Sorting order")]
