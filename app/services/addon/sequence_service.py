from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.addon.sequence as sequence_schema
from ..models.addon.sequence import Sequence
from aiogoogle import Aiogoogle
from app.core.config import settings
from app.providers.google.utills import build_client_creds, build_aiogoogle
from bson.objectid import ObjectId
from aiogoogle.auth.creds import UserCreds, ClientCreds

class SequenceService(BaseService[Sequence, sequence_schema.SequenceCreate, sequence_schema.SequenceUpdate]):
    def __init__(self):
        super().__init__(model=Sequence)

    async def create(self,
                     payload: sequence_schema.SequenceCreate) -> Sequence:

        exist = await Sequence.find_one({'sequence_id': payload.sequence_id})
        if exist:
            raise AppErrors(f"Sequence already exist template_id={payload.sequence_id}")

        data = payload.dict(exclude_unset=True)
        sequence = Sequence(**data)

        await sequence.commit()
        await sequence.reload()

        return sequence
