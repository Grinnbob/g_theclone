from app.core.config import settings
from app.scripts.globals import *
from app.scripts.zerobounce.provider import _execute_zerobounce_api
from app.services.closecom.contactemail_service import CloseComContactEmailService
from pprint import pprint


async def zerobounce_validate_email(email):
    settings.LOGGER.info(f"...zerobounce validating email={email}")

    res = await  _execute_zerobounce_api("validate_email", payload=email)
    if not res:
        settings.LOGGER.error(f"zerobounce_validate_email empty res={res}")

    pprint(res)

    return res

async def zerobounce_validate_batch():
    closecom_email_service = CloseComContactEmailService()

