from datetime import datetime
from umongo import Document, fields
from app.services.models import instance
from app.services.models.base_class import  Base

@instance.register
class Test(Base, Document):
    user_id = fields.ObjectIdField(required=True)

    title = fields.StringField(required=True)
    data = fields.DictField(required=True)

    active = fields.BooleanField(default=True)

    created_time = fields.DateTimeField(default=datetime.utcnow)
    updated_time = fields.DateTimeField()

    class Meta:
        indexes = ['-created_time']