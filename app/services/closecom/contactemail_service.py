from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.contactemail as contactemail_schema
from ..models.closecom.contactemail import CloseComContactEmail
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class CloseComContactEmailService(BaseService[CloseComContactEmail,
                                          contactemail_schema.ContactEmailCreate,
                                          contactemail_schema.ContactEmailUpdate]):
    def __init__(self):
        super().__init__(model=CloseComContactEmail)

    async def upsert_many(self,
                          items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"items list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComContactEmail.collection

            for item in items:
                res = await collection.update_one({'email' : item['email']},
                                                  { '$set' : {
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"CloseComContactEmail.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def get_emails(self,
                           customer=None,
                           limit=1000) -> List[str]:
        match = {}
        if customer:
            match['customer'] = {'$eq' : customer}

        pipeline = [
            {
                '$match': match
            },
            {
                '$limit' : limit
            },
            {
                '$project':
                    {
                        'email': 1
                    }
            },
        ]

        collection = CloseComContactEmail.collection
        return collection.aggregate(pipeline)
