from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.database import Database

from app.core.models import User


class AuthService:

    @classmethod
    async def register(cls, db: Database, new_user: User):
        users_collection: AsyncIOMotorCollection = db.users
        result = await users_collection.insert_one(new_user.model_dump(warnings=False))
        inserted_user = await users_collection.find_one({"_id": result.inserted_id})
        inserted_user["_id"] = str(inserted_user["_id"])
        return inserted_user
