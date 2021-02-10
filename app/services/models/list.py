from app.schemas.globals import *
from datetime import datetime
from umongo import Document, fields
from . import instance
from .base_class import Base

@instance.register
class SyncList(Base, Document):
    owner_id = fields.ObjectIdField(required=True)
    title = fields.StrField(required=True)
    account_labels = fields.DictField(required=True)
    status = fields.IntField(default=STATUS_IN_PROGRESS)

    tags = fields.ListField(fields.StrField())
    export_url = fields.URLField()

    labels_changed = fields.DictField()

    created_time = fields.DateTimeField(default=datetime.utcnow)
    updated_time = fields.DateTimeField()

    class Meta:
        indexes = ['-created_time']