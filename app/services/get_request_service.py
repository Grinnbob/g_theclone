from app.exceptions import *
from typing import List, Any
from .base import BaseService
import app.schemas.models.gmail_req as req_schema
from app.schemas.globals import *
from .models.gmail_req import GetRequestModel
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class RequestServiceGet(BaseService[GetRequestModel, req_schema.GetReqCreate, req_schema.ReqUpdate]):
    def __init__(self):
        super().__init__(model=GetRequestModel)

    async def get_by_status(self,
                            status: list,
                            list_ids: list = []) -> Any:

        req = {
            'status' : {'$in' : status}
        }
        if list_ids:
            req['list_id'] = {'$in' : list_ids}

        return GetRequestModel.find(req)


    async def create(self,
                        body: req_schema.GetReqCreate) -> GetRequestModel:

        new_request = GetRequestModel(**body)

        await new_request.commit()
        await new_request.reload()

        return new_request


    async def change_status(self,
                            id: str,
                            status: int,
                            error: str = '') -> Any:

        return await GetRequestModel.update_one({ '_id' : ObjectId(id)}, {'$set' : {'status' : status, 'error' : error}})

    async def list_delete(self,
                          list_id: str) -> Any:

        return await GetRequestModel.remove({ 'list_id' : list_id})
