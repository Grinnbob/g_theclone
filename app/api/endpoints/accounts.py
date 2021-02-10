from typing import List, Any, Optional
from fastapi import APIRouter, Body, Depends, Path, Query, Request

from app.exceptions import *
from app.api.utils import *

from app.services import account_service, user_service
from app.services.models.user import User

import app.schemas.models.account as account_schema
import app.schemas.google.gmail_api as gmail_schemas

from app.api import deps
from app.core.config import settings
from app.services.models.account import Account
from app.providers.google.gmail_api import GmailApiProvider

router = APIRouter()

#DASHBOARD routines
@router.get("/list/labels/")
async def list_labels(
    account_id: str,
    current_user: User = Depends(deps.get_current_active_user),
    service: account_service.AccountService = Depends(deps.get_account_service)
) -> Any:

    account = await service.get(id=account_id,
                                owner_id=current_user.id)
    if not account:
        raise AppErrors(f"Account {account_id} not found")

    api = await GmailApiProvider.create_api_provider(user_creds=account.credentials)

    return await api.list_labels()

@router.get("/list/", response_model=List[account_schema.AccountInDB])
async def list_accounts(
    page: int = 0,
    current_user: User = Depends(deps.get_current_active_user),
    service: account_service.AccountService = Depends(deps.get_account_service)
) -> Any:

    skip, limit = page_to_raw(page)
    return hack_serialize(await service.get_multi(owner_id=current_user.id,
                                    skip=skip,
                                    limit=limit))

#DASHBOARD routines
@router.get("/", response_model=account_schema.AccountInDB)
async def get_account(
    id:str,
    current_user: User = Depends(deps.get_current_active_user),
    service: account_service.AccountService = Depends(deps.get_account_service)
) -> Any:

    return hack_serialize(await service.get(
                                    id=id,
                                    owner_id=current_user.id))

@router.delete("/")
async def remove_account(
    id:str,
    current_user: User = Depends(deps.get_current_active_user),
    service: account_service.AccountService = Depends(deps.get_account_service)
) -> Any:

    return await service.remove(id=id,
                                owner_id=current_user.id)

#OAUTH ROUTINES
@router.get("/oauth/start/")
async def oauth_start(
    current_user: User = Depends(deps.get_current_active_user),
    service: account_service.AccountService = Depends(deps.get_account_service),
    user_service: user_service.UserService = Depends(deps.get_user_service)
) -> Any:
    url, state = service.oauth_start()

    await user_service.update_oauth_state(current_user, state)

    return url

@router.get("/oauth/end/", status_code=200)
async def oauth_end(
    request: Request,
    service: account_service.AccountService = Depends(deps.get_account_service),
    user_service: user_service.UserService = Depends(deps.get_user_service)
) -> Any:
    if request.query_params.get('error'):
        error = {
            'error': request.query_params.get('error'),
            'error_description': request.query_params.get('error_description')
        }
        return error
    elif request.query_params.get('code'):
        returned_state = request.query_params.get('state')
        if not returned_state:
            raise AppErrors(f"Wrong returned_state queryparams={request.query_params}")

        user = await user_service.get_by_state(returned_state)
        if not user:
            raise AppErrors(f"Wrong oauth state queryparams={request.query_params}")

        new_creds = await service.oauth_end(
            code=request.query_params.get('code')
        )

        if not new_creds:
            raise AppErrors("Can't recieve credentials")

        api = await GmailApiProvider.create_api_provider(dict(new_creds))

        user_profile = await api.get_profile()
        if not user_profile:
            raise AppErrors("Can't get_profile")

        await service.create(
            account_schema.AccountCreate(
                owner_id=user.id,
                email=user_profile.emailAddress,
                is_logged=1,
                credentials=dict(new_creds)
            ))

    return True


