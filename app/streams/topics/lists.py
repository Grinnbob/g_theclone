from app.streams import get_stream_app
from app.schemas.topics.lists import ListDataTopicModel, ListUpdateTopicModel, ListKeyBaseModel
from app.core.config import settings

app = get_stream_app()

#TODO: how to convert kafka connect mongodb source from STR to JSON
list_model_update_topic = app.topic(settings.TOPIC_LIST_CHANGE)

list_data_topic = app.topic('list_data_topic', key_type=ListKeyBaseModel, value_type=ListDataTopicModel)
list_update_topic = app.topic('list_update_topic', key_type=ListKeyBaseModel, value_type=ListUpdateTopicModel)