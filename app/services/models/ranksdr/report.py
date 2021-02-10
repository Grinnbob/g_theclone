from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class RankSdrReport(Base, Document):
    email = fields.StringField(required=True)

    report_type = fields.StringField() # int field ?
    
    data = fields.DictField()
