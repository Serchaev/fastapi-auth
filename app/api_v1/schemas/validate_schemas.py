from pydantic import BaseModel


class ValidateSchemaAnswer(BaseModel):
    sub: str
    username: str
    email: str
    first_name: str
    active: bool
