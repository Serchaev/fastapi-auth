from fastapi import HTTPException, status
from pymongo.database import Database
from pymongo.results import UpdateResult

from app.api_v1.schemas import LoginSchemaBody
from app.api_v1.services import AuthService, TokenService, UserService
from app.auth.utils import hash_password, validate_password
from app.core.models import Token, User
from app.tasks import activate_account


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
        activate_account.delay(
            email=inserted_user["email"],
            link=inserted_user["profile"]["activation_link"],
        )
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

    @classmethod
    async def login(cls, db: Database, login_data: LoginSchemaBody):
        data = {"username": str(login_data.login)}
        if "@" in login_data.login:
            data["email"] = data.pop("username")
        find_user = await UserService.find_one(
            db=db,
            **data,
        )
        print(find_user)
        if find_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or password.",
            )
        if not validate_password(login_data.password, find_user.get("hashed_password")):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or password.",
            )
        tokens = await TokenService.generate_tokens(find_user)
        await AuthService.token_save(
            db=db,
            token=Token(
                refresh_token=tokens["refresh_token"],
                user_id=find_user["_id"],
            ),
        )
        return tokens

    @classmethod
    async def logout(cls, db: Database, refresh_token: str):
        result = await AuthService.logout(db=db, refresh_token=refresh_token)
        if not result.acknowledged:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    async def refresh(cls, db: Database, refresh_token: str):
        await cls.logout(db=db, refresh_token=refresh_token)
        payload = await TokenService.validate_token(token=refresh_token)
        find_user = await UserService.find_one(
            db=db,
            username=payload["username"],
        )
        tokens = await TokenService.generate_tokens(find_user)
        await AuthService.token_save(
            db=db,
            token=Token(
                refresh_token=tokens["refresh_token"],
                user_id=find_user["_id"],
            ),
        )
        return tokens
