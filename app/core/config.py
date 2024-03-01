from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import MongoClient

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR.joinpath("certs/jwt-private.pem")
    public_key_path: Path = BASE_DIR.joinpath("certs/jwt-public.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 2 * 60


class DatabaseFactory:

    async def session_depends(self):
        client = AsyncIOMotorClient(self.db_url)
        try:
            yield client.get_database()
        except:  # noqa
            client.close()

    def generate_indexes(self):
        client = MongoClient(self.db_url)
        db = client.get_database()
        users = db.users
        users.create_index([("username", 1)], unique=True)
        users.create_index([("email", 1)], unique=True)
        client.close()

    def __init__(self, db_url: str):
        self.db_url = db_url
        self.generate_indexes()
