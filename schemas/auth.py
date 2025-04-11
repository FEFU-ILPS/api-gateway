import re
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from .examples.auth import (
    EMAIL_EXAMPLES,
    FLAG_EXAMPLES,
    ID_EXAMPLES,
    JWT_ACCESS_TOKEN_EXAMPLES,
    JWT_TOKEN_TYPE_EXAMPLES,
    NAME_EXAMPLES,
    PASSWORD_EXAMPLES,
)

Flag = Annotated[bool, Field(examples=FLAG_EXAMPLES)]
UserID = Annotated[UUID, Field(description="Идентификатор пользователя", examples=ID_EXAMPLES)]
UserName = Annotated[
    str,
    Field(description="Имя пользователя", max_length=255, examples=NAME_EXAMPLES),
]
UserEmail = Annotated[
    str,
    Field(description="Почта пользователя", max_length=40, min_length=8, examples=EMAIL_EXAMPLES),
]
UserPassword = Annotated[
    str,
    Field(
        description="Пароль пользователя", max_length=40, min_length=8, examples=PASSWORD_EXAMPLES
    ),
]
JWTAccessToken = Annotated[
    str, Field(description="Токен доступа", examples=JWT_ACCESS_TOKEN_EXAMPLES)
]
JWTTokenType = Annotated[
    str, Field(description="Тип токена доступа", examples=JWT_TOKEN_TYPE_EXAMPLES)
]


class AuthenticateUserRequest(BaseModel):
    username: UserName
    password: UserPassword


class AuthenticateUserResponse(BaseModel):
    access_token: JWTAccessToken
    token_type: JWTTokenType = Field(default="Bearer")


class RegisterUserRequest(BaseModel):
    name: UserName
    email: UserEmail
    password: UserPassword

    @field_validator("email")
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Password must contain at least one special character")

        return value


class RegisterUserResponse(BaseModel):
    id: UserID
    name: UserName


class AuthorizedUser(BaseModel):
    id: UserID
    name: UserName
    is_admin: Flag = Field(description="Флаг прав адиминистрирования")
