from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import Base

@instance.register
class RankSdrDialog(Base, Document):
    lead_id = fields.StringField(required=True, unique=True)

    date = fields.DateTimeField(default=datetime.utcnow)
    
    data = fields.DictField()
