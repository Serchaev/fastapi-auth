from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class RegisterSchema(BaseModel):
    username: constr(min_length=3, max_length=20)
    password: constr(min_length=8, max_length=20)
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None


class RegisterSchemaBody(RegisterSchema):
    pass
