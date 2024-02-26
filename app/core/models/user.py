from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    is_activated: bool = False
    activation_link: str = str(uuid4())


class User(BaseModel):
    username: str
    hashed_password: bytes
    email: EmailStr
    first_name: str
    last_name: Optional[str] = None
    created_at: str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    profile: Profile = Profile()
