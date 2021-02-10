from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class CloseComLead(Base, Document):
    lead_id = fields.StringField(required=True, unique=True)
    customer = fields.StringField(required=True)
    status_id = fields.StringField(required=True)
    status_label = fields.StringField(required=True)

    data = fields.DictField()
