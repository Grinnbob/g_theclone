from app.scripts.closecom.provider import _execute_closecom_api
from app.services.closecom.account_service import ClosecomAccountService
from app.core.config import settings

async def show_accounts(raw=False):
    settings.LOGGER.info("...showing all accounts")

    accounts = await  _execute_closecom_api("list_accounts", paginate=True)
    if not accounts:
        settings.LOGGER.error(f"There is no accounts created yet")

    settings.LOGGER.info("id | email | name | user_id |")
    for ac in accounts:
        try:
            di = ac['default_identity']
            settings.LOGGER.info(f"{ac['id']}      | {di['email']}      | {di['name']}   | {ac['user_id']}")
        except Exception as e:
            settings.LOGGER.error(f"Error for {ac['id']} {ac['email']} - {str(e)}")

    settings.LOGGER.debug(accounts)

async def update_accounts():
    settings.LOGGER.info("....updateing all accounts")

    accounts = await  _execute_closecom_api("list_accounts", paginate=True)
    if not accounts:
        settings.LOGGER.error(f"There is no accounts created yet")

    items = []
    for ac in accounts:
        items.append(dict(account_id=ac['id'],
                          data=ac))

    settings.LOGGER.info(f"...received {len(items)} accounts")

    service = ClosecomAccountService()

    res = await service.upsert_many(items)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
        settings.LOGGER.debug(f"raw={res.raw_result}")
    else:
        settings.LOGGER.info("None")

    return res
