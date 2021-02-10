from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.zerobounce.emailcheck as emailcheck_schema
from ..models.zerobounce.emailcheck import ZerobounceEmailCheck
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class ZerobounceStatusCheckService(BaseService[ZerobounceEmailCheck,
                                          emailcheck_schema.ZerobounceEmailCheckCreate,
                                          emailcheck_schema.ZerobounceEmailCheckUpdate]):
    def __init__(self):
        super().__init__(model=ZerobounceEmailCheck)

    async def upsert_many(self,
                          items: List[dict],
                          status: str) -> Any:
        res = None
        if not items:
            raise AppErrors(f"items list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = ZerobounceEmailCheck.collection

            for item in items:
                res = await collection.update_one({'email' : item['email']},
                                                  { '$set' : {
                                                      'status' : status,
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"ZerobounceEmailCheck.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

