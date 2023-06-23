from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException, status
from jose import jwt


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')
JWT_SECRET = config('JWT_SECRET')


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
