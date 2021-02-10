from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class CloseComCustomerStat(Base, Document):
    customer = fields.StringField()
    date_from = fields.DateField()
    date_to = fields.DateField()

    stats = fields.DateField()