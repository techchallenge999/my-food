from datetime import datetime, timedelta
from typing import Annotated
from dataclasses import dataclass
from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.infrastructure.postgresql.models.user import pwd_context
from src.use_cases.user.find.find_user_dto import FindUserByCpfOutputDto


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
JWT_SECRET = config("JWT_SECRET")

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@dataclass
class EmptyUser:
    uuid: str | None = None


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user: FindUserByCpfOutputDto | None,
):
    try:
        payload = decode_access_token(token)
        username: str = payload["sub"]
        if username is None:
            raise_credentials_exception("Could not validate credentials")
    except JWTError:
        raise_credentials_exception("Could not validate credentials")
    if user is None:
        raise_credentials_exception("Could not validate credentials")
    return user


async def get_current_user_optional(
    token: Annotated[str | None, Depends(oauth2_scheme_optional)],
    user: FindUserByCpfOutputDto | None,
):
    try:
        if token is None:
            return EmptyUser()
        payload = decode_access_token(token)
        username: str = payload["sub"]
        if username is None:
            return EmptyUser()
    except JWTError:
        return EmptyUser()
    if user is None:
        raise_credentials_exception("Could not validate credentials")
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    return payload


def raise_credentials_exception(detail: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
