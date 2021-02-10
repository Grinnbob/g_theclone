from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.account as account_schema
from ..models.closecom.account import CloseComAccount
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class ClosecomAccountService(BaseService[CloseComAccount,
                                         account_schema.AccountCreate,
                                         account_schema.AccountUpdate]):
    def __init__(self):
        super().__init__(model=CloseComAccount)

    async def upsert_many(self,
                          items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"items list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComAccount.collection

            for item in items:
                res = await collection.update_one({'account_id' : item['account_id']},
                                                  { '$set' : {
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"ClosecomAccountService.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def get_by_email(self,
                           email):
        return await CloseComAccount.find_one({'data.email': email})