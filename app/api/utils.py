from umongo import Document
from app.services.models.base_class import Base
from app.core.config import settings

def hack_serialize(data):
    if isinstance(data, Base):
        return data.to_mongo()

    if isinstance(data, list):
        if len(data) > 0:
            if isinstance(data[0], Base):
                data = [d.to_mongo() for d in data]

    return data

def page_to_raw(page: int):
    skip = page * settings.PER_PAGE
    limit = settings.PER_PAGE

    return skip, limit