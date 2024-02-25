from typing import Union

import bcrypt
import jwt

from app.core import auth_jwt


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    encoded = jwt.encode(
        payload=payload,
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
