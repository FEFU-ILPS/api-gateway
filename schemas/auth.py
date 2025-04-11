import re
from typing import Annotated
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, Field, field_validator

UserID = Annotated[UUID, Field(..., examples=["16fd2706-8baf-433b-82eb-8c7fada847da"])]
UserName = Annotated[str, Body(max_length=255, examples=["nagibator_rus"])]
UserEmail = Annotated[str, Body(max_length=40, min_length=8, examples=["!Password123"])]
UserPassword = Annotated[str, Body(max_length=40, min_length=8, examples=["!Password123"])]
JWTAccessToken = Annotated[str, Field(...)]
JWTTokenType = Annotated[str, Field(default="Bearer")]
Flag = Annotated[bool, Field(..., examples=["False"])]


class AuthenticateUserRequest(BaseModel):
    username: UserName
    password: UserPassword


class AuthenticateUserResponse(BaseModel):
    access_token: JWTAccessToken
    token_type: JWTTokenType


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
    is_admin: Flag
