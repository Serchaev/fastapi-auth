import re
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, Field, validator, field_validator


class RegisterSchema(BaseModel):
    username: constr(min_length=3, max_length=20)
    password: constr(min_length=8, max_length=20)
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None

    @field_validator("username")
    def validate_username(cls, v):
        pattern = r"^[a-zA-Z0-9_]+$"  # Регулярное выражение, которое разрешает только буквы, цифры и нижнее подчеркивание
        if not re.match(pattern, v):
            raise ValueError(
                "Username can contain only letters, numbers and underscores."
            )
        return v


class RegisterSchemaBody(RegisterSchema):
    pass


class RegisterSchemaAnswer(BaseModel):
    id: str = Field(alias="_id")
    username: str
    hashed_password: str
    email: str
    first_name: str
    last_name: Optional[str]
    created_at: str
