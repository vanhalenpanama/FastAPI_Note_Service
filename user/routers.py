from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from auth import get_current_user, create_access_token, Role, CurrentUser
from .schemas import UserCreate, UserUpdate, UserResponse, Token
from .crud import UserService, get_user_service

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    try:
        user = user_service.get_user_by_email(email=form_data.username)
        if not user_service.crypto.verify(form_data.password, user.password):
            raise HTTPException(status_code=401)
        access_token = create_access_token(payload={"sub": user.email, "id": user.id}, role=Role.USER)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_user_by_id(user_id=current_user.id)
   # return user_service.get_user_by_email(email=current_user.id)


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    user_create: UserCreate, user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(
        name=user_create.name,
        email=user_create.email,
        password=user_create.password,
        memo=user_create.memo,
    )


@router.get("", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.get_user_by_id(user_id=current_user.id)

    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return user_service.get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    # user = user_service.get_user_by_email(email=current_user.id)
    user = user_service.get_user_by_id(user_id=current_user.id)

    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user_service.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
   # user = user_service.get_user_by_email(email=current_user.id)
    user = user_service.get_user_by_id(user_id=current_user.id)

    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    user_service.delete_user(user_id)
