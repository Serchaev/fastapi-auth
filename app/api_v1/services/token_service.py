from app.auth.utils import encode_jwt
from app.core.models import User


class TokenService:

    @classmethod
    async def generate_tokens(cls, user: User):
        payload = {
            "sub": user["username"],
            "username": user["username"],
            "email": user["email"],
            "first_name": user["first_name"],
        }
        access_token = encode_jwt(payload=payload, expire_minutes=5)
        refresh_token = encode_jwt(payload=payload, expire_minutes=15)

        return {"access_token": access_token, "refresh_token": refresh_token}
