from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/")

oauth2_google_token = OAuth2()

def create_access_token(data: dict,
                        expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

