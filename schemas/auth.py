from pydantic import BaseModel, Field
from typing import Annotated


class AuthRequest(BaseModel):
    username: Annotated[str, Field(...)]
    passwords: Annotated[str, Field(...)]


class AuthResponse(BaseModel):
    access_token: Annotated[str, Field(...)]
