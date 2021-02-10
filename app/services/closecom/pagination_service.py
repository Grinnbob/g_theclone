from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.pagination as pagination_schema
from ..models.closecom.pagination import CloseComPagination
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class CloseComPaginationService(BaseService[CloseComPagination,
                                          pagination_schema.CloseComPaginationCreate,
                                          pagination_schema.CloseComPaginationUpdate]):
    def __init__(self):
        super().__init__(model=CloseComPagination)

    async def reset_pagination(self,
                               endpoint: str):

        exist = await CloseComPagination.find_one({'endpoint' : endpoint})
        if exist:
            await exist.remove()

        return exist

    async def update_page(self,
                          endpoint: str,
                          received: int):
        exist = await CloseComPagination.find_one({'endpoint' : endpoint})
        if not exist:
            exist = CloseComPagination(
                endpoint=endpoint,
                _skip=received
            )
            await exist.commit()
            await exist.reload()

            return exist

        exist._skip = exist._skip + received

        await exist.commit()
        await exist.reload()

        return exist



    async def get_page(self,
                       endpoint: str):

        exist = await CloseComPagination.find_one({'endpoint' : endpoint})
        if not exist:
            exist = CloseComPagination(
                endpoint=endpoint,
                _skip=0
            )
            await exist.commit()
            await exist.reload()

        return exist