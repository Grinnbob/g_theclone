from app.scripts.closecom.provider import _execute_closecom_api
from app.scripts.globals import *
from app.schemas.models.closecom.lead import CloseComLeadChangeStatus, ApiGetLeads
from app.core.config import settings
from app.services.closecom.lead_service import ClosecomLeadService
from pprint import pprint

async def show_all_status():
    settings.LOGGER.info(f"...showing lead status")

    statuses = await _execute_closecom_api("list_lead_statuses", paginate=True)
    if not statuses:
        settings.LOGGER.error(f"There is no statuses created yet")
        return None

    settings.LOGGER.info("id | label | organization_id |")
    for st in statuses:
        settings.LOGGER.info(f"{st['id']}     |  {st['label']}    |     {st['organization_id']}")

async def lead_change_status(lead_id, status):
    settings.LOGGER.info(f"...changing {lead_id} status to={status}")

    status_id = lead_status[status]
    return await  _execute_closecom_api("lead_change_status", payload=CloseComLeadChangeStatus(lead_id=lead_id,
                                                                                              status_id=status_id))

async def show_leads(once: str):
    if once == 'once':
        once = True
    else:
        once = False

    settings.LOGGER.info(f"...Show all leads once={once}")

    leads = await  _execute_closecom_api("get_all_leads",
                                            paginate=True,
                                            once=once)

    if not leads:
        settings.LOGGER.error(f"There are no leads yet")
        return None

    pprint(leads)

    settings.LOGGER.info(f"received={len(leads)}")
    return leads

async def update_leads(once: str):
    if once == 'once':
        once = True
    else:
        once = False

    settings.LOGGER.info(f"...get all leads from server and update or create in DB once={once}")

    leads = await  _execute_closecom_api("get_all_leads",
                                            paginate=True,
                                            once=once)

    if not leads:
        settings.LOGGER.error(f"There are no leads yet")
        return None

    items = []
    received = 0
    for lead in leads:

        customer = "Unknown"
        custom = lead.get("custom", {})
        if custom:
            customer = custom.get("Customer", "Unknown")
            if customer == "Unknown":
                customer = custom.get("customer", "Unknown")

        items.append(dict(lead_id=lead.get("id"),
                          status_id=lead.get("status_id", "Unknown"),
                          status_label=lead.get("status_label", "Unknown"),
                          customer=customer,
                          data=lead))
        received += 1


    service = ClosecomLeadService()

    res = await service.upsert_many(items)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
    else:
        settings.LOGGER.info("None")

    settings.LOGGER.info(f"received={received}")
    return res

