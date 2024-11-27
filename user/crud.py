from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ulid import ULID
from main import SessionLocal, Crypto
from .models import UserModel
from .schemas import UserUpdate


class UserService:
    def __init__(self):
        self.crypto = Crypto()

    def save(self, user: UserModel):
        with SessionLocal() as db:
            try:
                db.add(user)
                db.commit()
                db.refresh(user)
            except IntegrityError:
                db.rollback()
                raise HTTPException(status_code=409, detail="User already exists")

    def create_user(
        self, name: str, email: str, password: str, memo: Optional[str] = None
    ):
        now = datetime.utcnow()
        user = UserModel(
            id=str(ULID()),
            name=name,
            email=email,
            password=self.crypto.encrypt(password),
            memo=memo,
            created_at=now,
            updated_at=now,
        )
        self.save(user)
        return user

    def get_user_by_id(self, user_id: str) -> UserModel:
        with SessionLocal() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

    def get_user_by_email(self, email: str) -> UserModel:
        with SessionLocal() as db:
            user = db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user

    def get_users(self, skip: int = 0, limit: int = 20) -> List[UserModel]:
        with SessionLocal() as db:
            return db.query(UserModel).offset(skip).limit(limit).all()

    def update_user(self, user_id: str, user_update: UserUpdate) -> UserModel:
        with SessionLocal() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if field == "password":
                    value = self.crypto.encrypt(value)
                setattr(user, field, value)

            user.updated_at = datetime.utcnow()
            try:
                db.commit()
                db.refresh(user)
            except IntegrityError:
                db.rollback()
                raise HTTPException(status_code=409, detail="Email already exists")
            return user

    def delete_user(self, user_id: str):
        with SessionLocal() as db:
            user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            db.delete(user)
            db.commit()
            return True


def get_user_service():
    return UserService()
