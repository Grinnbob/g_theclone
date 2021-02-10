from app.streams import get_stream_app
from app.schemas.topics.lists import ListModelChange, ListDataTopicModel
from app.core.config import settings

app = get_stream_app()

list_data_table = app.Table('list_data_table', partitions=8)
list_stats_table = app.Table('list_stats_table', partitions=8)