from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    hashed_password: bytes
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    created_at: datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    is_confirm: bool = False
