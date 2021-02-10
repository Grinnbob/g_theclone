from app.exceptions import *
from app.scripts.globals import *
from app.scripts.closecom.accounts import update_accounts
from app.scripts.closecom.sequences import update_sequences
from app.scripts.closecom.smartviews import update_smartviews
from app.scripts.closecom.subscriptions import update_subscriptions
from app.scripts.closecom.smartviews import subscribe_smartview
from app.scripts.closecom.subscriptions import launch_subscribe
from app.scripts.closecom.lead import lead_change_status

from app.services.closecom.sequence_service import CloseComSequenceService
from app.services.closecom.account_service import ClosecomAccountService
from app.services.closecom.dailylaunch_service import ClosecomDailyLaunchService
import time
from app.core.config import settings

async def update_all():
    settings.LOGGER.info(f"...updating all data")

    settings.LOGGER.info("updating accounts...")
    await update_accounts()

    settings.LOGGER.info("updating sequences...")
    await update_sequences()

    settings.LOGGER.info("updating smartviews...")
    await update_smartviews()

    settings.LOGGER.info("updating subscriptions...")
    await update_subscriptions()

async def launch_all(need_update='1'):
    if need_update == '1':
        settings.LOGGER.info("...UPDATING ALL ENTITIES")
        await update_all()

    settings.LOGGER.info("...launching daily sequence subscriptions")

    sequence_service = CloseComSequenceService()
    account_service = ClosecomAccountService()
    dailylaunch_service = ClosecomDailyLaunchService()

    for smartview_id, data in smartviews_launch_list.items():
        if data['status'] != 'active':
            settings.LOGGER.info(f"...PASS: smartview {data['title']}  status={data['status']}")
            continue

        tasks = data['tasks']
        if not tasks:
            settings.LOGGER.info(f"...NO TASKS: {data['title']}  status={data['status']}")
            continue

        settings.LOGGER.info(f"...EXECUTE: {data['title']}  status={data['status']}")
        for task in tasks:
            settings.LOGGER.info("waiting 10 seconds....")
            time.sleep(10)

            try:
                sequence_name = task['sequence']
                sender_email = task['sender']

                sequence = await sequence_service.get_by_name(sequence_name)
                if not sequence:
                    raise AppErrors(f"sequence_name={sequence_name} NOT FOUND")

                sender = await account_service.get_by_email(sender_email)
                if not sender:
                    raise AppErrors(f"sender_email={sender_email} NOT FOUND")

                try:
                    settings.LOGGER.info(f"Creating launch in database")
                    # sequence_id, smartview_id
                    await subscribe_smartview(sequence_id=sequence.sequence_id,
                                              smartview_id=smartview_id)
                except Exception as e:
                    settings.LOGGER.error(f"{str(e)} for sequence_name={sequence_name} - smartview_id={smartview_id}")
                    pass


                contacts = {}
                try:
                    settings.LOGGER.info(f"Launch subscription")
                    # sequence_id, smartview_id
                    exist = await dailylaunch_service.get_launch_for_today(smartview_id=smartview_id,
                                                                               sequence_id=sequence.sequence_id)
                    if not exist:
                        raise AppErrors(f"ERROR: launch NOT FOUND smartview_id={smartview_id} sequence_id={sequence.sequence_id}")

                    launch_id = str(exist.id)
                    contacts = await launch_subscribe(launch_id=launch_id)

                except Exception as e:
                    settings.LOGGER.error(f"{str(e)}")
                    pass


                try:
                    if not contacts:
                        settings.LOGGER.info(f"Changing lead status - no need, contacts empty")
                        continue

                    settings.LOGGER.info(f"Changing lead status")
                    for c_id, data in contacts.items():
                        try:
                            res = await lead_change_status(lead_id=data['lead_id'],
                                                           status='scheduled')
                        except Exception as e:
                            settings.LOGGER.error(f"lead_id={data['lead_id']} can't change status error={str(e)}")
                            continue

                except Exception as e:
                    settings.LOGGER.error(f"{str(e)}")
                    pass

            except Exception as e:
                settings.LOGGER.error(f"..ERROR: can't execute task={task}  error={str(e)}")
                continue

