from datetime import datetime
from umongo import Document, fields
from . import instance
from .base_class import Base

@instance.register
class Form(Base, Document):
    owner_id = fields.ObjectIdField(required=True)
    form_id = fields.StringField(default='')
    data = fields.DictField()

    class Meta:
        indexes = ['owner_id']