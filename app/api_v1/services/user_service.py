from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.database import Database


class UserService:

    @classmethod
    async def find_one(cls, db: Database, **data):
        users_collection: AsyncIOMotorCollection = db.users
        return await users_collection.find_one(data)
