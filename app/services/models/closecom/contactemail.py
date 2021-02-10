from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class CloseComContactEmail(Base, Document):
    email = fields.StringField(required=True, unique=True)

    data = fields.DictField()