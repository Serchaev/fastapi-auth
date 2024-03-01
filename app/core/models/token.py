from bson import ObjectId
from pydantic import BaseModel


class Token(BaseModel):
    user_id: ObjectId
    refresh_token: str

    class Config:
        arbitrary_types_allowed = True
