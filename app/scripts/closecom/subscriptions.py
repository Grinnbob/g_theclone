from app.scripts.closecom.provider import _execute_closecom_api
from app.services.closecom.subscription_service import ClosecomSubscriptionService
from app.services.closecom.dailylaunch_service import ClosecomDailyLaunchService
from app.exceptions import *
from app.schemas.models.closecom.subscription import *
from pprint import pprint
import traceback
from app.core.config import settings

async def show_subscription(s_id):
    settings.LOGGER.info(f"...showing subscription id={s_id}")

    subscription = await  _execute_closecom_api("list_subscription", payload=s_id)
    if not subscription:
        settings.LOGGER.error(f"There is no subscription for id={s_id}")
        return None

    settings.LOGGER.info(subscription)


async def show_subscriptions():
    settings.LOGGER.info("...showing all subscriptions")

    subscriptions = await  _execute_closecom_api("list_subscriptions", paginate=True)
    if not subscriptions:
        settings.LOGGER.error(f"There is no subscriptions yet")
        return None

    settings.LOGGER.info(subscriptions)

    return

async def update_subscriptions():
    settings.LOGGER.info("...get all subscriptions from server and update or create in DB")

    subscriptions = await  _execute_closecom_api("list_subscriptions", paginate=True)
    if not subscriptions:
        settings.LOGGER.error(f"There is no subscriptions yet")
        return None

    items = []
    for sub in subscriptions:
        items.append(dict(subscription_id=sub['id'],
                          status=sub.get('status', ''),
                          data=sub))

    service = ClosecomSubscriptionService()

    res = await service.upsert_many(items)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
        settings.LOGGER.debug(f"raw={res.raw_result}")
    else:
        settings.LOGGER.info("None")

    return res


async def show_duplicated_subscriptions(sequence_groups):
    settings.LOGGER.info("...showing duplicated subscriptions: DON'T FORGET to CALL --store-subscriptions first")

    service = ClosecomSubscriptionService()

    all_subscriptions = await service.get_grouped_by_contact()

    #will be stored duplicated sequence_ids that we need to finis
    # {
    #    1 : [sequence_id1, sequence_id2, ...],
    #    2 : [...]
    #    ....
    # }
    duplicates = {}
    duplicated_contacts = set()
    index = 1
    async for sub in all_subscriptions:
        # we group by contact_id, and data = [ push: CloseComSubscription.data]
        # data = all subscriptions to current contact_id
        data = sub.get('data')
        if len(data) > 1:
            index = index + 1
            grouped_by_group_name = {}
            duplicate_found = False

            #loop through all subscriptions for given contact
            #if there are more than 1 subscription from the same group - it's a duplicate
            for d in data:
                sequence_id = d.get('sequence_id')
                subscription_id = d.get('id')
                subscription_status = d.get('status')

                group_name = sequence_groups.get(sequence_id, None)
                if not group_name:
                    raise Exception(f"There is no line in sequence_groups for sequence_id={sequence_id}")

                exist = grouped_by_group_name.get(group_name, None)
                if exist:
                    duplicate_found = True

                    if duplicates.get(index, None) is None:
                        duplicates[index] = []

                    #these are 2nd and the next sequences from the same group - we will need to finish it
                    #because it duplicates
                    duplicates[index].append({ 'subscription_id' : subscription_id,
                                                'subscription_status': subscription_status})
                else:
                    #the first sequence for this group
                    grouped_by_group_name[group_name] = [sequence_id]

            if duplicate_found:
                settings.LOGGER.info(f"\nDuplicate found for {data[0].get('contact_email')} - {data[0].get('contact_id')}")
                duplicated_contacts.add(data[0].get('contact_email'))
                for d in data:
                    settings.LOGGER.info(f"*****{d.get('contact_email')} - {d.get('sender_email')} - {d.get('status')} - {d.get('id')}")

    settings.LOGGER.info(duplicates)
    settings.LOGGER.info(duplicated_contacts)
    return duplicates

async def unsubscribe_duplicated_subscriptions(sequence_groups):
    duplicates = await show_duplicated_subscriptions(sequence_groups=sequence_groups)

    if len(duplicates.keys()) <= 0:
        settings.LOGGER.info("There is no duplicate found, try to call --store-subscriptions")
        return

    for k, v in duplicates.items():
        for sub in v:
            s_status = sub['subscription_status']
            s_id = sub['subscription_id']
            if s_status != 'active':
                settings.LOGGER.info(f"{s_id} already paused or finished current_status={s_status}")
                continue

            res = await  _execute_closecom_api("finish_subscription", payload=s_id)
            settings.LOGGER.info(f"paused {s_id}, res={res}")


async def finish_subscription(subscription_id):
    res = await  _execute_closecom_api("finish_subscription", payload=subscription_id)
    pprint(res)

    return res



async def launch_subscribe(launch_id):
    service = ClosecomDailyLaunchService()

    launch = await service.get(id=launch_id)
    if not launch:
        raise AppErrors(f"launch_subscribe ERROR: launch with id={launch_id} not found")

    sequence_id = launch.sequence_id
    contacts = launch.data.copy()
    for c_id, data in contacts.items():
        current_status = data.get('status')
        if current_status != 'never_subscribed':
            settings.LOGGER.info(f"ALREADY subscribed {c_id} - {data['contact_email']} - {data['status']}")
            continue

        try:
            res = await _execute_closecom_api("sequence_subscribe",
                                              payload=ApiSubscribeSequence(sequence_id=sequence_id,
                                                                           contact_id=c_id,
                                                                           contact_email=data['contact_email'],
                                                                           sender_account_id=data['sender_account_id'],
                                                                           sender_email=data['sender_email'],
                                                                           sender_name=data['sender_name']
            ))

            if res:
                contacts[c_id]['status'] = 'subscribed'
                settings.LOGGER.info(f"SUBSCRIBED: {c_id} - {data['contact_email']}")
            else:
                raise AppErrors(f"something went wrong res={res}")
        except Exception as e:
            traceback.print_exc()
            settings.LOGGER.error(str(e))
            settings.LOGGER.error(f"Error subscribing contact_id={c_id} - email={data['contact_email']} - status={data['status']}")
            continue

    try:
        res = await service.update_data(id=launch_id, data=contacts)
    except Exception as e:
        settings.LOGGER.error(str(e))
        settings.LOGGER.error(f"Error updating status for launch_id={launch_id}")
        settings.LOGGER.error("NEED TO DO IT by hands status:")
        settings.LOGGER.error(contacts)

    return contacts

async def test_update():
    items = [
        {
            'subscription_id' : 'new',
            'status' : 'newwwwwwwwwwwwwwwww',
            'data' : {
                'asfadfadsf':'sadfa123123123dsfsdf'
            }
        },
        {
            'subscription_id': 'new1',
            'status': 'new-newwwwwwwwwww',
            'data': {
                'one' : 1123123123
            }
        },
        {
            'subscription_id': 'new3',
            'status': 'new',
            'data': {
                'one': 2123123
            }
        }
    ]

    service = ClosecomSubscriptionService()

    res = await service.upsert_many(items)

    if res:
        pprint(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
        pprint(f"raw={res.raw_result}")
    else:
        pprint("None")

    return res
