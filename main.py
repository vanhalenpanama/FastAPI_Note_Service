from datetime import datetime
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic_settings import BaseSettings
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Crypto:
    def __init__(self):
        self.pwd_context = PasswordHasher()

    def encrypt(self, secret: str) -> str:
        return self.pwd_context.hash(secret)

    def verify(self, secret: str, hash: str) -> bool:
        try:
            return self.pwd_context.verify(hash, secret)
        except VerifyMismatchError:
            return False


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5438"
    DB_NAME: str = "DB_NAME"
    DB_USER: str = "DB_USER"
    DB_PASSWORD: str = "DB_PASSWORD"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()
engine = create_engine(settings.DATABASE_URL)
# Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# FastAPI 앱 및 라우터
app = FastAPI()


# 라우터 등록
from user.routers import router as user_router
from note.routers import router as note_router

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(note_router, prefix="/notes", tags=["notes"])
