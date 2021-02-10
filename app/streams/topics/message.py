from app.streams import get_stream_app
from app.core.config import settings

app = get_stream_app()

#TODO: how to convert kafka connect mongodb source from STR to JSON
message_model_update_topic = app.topic(settings.TOPIC_MESSAGE_CHANGE)