from datetime import datetime
from umongo import Document, fields
from . import instance
from .base_class import Base

@instance.register
class ListRequestModel(Base, Document):
    list_id = fields.StringField(required=True)
    account = fields.StringField(required=True)
    status = fields.IntField(default=0) #NEW, IN_PROGRESS, PAUSED, FOR_DELETE, DELETED, ERROR

    labels = fields.ListField(fields.StringField()) #Once labels_ids is empty, we can delete a job
    next_page_token = fields.StringField(default='')

    body = fields.DictField()
    response = fields.DictField()

    error = fields.StringField()

@instance.register
class HistoryRequest(Base, Document):
    list_id = fields.StringField(required=True)
    account = fields.StringField(required=True)
    status = fields.IntField(default=0) #NEW, IN_PROGRESS, PAUSED, FOR_DELETE, DELETED, ERROR

    start_history_id = fields.StringField() #Once labels_ids is empty, we can delete a job
    next_page_token = fields.StringField(default='')

    body = fields.DictField()
    response = fields.DictField()

    error = fields.StringField()

@instance.register
class GetRequestModel(Base, Document):
    list_id = fields.StringField(required=True)
    account = fields.StringField(required=True)
    msg_format = fields.StringField(required=True)
    status = fields.IntField(default=0) #NEW, IN_PROGRESS, PAUSED, FOR_DELETE, DELETED, ERROR

    msg_ids = fields.ListField(fields.StringField())
    body = fields.DictField()
    response = fields.DictField()

    error = fields.StringField()


@instance.register
class Watches(Base, Document):
    list_id = fields.StringField(required=True)
    account = fields.StringField(required=True)
    status = fields.IntField(default=0) #NEW, IN_PROGRESS, PAUSED, FOR_DELETE, DELETED, ERROR

    labels = fields.ListField(fields.StringField()) #Once labels_ids is empty, we can delete a job

    expiration = fields.StringField()
    history_id = fields.StringField()

    body = fields.DictField()
    response = fields.DictField()

    error = fields.StringField()
