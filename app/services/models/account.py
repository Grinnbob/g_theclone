from datetime import datetime
from umongo import Document, fields
from . import instance
from .base_class import Base

@instance.register
class Account(Base, Document):
    email = fields.StringField(required=True)
    status = fields.IntField(default=0)
    owner_id = fields.ObjectIdField()
    active = fields.BooleanField(default=True)
    is_logged = fields.IntField(default=0)

    credentials = fields.DictField()
    profile = fields.DictField()
    oauth_state = fields.StringField(default='')

    error_message = fields.StringField(default='')

    created_time = fields.DateTimeField(default=datetime.utcnow)
    updated_time = fields.DateTimeField()

    class Meta:
        indexes = ['-created_time']