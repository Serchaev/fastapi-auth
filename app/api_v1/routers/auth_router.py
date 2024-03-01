from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from pymongo.database import Database

from app.api_v1.controllers import AuthController
from app.api_v1.schemas import (
    LoginSchemaAnswer,
    LoginSchemaBody,
    RegisterSchemaAnswer,
    RegisterSchemaBody,
)
from app.core import db_factory, settings

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    register_body: RegisterSchemaBody,
    db: Database = Depends(db_factory.session_depends),
) -> RegisterSchemaAnswer:
    return await AuthController.register(
        db=db,
        new_user=register_body.model_dump(exclude_none=True),
    )


@router.get("/activate/{link}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def activate_profile(
    link: str,
    db: Database = Depends(db_factory.session_depends),
):
    await AuthController.activate_profile(db=db, link=link)
    return RedirectResponse(settings.REDIRECT_ACTIVATE_PROFILE)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    login_data: LoginSchemaBody,
    db: Database = Depends(db_factory.session_depends),
) -> LoginSchemaAnswer:
    tokens = await AuthController.login(db=db, login_data=login_data)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
    )
    return {
        "access_token": tokens["access_token"],
        "token_type": "Bearer",
    }


async def get_refresh_from_cookie(refresh_token: str = Cookie(alias="refresh_token")):
    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found",
        )
    return refresh_token


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    refresh_token: str = Depends(get_refresh_from_cookie),
    db: Database = Depends(db_factory.session_depends),
):
    await AuthController.logout(db=db, refresh_token=refresh_token)
    response.delete_cookie("refresh_token")


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    response: Response,
    refresh_token: str = Depends(get_refresh_from_cookie),
    db: Database = Depends(db_factory.session_depends),
):
    tokens = await AuthController.refresh(db=db, refresh_token=refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
    )
    return {
        "access_token": tokens["access_token"],
        "token_type": "Bearer",
    }
