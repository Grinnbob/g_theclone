from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class ZerobounceEmailCheck(Base, Document):
    email = fields.StringField(required=True, unique=True)
    status = fields.StringField(default="new")

    data = fields.DictField()