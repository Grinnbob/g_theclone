from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from .base import BaseService
import app.schemas.models.account as account_schema
from .models.account import Account
from .models.user import User
from aiogoogle import Aiogoogle
from aiogoogle.auth.utils import create_secret
from app.core.config import settings
from app.providers.google.utills import build_client_creds, build_aiogoogle
from bson.objectid import ObjectId
from aiogoogle.auth.creds import UserCreds, ClientCreds
from app.schemas.models.user import UserAddonProfile

class AccountService(BaseService[Account, account_schema.AccountCreate, account_schema.AccountUpdate]):
    def __init__(self):
        super().__init__(model=Account)

    def oauth_start(self,
                    redirect_url: str) -> tuple:

        state =  create_secret()

        client_creds, aiogoogle = build_aiogoogle(redirect_url)

        include_granted_scopes = True
        if settings.GOOGLE_CLIENT_SETTINGS['gmail_include_granted_scopes'] != 'true':
            include_granted_scopes = False

        url = aiogoogle.oauth2.authorization_url(
            client_creds=client_creds,
            state=state,
            access_type=settings.GOOGLE_CLIENT_SETTINGS['gmail_access_type'],
            include_granted_scopes=include_granted_scopes,
            login_hint='client email',
            prompt='consent'
        )

        return (url, state)


    async def oauth_end(self,
                        code:str,
                        redirect_url=None) -> Any:

        client_creds, aiogoogle = build_aiogoogle(redirect_url=redirect_url)

        return await aiogoogle.oauth2.build_user_creds(
            grant = code,
            client_creds = client_creds
        )


    async def update_oauth_state(self,
                                 account: Account,
                                 state: str) -> Any:
        if not state:
            raise AppErrors("State can't be empty")

        account.oauth_state = state

        await account.commit()
        await account.reload()

        return account


    async def get_by_state(self,
                           state:str) -> Account:
        if not state:
            raise AppErrors("State can't be empty")

        return await Account.find_one({'oauth_state': state})


    async def create(self,
                     obj_in:account_schema.AccountCreate,) -> Account:

        exist = await Account.find_one({'email' : obj_in.email})
        if not exist:
            data = obj_in.dict(exclude_unset=True)
            exist = Account(**data)
        else:
            exist.is_logged = obj_in.is_logged
            exist.credentials = obj_in.credentials

        await exist.commit()
        await exist.reload()

        return exist

    async def get_by_email(self,
                           email: str) -> Account:
        if not email:
            return None

        return await Account.find_one({'email' : email})

    async def get_addon_profile(self,
                                account: Account) -> Any:
        profile = UserAddonProfile()
        profile.is_logged = account.is_logged

        if account.owner_id:
            user = await User.find_one({'_id' : account.owner_id})
            if user:
                profile.level = user.custom_info.get('level', 0)
                profile.stats = user.custom_info.get('stats', {})
                profile.tests = user.custom_info.get('tests', {})

        return profile

    async def get_or_create(self,
                            idinfo: dict) -> Any:

        email = idinfo.get('email')
        if not email:
            return None

        exist = await Account.find_one({'email' : email})
        if not exist:
            exist = Account(email=email,
                            profile=idinfo)

            await exist.commit()
            await exist.reload()

        return exist