from app.exceptions import *
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from app.database import get_db
from app.services.models import instance, Base
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
import traceback

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

        initialized = False
        try:
            exist = instance.db
            if exist:
                initialized = True
        except Exception as e:
            initialized = False
            self.db = None

        if not initialized:
            self.db = get_db()
            instance.init(self.db)

    async def create_many(self,
                           items: List[CreateSchemaType]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"create_many list can't be empty")

        try:
            res = await self.model.insert_many(items, ordered=False) #ordered - will ignore duplicates, but still raise an Exception
        except Exception as e:
            #TODO: catch only duplicate error
            traceback.print_exc()
            print(f"create_many {str(e)}  type={type(e)}")
            return None

        return res


    async def get(self,
                  id: str,
                  owner_id: Optional[ObjectId] = None) -> Optional[ModelType]:
        req = {
            '_id' : ObjectId(id)
        }
        if owner_id:
            req['owner_id'] = owner_id

        exist = await self.model.find_one(req)
        if not exist:
            raise AppErrors("Not exist")

        return exist

    async def get_multi(self,
                    owner_id: Optional[ObjectId] = None,
                    skip: int = 0,
                    limit: int = 100
    ) -> List[ModelType]:
        req = {}
        if owner_id:
            req['owner_id'] = owner_id

        cursor = self.model.find(req).skip(skip).limit(limit)

        return await cursor.to_list(length=limit)

    async def create(self,
               obj_in: CreateSchemaType) -> ModelType:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore

        await db_obj.commit()
        await db_obj.reload()

        return db_obj

    async def update(
        self,
        id: str,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:

        db_obj = await self.model.find_one({ '_id' : ObjectId(id)})
        if not db_obj:
            raise AppErrors("Not exist")

        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        await db_obj.commit()
        await db_obj.reload()

        return db_obj

    async def remove(self,
                id: str,
                owner_id: Optional[ObjectId] = None) -> ModelType:
        req = {
            '_id' : ObjectId(id)
        }
        if owner_id:
            req['owner_id'] = owner_id

        exist = await self.model.find_one(req)
        if not exist:
            raise AppErrors("Not exist")

        await exist.remove()

        return True
