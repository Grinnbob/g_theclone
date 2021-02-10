from app.streams import get_stream_app
from app.schemas.topics.watch import WatchUpdateModel, WatchKeyBase
from app.core.config import settings

app = get_stream_app()

watch_update_topic = app.topic('watch_update_topic', key_type=WatchKeyBase, value_type=WatchUpdateModel)