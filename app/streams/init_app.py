import faust
from app.core.config import settings

_app = None

def get_stream_app():
    global _app

    if not _app:
        _app = faust.App(settings.FAUST_APP_NAME,
                         broker=settings.FAUST_APP_BROKER,
                         store=settings.FAUST_APP_STORE)

    return _app

