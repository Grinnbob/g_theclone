from app.exceptions import *
from typing import Any
import traceback
import os
from app.core.config import settings
import pandas as pd
from .topics import TopicStatistics
from .entities import EntityStatistics

from .dummy_topics import dummy_topics_list


class NlpProvider():
    def __init__(self, direct=True):
        if direct:
            raise AppErrors("Must use async create_api_provider to create instance")

        self.session = None


    @classmethod
    async def create_api_provider(cls,
                                  settings: dict=settings.NLP_PROVIDER_SETTINGS) -> Any:

        provider = cls(direct=False)

        provider.settings = settings

        return provider


    async def get_entities_report(self, payload):
        model = EntityStatistics()

        # Get entities for each lead
        all_entities = []
        #n_messages_total = 0
        lead_data = []
        for lead in payload:
            all_entities.append(model.get_cleaned_entities(lead))
            lead_data.append({'email': lead.data['email'], 'n_messages': len(lead['data']['dialogs'].values())})
            #n_messages_total += len(lead['data']['dialogs'].values())

        settings.LOGGER.info(f'... {len(lead_data)} leads received')
        #settings.LOGGER.info(f'... {n_messages_total} total messages received')

        df_all_entities = pd.concat(all_entities)

        # Get avg values
        #model.set_eatalon_entities(df_all_entities, n_messages_total)

        # Get reports
        reports = []
        i = 0
        for lead_entities in all_entities:
            report_data = model.get_top_entities(lead_entities, lead_data[i]['n_messages'])
            #report_data = model.get_compared_entities(top_lead_entities)

            # transform int keys to strings for mongo
            report_data = {
                'count': {str(key): value for key, value in report_data['count'].items()},
                'name': {str(key): value for key, value in report_data['name'].items()}
            }

            reports.append({'email': lead_data[i]['email'], 'report_type': 'entities', 'data': report_data})
            i += 1

        return reports


    async def get_topics_report(self, payload):
        model = TopicStatistics()
        topics = dummy_topics_list # dummy topics
        model.fit(topics)

        # Get topics for each lead
        all_topics = []
        emails = []
        for lead in payload:
            all_topics.append(model.get_topics_from_messages(list(lead.data['dialogs'].values())))
            emails.append(lead.data['email'])

        df_all_topics = pd.concat(all_topics)

        # Get avg values
        etalon_topics = df_all_topics.groupby(['topic']).mean().reset_index()
        model.set_etalon_topics(etalon_topics)

        # Get reports
        reports = []
        i = 0
        for lead_topics in all_topics:
            report_data = model.get_compared_topics(lead_topics)

            # transform int keys to strings for mongo
            report_data = {
                'count': {str(key): value for key, value in report_data['count'].items()},
                'topic': {str(key): value for key, value in report_data['topic'].items()}
            }

            reports.append({'email': emails[i], 'report_type': 'topics', 'data': report_data})
            i += 1

        return reports
