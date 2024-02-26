from typing import Optional

from pydantic import BaseModel, EmailStr, constr, Field


class RegisterSchema(BaseModel):
    username: constr(min_length=3, max_length=20)
    password: constr(min_length=8, max_length=20)
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None


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
