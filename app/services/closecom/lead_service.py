from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.lead as lead_schema
from ..models.closecom.lead import CloseComLead
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class ClosecomLeadService(BaseService[CloseComLead,
                                         lead_schema.CloseComLeadCreate,
                                         lead_schema.CloseComLeadUpdate]):
    def __init__(self):
        super().__init__(model=CloseComLead)

    async def upsert_many(self,
                          items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"items list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComLead.collection

            for item in items:
                res = await collection.update_one({'lead_id' : item['lead_id']},
                                                  { '$set' : {
                                                      'status_id' : item['status_id'],
                                                      'status_label' : item['status_label'].lower(),
                                                      'customer' : item['customer'].lower(),
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"ClosecomLeadService.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def get_by_lead_ids(self,
                              lead_ids: List) -> Any:
        return CloseComLead.find({'lead_id' : {'$in' : lead_ids}})

    async def all_leads(self):
        return CloseComLead.find()