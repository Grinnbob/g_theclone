from app.scripts.closecom.provider import _execute_closecom_api
from app.services.closecom.sequence_service import CloseComSequenceService
from app.core.config import settings

async def show_sequence(s_id):
    settings.LOGGER.info(f"...showing sequence id={s_id}")

    sequence = await  _execute_closecom_api("list_sequence", s_id)
    if not sequence:
        settings.LOGGER.error(f"There is no sequence for id={s_id}")
        return

    settings.LOGGER.info("id | name | stats")
    settings.LOGGER.info(f"{sequence['id']}        |  {sequence['subscription_counts_by_status']}           | {sequence['name']}")

    settings.LOGGER.info("..full data: ")
    settings.LOGGER.info(sequence)

async def show_sequences():
    settings.LOGGER.info("...showing all sequences")

    sequences = await  _execute_closecom_api("list_sequences", paginate=True)
    if not sequences:
        settings.LOGGER.error(f"There is no sequences created yet")
        return None

    settings.LOGGER.info("id | status | timezone | name |")
    for sq in sequences:
        settings.LOGGER.info(f"{sq['id']}      | {sq['status']}      | {sq['timezone']}        | {sq['name']}")

    return sequences

async def update_sequences():
    settings.LOGGER.info("...get all sequences from server and update or create in DB")

    sequences = await  _execute_closecom_api("list_sequences", paginate=True)
    if not sequences:
        settings.LOGGER.error(f"There is no sequences yet")
        return None

    items = []
    for sq in sequences:
        items.append(dict(sequence_id=sq['id'],
                          data=sq))

    service = CloseComSequenceService()

    res = await service.upsert_many(items)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
    else:
        settings.LOGGER.info("None")

    return res

