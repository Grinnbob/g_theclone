from typing import Optional, Any, List, Type, TypeVar, Union, Dict
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.ranksdr.dialog as dialog_schema
from ..models.ranksdr.dialog import RankSdrDialog
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class RankSdrDialogService(BaseService[RankSdrDialog,
                                         dialog_schema.RankSdrDialogCreate,
                                         dialog_schema.RankSdrDialogUpdate]):
    def __init__(self):
        super().__init__(model=RankSdrDialog)

    async def upsert_many(self,
                          items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"items list can't be empty")

        try:
            # low level operations start here because of poor implamentation of umongo
            collection = RankSdrDialog.collection

            for item in items:
                res = await collection.update_one({'lead_id' : item['lead_id']},
                                                  { '$set' : {
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"RankSdrDialogService.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def load_dialogs(self):
        return RankSdrDialog.find()
