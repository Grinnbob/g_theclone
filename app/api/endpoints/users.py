from typing import List, Any
from fastapi import APIRouter, Body, Depends, Path, Query, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from app.exceptions import *
from app.services import user_service
import app.schemas.models.user as user_schema
from app.schemas.auth import Token
from app.api import deps
from app.core.config import settings
from app.services.models.user import User
from app.api.auth import create_access_token
from app.api.utils import *

router = APIRouter()

@router.post("/token/", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: user_service.UserService = Depends(deps.get_user_service)
) -> Any:
    obj_in = user_schema.UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    user = await service.authenticate(obj_in=obj_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register/", response_model=user_schema.UserInDB)
async def register_user(
    payload: user_schema.UserRegister,
    service: user_service.UserService = Depends(deps.get_user_service)
) -> User:
    res = await service.create(obj_in=payload)
    return hack_serialize(res)


@router.get("/profile/", response_model=user_schema.UserInDB)
async def get_user(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return hack_serialize(current_user)