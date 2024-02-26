from fastapi import APIRouter, status

router = APIRouter(prefix="/user", tags=["Пользователи"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_users():
    pass
