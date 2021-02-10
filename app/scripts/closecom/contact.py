from app.scripts.closecom.provider import _execute_closecom_api
from app.scripts.globals import *
from app.core.config import settings
from app.services.closecom.pagination_service import CloseComPaginationService
from app.services.closecom.contactemail_service import CloseComContactEmailService
from app.schemas.models.closecom.contactemail import ApiContactsGet
from pprint import pprint

ENDPOINT = 'contact'

async def show_contacts(once: str):
    if once == 'once':
        once = True
    else:
        once = False

    settings.LOGGER.info(f"...show all contacts from server and update or create in DB ONCE={once}")

    #NOT WORKING
    #pagination_service = CloseComPaginationService()
    #next_page = await pagination_service.get_page(endpoint=ENDPOINT)
    #payload = ApiContactsGet(skip=next_page._skip)
    #settings.LOGGER.info(f"...calling API next_page._skip={next_page._skip} payload._skip={payload.skip}")

    payload = ApiContactsGet(skip=0)
    contacts = await  _execute_closecom_api("get_contacts",
                                            payload=payload,
                                            paginate=True,
                                            once=once)
    if not contacts:
        settings.LOGGER.error(f"There is no contacts yet")
        return None

    pprint(contacts)
    print(f"....total received={len(contacts)} once={once} _skip={next_page._skip}")
    return contacts


async def update_contacts(once: str):
    if once == 'once':
        once = True
    else:
        once = False

    settings.LOGGER.info(f"...get all contacts from server and update or create in DB once={once}")

    #pagination_service = CloseComPaginationService()
    #next_page = await pagination_service.get_page(endpoint=ENDPOINT)
    #payload = ApiContactsGet(skip=next_page._skip)
    #settings.LOGGER.info(f"...calling API next_page._skip={next_page._skip} payload._skip={payload.skip}")

    payload = ApiContactsGet(skip=0)
    contacts = await  _execute_closecom_api("get_contacts",
                                            payload=payload,
                                            paginate=True,
                                            once=once)

    if not contacts:
        settings.LOGGER.error(f"There is no contacts yet")
        return None

    items = []
    received = 0
    emails_count = 0
    for contact in contacts:
        emails = contact.get('emails', [])
        if emails:
            for n in emails:
                email = n.get('email', None)
                if email:
                    items.append(dict(email=email,
                                      data=contact))
                    emails_count += 1

        received += 1


    service = CloseComContactEmailService()

    res = await service.upsert_many(items)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
    else:
        settings.LOGGER.info("None")

    #update paging
    #await pagination_service.update_page(endpoint=ENDPOINT,
    #                                     received=received)

    settings.LOGGER.info(f"received={received} emails_count={emails_count}")
    return res
