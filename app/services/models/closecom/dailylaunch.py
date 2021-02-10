from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class CloseComDailyLaunch(Base, Document):
    sequence_id = fields.StringField(required=True)
    smartview_id = fields.StringField(required=True)

    data = fields.DictField()
    created_day = fields.StringField(required=True)


@instance.register
class CloseComSmartView(Base, Document):
    smartview_id = fields.StringField(required=True, unique=True)

    data = fields.DictField()