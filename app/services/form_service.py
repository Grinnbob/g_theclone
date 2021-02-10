from app.exceptions import *
from typing import Any, Type
from .base import BaseService
import app.schemas.models.form as form_schema
from .models.form import Form
from .models.base_class import Base
from app.core.config import settings
from bson.objectid import ObjectId


class FormService(BaseService[Form, form_schema.FormCreate, form_schema.FormUpdate]):
    def __init__(self):
        super().__init__(model=Form)

    async def create(self,
                     owner_id: ObjectId,
                     form_id: str) -> Form:
        exist = await Form.find_one({'owner_id' : owner_id, 'form_id': form_id})
        if exist:
            return exist

        db_obj = Form(owner_id=owner_id,
                      form_id=form_id)

        await db_obj.commit()
        await db_obj.reload()

        return db_obj

    async def update(self,
        owner_id: ObjectId,
        obj_in: form_schema.FormUpdate
    ) -> Form:
        exist = await Form.find_one({'form_id': obj_in.form_id, 'owner_id' : owner_id})
        if not exist:
            raise AppErrors(f"No such form id={obj_in.form_id}")

        o_data = {}
        if exist.data:
            o_data = exist.data.to_mongo()

        o_data[obj_in.step] = obj_in.data
        exist.data = o_data

        await exist.commit()
        await exist.reload()

        return exist

    async def dump(self,
                   owner_id: ObjectId,
                   form_id: str,
                   model_class: Type[Base]) -> Base:

        exist = await Form.find_one({'form_id': form_id, 'owner_id': owner_id})
        if not exist:
            raise AppErrors(f"No such form id={form_id}")

        res = {}

        data = exist.data
        for k, v in data.items():
            res.update(v)

        instance = model_class(owner_id=owner_id, **res)

        await instance.commit()

        try:
            await exist.remove()
        except:
            pass

        return instance

