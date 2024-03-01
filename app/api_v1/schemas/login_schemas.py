from pydantic import BaseModel


class LoginSchemaBody(BaseModel):
    login: str
    password: str


class LoginSchemaAnswer(BaseModel):
    access_token: str
    token_type: str
