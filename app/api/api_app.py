from fastapi import Depends, FastAPI, Header, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import get_db, close_db
from .routes import setup_routes
from .errors import setup_error_handler
from umongo import Document
_app = None

def get_app():
    global _app

    if not _app:
        _app = FastAPI(title=settings.PROJECT_NAME)
        setup_app(_app)

    return _app

def setup_app(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", get_db)
    app.add_event_handler("shutdown", close_db)

    # app.add_exception_handler(HTTPException, http_error_handler)
    # app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

    setup_routes(app)
    setup_error_handler(app)