from typing import List, Any, Optional
from fastapi import APIRouter, Body, Depends, Path, Query, Request

from app.exceptions import *
from app.api.utils import *

from app.services import account_service, user_service
from app.services.addon import template_service, test_service, sequence_service
from app.services.models.user import User

import app.schemas.models.user as user_schema
import app.schemas.models.account as account_schema
import app.schemas.models.addon.sequence as sequence_schema
import app.schemas.models.addon.template as template_schema
import app.schemas.models.addon.test as test_schema


from app.api import deps
from app.core.config import settings
from app.services.models.account import Account
from app.providers.google.gmail_api import GmailApiProvider

router = APIRouter()

#DASHBOARD routines
@router.get("/", response_model=user_schema.UserAddonProfile)
async def get_profile(
    current_account: Account = Depends(deps.get_current_active_account),
    service: account_service.AccountService = Depends(deps.get_account_service)
) -> Any:

    return hack_serialize(await service.get_addon_profile(
                                    account=current_account))

#OAUTH ROUTINES
@router.get("/oauth/start/")
async def addon_oauth_start(
    current_account: Account = Depends(deps.get_current_active_account),
    service: account_service.AccountService = Depends(deps.get_account_service)
) -> Any:
    url, state = service.oauth_start(redirect_url=settings.GOOGLE_OAUTH_ADDON_REDIRECT_URL)

    await service.update_oauth_state(current_account, state)

    return url

@router.get("/oauth/end/", status_code=200)
async def addon_oauth_end(
    request: Request,
    service: account_service.AccountService = Depends(deps.get_account_service),
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

        account = await service.get_by_state(returned_state)
        if not account:
            raise AppErrors(f"Wrong oauth state queryparams={request.query_params}")

        new_creds = await service.oauth_end(
            code=request.query_params.get('code'),
            redirect_url=settings.GOOGLE_OAUTH_ADDON_REDIRECT_URL
        )

        if not new_creds:
            raise AppErrors("Can't recieve credentials")

        api = await GmailApiProvider.create_api_provider(dict(new_creds))

        user_profile = await api.get_profile()
        if not user_profile:
            raise AppErrors("Can't get_profile")

        await service.create(
            account_schema.AccountCreate(
                email=user_profile.emailAddress,
                is_logged=1,
                credentials=dict(new_creds)
            ))

    return True


############################################################################
########################## MAJOR API #######################################
############################################################################


###################################################################################################################
            ############## TEMPLATES ##########################
@router.get("/templates/", response_model=List[template_schema.TemplateInDB])
async def list_templates(
    current_account: Account = Depends(deps.get_current_active_account),
    service: template_service.TemplateService = Depends(deps.get_template_service)
) -> Any:

    return hack_serialize(await service.get_templates(account_id=str(current_account.id)))

@router.post("/templates/", response_model=template_schema.TemplateInDB)
async def create_template(
    payload: template_schema.TemplateCreate,
    current_account: Account = Depends(deps.get_current_active_account),
    service: template_service.TemplateService = Depends(deps.get_template_service)
) -> Any:

    return hack_serialize(await service.create(payload=payload))


###################################################################################################################
                    ############## SEQUENCES ##########################
@router.post("/sequences/", response_model=sequence_schema.SequnceInDB)
async def create_sequences(
    payload: sequence_schema.SequenceCreate,
    current_account: Account = Depends(deps.get_current_active_account),
    service: sequence_service.SequenceService = Depends(deps.get_sequence_service)
) -> Any:
    return hack_serialize(await service.create(payload=payload))



###################################################################################################################
                ############## TESTS ##########################
@router.get("/tests/", response_model=List[test_schema.TestInDB])
async def list_tests(
    current_account: Account = Depends(deps.get_current_active_account),
    service: test_service.TestService = Depends(deps.get_test_service)
) -> Any:

    return hack_serialize(await service.get_test(account_id=str(current_account.id)))

#DASHBOARD routines
@router.post("/tests/", response_model=test_schema.TestInDB)
async def create_test(
    payload: test_schema.TestCreate,
    current_account: Account = Depends(deps.get_current_active_account),
    service: test_service.TestService = Depends(deps.get_test_service)
) -> Any:
    return hack_serialize(await service.create(payload=payload))

