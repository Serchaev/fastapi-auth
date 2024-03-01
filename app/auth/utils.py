from datetime import datetime, timedelta
from typing import Union

import bcrypt
import jwt

from app.core import auth_jwt


def encode_jwt(
    payload: dict,
    expire_minutes: int,
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: Union[str, bytes],
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password=password.encode("utf-8"),
        salt=bcrypt.gensalt(),
    )


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password,
    )
