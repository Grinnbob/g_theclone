from app.streams import get_stream_app
from app.schemas.topics.google_push import PushDataModel, PushKeyBase
from app.core.config import settings

app = get_stream_app()

push_updates_topic = app.topic('push_updates_topic', key_type=PushKeyBase, value_type=PushDataModel)