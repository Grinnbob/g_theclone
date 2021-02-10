from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class CloseComSubscription(Base, Document):
    subscription_id = fields.StringField(required=True, unique=True)
    status = fields.StringField()

    data = fields.DictField()
