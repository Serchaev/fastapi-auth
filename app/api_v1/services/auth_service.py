from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.database import Database

from app.core.models import User


class AuthService:

    @classmethod
    async def register(cls, db: Database, new_user: User):
        users_collection: AsyncIOMotorCollection = db.users
        return await users_collection.insert_one(new_user.model_dump())

    @classmethod
    async def activate_profile(cls, db: Database, link: str):
        pass
