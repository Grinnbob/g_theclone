from app.streams import get_stream_app
from app.schemas.topics.closecom_commands import CloseCommandKey, CloseCommandModel
from app.core.config import settings

app = get_stream_app()

closecom_commands_topic = app.topic('closecom_commands_topic', key_type=CloseCommandKey, value_type=CloseCommandModel)