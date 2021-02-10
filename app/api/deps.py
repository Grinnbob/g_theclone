from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from app.services import user_service, account_service, list_service, form_service, admin_dashboard_service
from app.services.addon import template_service, sequence_service, test_service
from app.services.models.user import User
from app.services.models.account import Account
from .auth import oauth2_scheme, oauth2_google_token
from app.schemas.auth import Token, TokenData
from jose import JWTError, jwt
from app.core.config import settings

async def get_user_service():
    return user_service.UserService()

async def get_list_service():
    return list_service.ListService()

async def get_form_service():
    return form_service.FormService()

async def get_account_service():
    return account_service.AccountService()

async def get_admin_service():
    return admin_dashboard_service.AdminDashboardService()

async def get_template_service():
    return template_service.TemplateService()

async def get_sequence_service():
    return sequence_service.SequenceService()

async def get_test_service():
    return test_service.TestService()



async def get_current_user(token: str = Depends(oauth2_scheme),
                           user_service: user_service.UserService = Depends(get_user_service)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await user_service.get_by_id(user_id=token_data.username)
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_active_admin_user(active_user: User = Depends(get_current_active_user)):
    if active_user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not an admin")

    return active_user


################################################################################################################
############### AUTH methods for /addons requests ##############################################################
################################################################################################################
from google.oauth2 import id_token
from google.auth.transport import requests

async def get_current_account(token: str = Depends(oauth2_google_token),
                              account_service: account_service.AccountService = Depends(get_account_service)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or user doesn't exist",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.ADDON_CLIENT_ID)
        idinfo = id_token.verify_token(token, requests.Request())

        user_email = idinfo.get('email')
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    account = await account_service.get_or_create(idinfo=idinfo)
    if account is None:
        raise credentials_exception

    return account


async def get_current_active_account(current_account: Account = Depends(get_current_account)):
    if not current_account.active:
        raise HTTPException(status_code=400, detail="Inactive account")

    return current_account
