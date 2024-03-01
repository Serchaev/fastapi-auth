from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.database import Database

from app.core.models import User, Token


class AuthService:

    @classmethod
    async def register(cls, db: Database, new_user: User):
        users_collection: AsyncIOMotorCollection = db.users
        return await users_collection.insert_one(new_user.model_dump())

    @classmethod
    async def token_save(cls, db: Database, token: Token):
        tokens_collection: AsyncIOMotorCollection = db.tokens
        return await tokens_collection.insert_one(token.model_dump())
