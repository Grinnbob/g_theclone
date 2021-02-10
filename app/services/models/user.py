from datetime import datetime
from umongo import Document, fields
from . import instance
from .base_class import Base


@instance.register
class User(Base, Document):
    email = fields.EmailField(unique=True, required=True)
    hashed_password = fields.StringField(required=True)

    role = fields.StringField(default='')
    active = fields.BooleanField(default=True)
    package = fields.StringField(default='free')

    oauth_state = fields.StringField(default='')

    created_time = fields.DateTimeField(default=datetime.utcnow)
    updated_time = fields.DateTimeField()

    custom_info = fields.DictField()

    class Meta:
        indexes = ['-created_time']