from app.scripts.closecom.provider import _execute_closecom_api
from pprint import pprint
from app.core.config import settings
from app.schemas.models.closecom.activity import ApiEmailThread, ApiEmail
from app.schemas.models.closecom.emailactivity import CloseComEmailActivityCreate
from app.services.closecom.emailactivity_service import ClosecomEmailActivityService

async def show_activities():
    settings.LOGGER.info("...showing all sequences")

    activities = await  _execute_closecom_api("list_activities")
    if not activities:
        settings.LOGGER.error(f"There is no activities created yet")
        return None

    settings.LOGGER.debug(activities)

async def show_emails(date_from, date_to, once: str):
    if once == 'once':
        once = True
    else:
        once = False

    settings.LOGGER.info("...showing all emails activities")

    payload = ApiEmail(date_created__gt=date_from,
                             date_created__lt=date_to)

    activities = await  _execute_closecom_api("list_emails",
                                              payload=payload,
                                              paginate=True,
                                              once=once)
    if not activities:
        settings.LOGGER.error(f"There is no emails created yet")
        return None

    pprint(activities)

    stats = {}
    for act in activities:
        thread_id = act.get("thread_id")
        if not stats.get(thread_id, None):
            stats[thread_id] = []

        envelope = act.get("envelope")

        from_email = envelope.get("from")[0].get("email")
        to_email = envelope.get("to")[0].get("email")

        stats[thread_id].append({
            'contact_id' : act.get("contact_id"),
            'direction' : act.get("direction"),
            'has_reply' : act.get("has_reply"),
            'lead_id' : act.get("lead_id"),
            'opens' : act.get("opens"),
            'sender' : act.get("sender"),
            'receiver' : act.get("to"),
            'from_email' : from_email,
            'to_email' : to_email,
            'sequence_id' : act.get("sequence_id"),
            'sequence_name' : act.get("sequence_name"),
            'status' : act.get("status"),
            'subject' : act.get("subject"),
            'is_autoreply' : envelope.get("is_autoreply"),
            'template_id' : act.get("template_id"),
            'template_name' : act.get("template_name")
        })

async def update_emails(date_from, date_to, once: str):
    if once == 'once':
        once = True
    else:
        once = False

    settings.LOGGER.info("...updating all emails activities in DB")

    payload = ApiEmail(date_created__gt=date_from,
                             date_created__lt=date_to)

    activities = await  _execute_closecom_api("list_emails",
                                              payload=payload,
                                              paginate=True,
                                              once=once)
    if not activities:
        settings.LOGGER.error(f"There is no emails created yet")
        return None

    items = []
    for act in activities:
        thread_id = act.get("thread_id", "")
        envelope = act.get("envelope")
        from_email = envelope.get("from")[0].get("email")
        to_email = envelope.get("to")[0].get("email")

        items.append(CloseComEmailActivityCreate(
            activity_id=act.get("id"),
            thread_id=thread_id,
            from_email=from_email,
            to_email=to_email,
            direction=act.get("direction"),
            data=act
        ))

    service = ClosecomEmailActivityService()

    res = await service.upsert_many(items)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
    else:
        settings.LOGGER.info("None")

    settings.LOGGER.info(f"received={len(items)}")
    return res


async def show_email_threads(date_from, date_to, once: str):
    if once == 'once':
        once = True
    else:
        once = False

    settings.LOGGER.info("...showing all email threads")

    payload = ApiEmailThread(date_created__gt=date_from,
                             date_created__lt=date_to)

    activities = await  _execute_closecom_api("list_email_threads",
                                              payload=payload,
                                              paginate=True,
                                              once=once)
    if not activities:
        settings.LOGGER.error(f"There is no email threads created yet")
        return None

    for act in activities:
        emails = act.get("latest_emails", None)
        if not emails:
            emails = act.get("emails", None)

        if not emails:
            settings.LOGGER.info(f"NO EMAILS for thread id={act.get('id', 'NO_ID')}")
            continue

        participants = act.get("participants")
        latest_normalized_subject = act.get("latest_normalized_subject")
        settings.LOGGER.info(f"THREAD subject={latest_normalized_subject} with={participants}")
        for email in emails:
            status = email.get("status")
            direction = email.get("direction")
            subject = email.get("subject")
            opens_summary = email.get("opens_summary")
            sender = email.get("sender")
            to = email.get("to")
            settings.LOGGER.info(f"....{direction}-{status}: from={sender} to={to} {subject} {opens_summary}")




