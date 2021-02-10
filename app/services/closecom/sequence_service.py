from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.sequence as sequence_schema
from ..models.closecom.sequence import CloseComSequence
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class CloseComSequenceService(BaseService[CloseComSequence,
                                          sequence_schema.CloseComSequenceCreate,
                                          sequence_schema.CloseComSequenceUpdate]):
    def __init__(self):
        super().__init__(model=CloseComSequence)

    async def upsert_many(self,
                          items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"items list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComSequence.collection

            for item in items:
                res = await collection.update_one({'sequence_id' : item['sequence_id']},
                                                  { '$set' : {
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"ClosecomSequenceService.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def get_by_name(self,
                          name: str) -> Any:
        return await CloseComSequence.find_one({'data.name' : name})

    async def get_by_id(self,
                          sequence_id: str) -> Any:
        return await CloseComSequence.find_one({'sequence_id' : sequence_id})

    async def sequence_id_to_name(self):
        cursor = CloseComSequence.find()

        all_sequences = {}
        async for sq in cursor:
            all_sequences[sq.sequence_id] = sq.data.get('name')

        return all_sequences
