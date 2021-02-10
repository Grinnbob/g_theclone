from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class CloseComEmailActivity(Base, Document):
    activity_id = fields.StringField(required=True, unique=True)
    thread_id = fields.StringField()
    from_email = fields.StringField(required=True)
    to_email = fields.StringField(required=True)
    direction = fields.StringField(required=True)

    data = fields.DictField()