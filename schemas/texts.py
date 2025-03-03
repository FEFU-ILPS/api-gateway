from pydantic import BaseModel, Field
from typing import Annotated


class TextResponse(BaseModel):
    title: Annotated[str, Field(...)]
