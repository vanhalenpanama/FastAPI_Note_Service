from datetime import datetime, timedelta
from enum import StrEnum
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic_settings import BaseSettings
from dataclasses import dataclass


class Settings(BaseSettings):
    JWT_SECRET: str = "your-secret-key-for-jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 6

    class Config:
        env_file = ".env"


settings = Settings()


class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


def create_access_token(
    payload: dict,
    role: Role,
    expires_delta: timedelta = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
):
    expire = datetime.utcnow() + expires_delta
    payload.update(
        {
            "role": role,
            "exp": expire,
        }
    )
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@dataclass
class CurrentUser:
    id: str
    email: str
    role: Role

    def __str__(self):
        return f"{self.id}({self.role})"


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    payload = decode_access_token(token)
    email = payload.get("sub")
    id = payload.get("id")
    role = payload.get("role", Role.USER)

   #if not email:
    if not email or id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return CurrentUser(id, email, Role(role))


def get_admin_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    payload = decode_access_token(token)
    role = payload.get("role")

    if not role or role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser("ADMIN_USER_ID", Role(role))
