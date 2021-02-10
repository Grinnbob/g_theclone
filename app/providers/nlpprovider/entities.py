import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from app.core.config import settings

import os
from google.cloud import language_v1

class EntityStatistics:

    def __init__(self, top_n=20):
        # top N entities
        self.top_n = top_n

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./My Project-41f62cd13906.json" # todo: remove from here


    def _analyze_entities(self, text_content):
        client = language_v1.LanguageServiceClient()

        # Available types: PLAIN_TEXT, HTML
        type_ = language_v1.Document.Type.PLAIN_TEXT

        # Optional. If not specified, the language is automatically detected.
        # For list of supported languages:
        # https://cloud.google.com/natural-language/docs/languages
        document = {"content": text_content, "type_": type_, "language": "en"}

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = language_v1.EncodingType.UTF8

        response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

        return response.entities

    
    def _get_raw_entities(self, data):
        entities = []

        for msg in data:
            msg_entities = self._analyze_entities(msg)

            for entity in msg_entities:
                new_entity = {'name': entity.name, 'type': language_v1.Entity.Type(entity.type_).name}

                entities.append(new_entity)
        
        settings.LOGGER.info("...Entities found: {}".format(len(entities)))
        return entities

    
    def get_cleaned_entities(self, raw_entities):
        entities = pd.DataFrame(self._get_raw_entities(raw_entities['data']['dialogs'].values()))

        entities.drop(entities[entities.type == 'NUMBER'].index, inplace=True)
        entities.drop(entities[entities.type == 'DATE'].index, inplace=True)
        entities.drop(entities[entities.type == 'PHONE_NUMBER'].index, inplace=True)

        return entities


    def get_top_entities(self, entities, n_messages):
        # get top N entities
        entities = entities.drop('type', axis=1) # one name can has a few types
        top_entities = pd.DataFrame(entities.value_counts(sort=True)[:self.top_n].index.tolist())
        top_entities.columns = ['name']

        entities_count = entities.value_counts(sort=True)[:self.top_n].values.tolist()
        top_entities['count'] = list(map(lambda x: 100 * x / n_messages, entities_count))

        return top_entities


    def set_eatalon_entities(self, all_entities, n_messages):
        self.etalon_entities = self.get_top_entities(all_entities, n_messages)
        settings.LOGGER.info(self.etalon_entities)


    def get_compared_entities(self, entities):
        compared_entities = []
        for index, row in self.etalon_entities.iterrows():
            try:
                entity_value = entities.loc[entities['name'] == row['name']]['count'].values[0]
            except:
                # entity not found
                entity_value = 0

            if entity_value > row['count']:
                compared_value = entity_value / row['count'] - 1
            elif entity_value == 0:
                compared_value = - row['count'] / 100
            else:
                compared_value = 1 - row['count'] / entity_value

            compared_entities.append({'name': row['name'], 'count': 100 * compared_value})

        # sort values
        return pd.DataFrame(compared_entities).sort_values(by=['count'], ascending=False).reset_index(drop=True)


    def save_plot(self, compared_entities, filepath):
        compared_entities = pd.DataFrame(compared_entities)

        f, ax = plt.subplots(figsize=(16, len(compared_entities)))

        sns_plot = sns.barplot(y="name", x="count",
                    palette="ch:.25", edgecolor=".6",
                    data=compared_entities)

        ax.set(ylabel="",
            xlabel="SDR entities difference from average, %")

        sns_plot.get_figure().savefig(filepath)