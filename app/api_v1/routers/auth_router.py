from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from pymongo.database import Database

from app.api_v1.controllers import AuthController
from app.api_v1.schemas import RegisterSchemaBody
from app.api_v1.schemas.register_schemas import RegisterSchemaAnswer
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
    link,
    db: Database = Depends(db_factory.session_depends),
):
    await AuthController.activate_profile(db=db, link=link)
    return RedirectResponse(settings.REDIRECT_ACTIVATE_PROFILE)
