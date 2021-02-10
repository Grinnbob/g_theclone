from datetime import datetime
from umongo import Document, fields
from . import instance
from .base_class import Base

@instance.register
class Message(Base, Document):
    msg_id = fields.StringField(required=True, unique=True)
    msg_format = fields.StringField(required=True)
    account = fields.StringField(required=True)
    list_id = fields.StringField()

    lists = fields.ListField(fields.StringField())

    status = fields.IntField(default=0) #NEW, IN_PROGRESS, PAUSED, FOR_DELETE, DELETEDб ERROR
    raw_message = fields.DictField()

    merge = fields.DictField()

    class Meta:
        indexes = ['msg_id', 'lists', 'account']
