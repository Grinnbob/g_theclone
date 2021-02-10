from app.scripts.closecom.provider import _execute_closecom_api
from app.services.closecom.dailylaunch_service import ClosecomDailyLaunchService
from app.services.closecom.subscription_service import ClosecomSubscriptionService
from app.services.closecom.sequence_service import CloseComSequenceService
from app.services.closecom.account_service import ClosecomAccountService

from app.schemas.models.closecom.dailylaunch import *
from app.exceptions import *
from app.scripts.globals import *
from app.core.config import settings

async def show_smartviews(raw=False):
    settings.LOGGER.info("...showing all show_smartviews")

    smartviews = await  _execute_closecom_api("list_smartviews", paginate=True)
    if not smartviews:
        settings.LOGGER.error(f"There is no smartviews created yet")
        return None

    settings.LOGGER.info("id | name | query |")
    for sq in smartviews:
        settings.LOGGER.info(f"{sq['id']}      | {sq['name']}      | {sq['query']}")



    settings.LOGGER.debug(smartviews)

    return smartviews

async def update_smartviews():
    settings.LOGGER.info("...get all update_smartviews from server and update or create in DB")

    smartviews = await  _execute_closecom_api("list_smartviews", paginate=True)
    if not smartviews:
        settings.LOGGER.error(f"There is no smartviews yet")
        return None

    items = []
    for sub in smartviews:
        items.append(dict(smartview_id=sub['id'],
                          data=sub))

    service = ClosecomDailyLaunchService()

    res = await service.smartview_upsert_many(items)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
        settings.LOGGER.debug(f"raw={res.raw_result}")
    else:
        settings.LOGGER.info("None")

    return res

async def show_smartview_leads(smartview_id, raw=False):
    service = ClosecomDailyLaunchService()
    query = await service.get_smartview_query(smartview_id)

    if not query or query == "*":
        raise AppErrors(f"broken query: {query}")

    leads = await  _execute_closecom_api("list_leads_by_query",
                                         payload=query,
                                         paginate=True)
    if not leads:
        raise AppErrors(f"No leads for query: {query} leads={leads}")

    settings.LOGGER.info(f"received {len(leads)} leads")
    settings.LOGGER.info("...showing major contacts")
    for lead in leads:
        contacts = lead.get('contacts', None)
        if not contacts:
            settings.LOGGER.error(f"no contacts for lead_id={lead['id']}")
            continue

        settings.LOGGER.info(f"{contacts[0]['emails'][0]['email']}                         - {contacts[0]['id']} first contacct for {lead['id']} || total contacts = {len(contacts)}")


    settings.LOGGER.debug(leads)

    return leads

async def check_smartview_leads_duplicates(smartview_id, sequence_id):
    settings.LOGGER.info(f"checking for smartview_id={smartview_id}  sequence_id={sequence_id}")

    service = ClosecomDailyLaunchService()
    query = await service.get_smartview_query(smartview_id)

    if not query or query == "*":
        raise AppErrors(f"broken query: {query}")

    leads = await  _execute_closecom_api("list_leads_by_query",
                                         payload=query,
                                         paginate=True)
    if not leads:
        raise AppErrors(f"No leads for query: {query} leads={leads}")

    contacts = await _remove_subscribed(leads,
                                  sequence_id=sequence_id,
                                  verbose=True)

    settings.LOGGER.info(f"unique contacts found len {len(contacts)}")
    for c in contacts:
        settings.LOGGER.info(f"{c['contact_email']} - {c['contact_id']}")


async def subscribe_smartview(sequence_id,
                              smartview_id,
                              ignore=False):
    service = ClosecomDailyLaunchService()
    sequence_service = CloseComSequenceService()

    sequence = await sequence_service.get_by_id(sequence_id)
    if not sequence:
        raise AppErrors(f"...ERROR not found: sequence_id={sequence_id} call --update-all first")

    data = sequence.data
    sequence_name = data['name']

    sender_dict = await _sequnce_to_sender(sequence_name)
    if not sender_dict:
        raise AppErrors(f"...ERROR not found: can't find sender for sequence_name={sequence_name}")


    can_launch = await service.can_launch(payload=DailyLaunchCreate(
        sequence_id=sequence_id,
        smartview_id=smartview_id,
        data={}
    ))

    if not ignore:
        if not can_launch:
            raise AppErrors(f"You already launched this sequence to this smart_view today")

    query = await service.get_smartview_query(smartview_id)

    if not query or query == "*":
        raise AppErrors(f"broken query: {query}")

    leads = await  _execute_closecom_api("list_leads_by_query",
                                         payload=query,
                                         paginate=True)
    if not leads:
        raise AppErrors(f"No leads for query: {query} leads={leads}")

    # return the list of [{'contact_id' : .., 'contact_email' : ..., 'status' : ..}]
    # this contacts can be subscribed to the sequence_id
    contacts = await _remove_subscribed(leads,
                                  sequence_id=sequence_id)
    if not contacts:
        raise AppErrors(f"Nothing co subscribe, contacts empty={contacts}")


    converted = _convert_to_contacts_dict(contacts,
                                          sender_dict)

    res = await service.launch(payload=DailyLaunchCreate(
        sequence_id=sequence_id,
        smartview_id=smartview_id,
        data=converted
    ))

    if not res:
        raise AppErrors(f"subscribe_smartview ERROR: res for service.launch can't be empty")

    settings.LOGGER.info(f"...Saved launch id={str(res.id)}, call --launch-subscribe now")

async def _sequnce_to_sender(sequence_name):
    sender_email = sequence_to_sender[sequence_name]

    account_service = ClosecomAccountService()

    sender = await account_service.get_by_email(sender_email)
    if not sender:
        return None

    data = sender.data
    di = data['default_identity']
    sender_email = di['email']
    sender_name = di['name']

    sender_dict = dict(sender_account_id=data['id'],
                       sender_email = sender_email,
                       sender_name = sender_name)

    return sender_dict

def _convert_to_contacts_dict(contacts,
                              sender_dict):
    contacts_dict = {}
    for c in contacts:
        contacts_dict[c['contact_id']] = {
            'status' : c['status'],
            'contact_email' : c['contact_email'],
            'id' : c['contact_id'],
            'lead_id' : c['lead_id'],

            'sender_account_id' : sender_dict['sender_account_id'],
            'sender_email' : sender_dict['sender_email'],
            'sender_name' : sender_dict['sender_name']
        }

    return contacts_dict


async def _remove_subscribed(leads, sequence_id, verbose=False):
    all_contacts = []
    for lead in leads:
        contacts = lead.get('contacts', None)
        if not contacts:
            settings.LOGGER.error(f"no contacts for lead_id={lead['id']}")
            continue

        emails = contacts[0].get('emails', [])
        if not emails:
            settings.LOGGER.error(f"no contact emails for lead_id={lead['id']}")
            continue

        all_contacts.append({
            'contact_id' : contacts[0]['id'],
            'contact_email' : emails[0]['email'],
            'status' : 'never_subscribed',
            'lead_id' : lead['id']
        })


    unique_contacts = []

    #Get group_names for all existing contacts with subscription
    contacts_to_group = await _group_by_contacts(verbose=verbose)
    if not contacts_to_group:
        return all_contacts

    new_group_name = sequence_groups[sequence_id]
    for contact in all_contacts:
        contact_id = contact['contact_id']
        contact_email = contact['contact_email']
        if contact_id not in contacts_to_group.keys():
            unique_contacts.append(contact)
            continue

        current_group_names = contacts_to_group[contact_id]
        if new_group_name not in current_group_names:
            unique_contacts.append(contact)
            continue

        settings.LOGGER.info(f"Found duplicate {contact_id} - {contact_email} already subscribed to group={new_group_name} ")


    return unique_contacts

async def _group_by_contacts(verbose=False):
    service = ClosecomSubscriptionService()

    #Will store groups of all sequence the contact already subscribed to
    contacts_to_group = {}

    contacts = await service.get_grouped_by_contact()
    async for c in contacts:
        sequence_ids = c.get('sequence_ids', None)
        if not sequence_ids:
            continue

        contact_id = c['_id']
        if not contact_id:
            raise AppErrors(f"_group_by_contacts ERROR: Never happend conact_id={contact_id}")

        contacts_to_group[contact_id] = []
        for seq in sequence_ids:
            group_name = sequence_groups[seq]
            contacts_to_group[contact_id].append(group_name)

    if verbose:
        settings.LOGGER.info(f"....found unique contacts with subscriptions={len(contacts_to_group.keys())}")
        for c, groups in contacts_to_group.items():
            settings.LOGGER.info(f"{c} - {groups}")

    return contacts_to_group