from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.api_v1.controllers import AuthController
from app.api_v1.schemas import RegisterSchemaBody
from app.core import db_factory

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register")
async def register(
    register_body: RegisterSchemaBody,
    db: Database = Depends(db_factory.session_depends),
):
    return await AuthController.register(
        db=db,
        new_user=register_body.model_dump(exclude_none=True),
    )
