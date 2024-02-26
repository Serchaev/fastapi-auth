from fastapi import HTTPException, status
from pymongo.database import Database
from pymongo.results import UpdateResult

from app.api_v1.services import AuthService, UserService
from app.auth.utils import hash_password
from app.core.models import User


class AuthController:

    @classmethod
    async def register(cls, db: Database, new_user: dict):
        check_username = await UserService.find_one(
            db=db,
            username=new_user.get("username"),
        )
        if check_username is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username - {new_user.get('username')} already exists!",
            )
        check_email = await UserService.find_one(
            db=db,
            email=new_user.get("email"),
        )
        if check_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email - {new_user.get('email')} already exists!",
            )
        new_user["hashed_password"] = hash_password(new_user["password"])
        new_user.pop("password")
        result = await AuthService.register(
            db=db,
            new_user=User(**new_user),
        )
        inserted_user = await UserService.find_one(
            db=db,
            **{"_id": result.inserted_id},
        )
        inserted_user["_id"] = str(inserted_user["_id"])
        return inserted_user

    @classmethod
    async def activate_profile(cls, db: Database, link: str):
        user: User = await UserService.find_one(
            db=db,
            **{"profile.activation_link": link, "profile.is_activated": False},
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile with activation_link - {link} not found!",
            )
        result: UpdateResult = await UserService.update(
            db=db,
            user_id=user["_id"],
            **{"profile.is_activated": True},
        )
        if not result.acknowledged:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
