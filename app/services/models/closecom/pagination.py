from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class CloseComPagination(Base, Document):
    endpoint = fields.StringField(required=True, unique=True)
    _skip = fields.IntField(required=True)