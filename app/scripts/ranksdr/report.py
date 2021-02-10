import pandas as pd
from app.services.ranksdr.dialog_service import RankSdrDialogService
from app.services.ranksdr.report_service import RankSdrReportService
from app.core.config import settings

from .provider import _execute_nlp_report
from app.providers.nlpprovider.topics import TopicStatistics
from app.providers.nlpprovider.entities import EntityStatistics

async def analyze_ranksdr_data(filepath):
    await save_dialogs(filepath)

    await build_entities_report()
    await build_topics_report()

    settings.LOGGER.info('...data reports analyzed')


async def show_ranksdr_data(email, filepath):
    # find report data by email
    report_service = RankSdrReportService()

    topics_report = await report_service.load_report(email, 'topics')
    settings.LOGGER.info('...topics report received')
    #settings.LOGGER.info(topics_report)

    # plot graph and save in filepath
    topics_model = TopicStatistics()
    topics_model.save_plot(topics_report['data'], filepath + "_topics")

    settings.LOGGER.info('...topics data report saved')

    entities_report = await report_service.load_report(email, 'entities')
    settings.LOGGER.info('...entities report received')
    #settings.LOGGER.info(entities_report)

    # plot graph and save in filepath
    entities_model = EntityStatistics()
    entities_model.save_plot(entities_report['data'], filepath + "_entities")

    settings.LOGGER.info('...entities data report saved')


async def build_entities_report():

    dialog_service = RankSdrDialogService()
    report_service = RankSdrReportService()

    dialogs = await dialog_service.load_dialogs()

    dialogs_list = []

    async for dialog in dialogs:
        dialogs_list.append(dialog)

    settings.LOGGER.info(f"dialogs_list: {len(dialogs_list)}")

    try:
        data = await _execute_nlp_report('get_entities_report',
                                    payload=dialogs_list)
        
        if data:
            await report_service.save_report(data)

    except Exception as e:
        settings.LOGGER.error(f"ERROR: can't build reports for entities: ")
        settings.LOGGER.error(e)


async def build_topics_report():

    dialog_service = RankSdrDialogService()
    report_service = RankSdrReportService()

    dialogs = await dialog_service.load_dialogs()

    dialogs_list = []

    async for dialog in dialogs:
        dialogs_list.append(dialog)

    settings.LOGGER.info(f"dialogs_list: {len(dialogs_list)}")

    try:
        data = await _execute_nlp_report('get_topics_report',
                                    payload=dialogs_list)
        
        if data:
            await report_service.save_report(data)

    except Exception as e:
        settings.LOGGER.error(f"ERROR: can't build reports for topics: ")
        settings.LOGGER.error(e)


async def save_dialogs(filepath):

    # load data from CSV
    df = pd.read_csv(filepath, delimiter=';')
    df.drop(['Phone', 'Name', 'Status ID', 'formid', 'Date'], axis=1, inplace=True)
    df.dropna(inplace=True)
    df['id'] = df['tranid'].apply(lambda x: str(x))
    df.drop(['tranid'], axis=1, inplace=True)

    data = df.set_index('id').to_dict('index')

    transformed_data = []
    for key in data:
        email = data[key]['Email']
        del data[key]['Email']
        lead = {
            'lead_id': key,
            'data': {
                'email': email,
                'dialogs': data[key]
            }
        }
        transformed_data.append(lead)

    settings.LOGGER.info(f"...received {len(transformed_data)} dialogs")

    service = RankSdrDialogService()

    res = await service.upsert_many(transformed_data)

    if res:
        settings.LOGGER.info(f"result = matched_count={res.matched_count}, modified_count={res.modified_count}, upserted_id={res.upserted_id}")
        settings.LOGGER.debug(f"raw={res.raw_result}")
    else:
        settings.LOGGER.info("None")

    return res

