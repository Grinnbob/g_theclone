from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.customerstat as customerstat_schema
from ..models.closecom.customerstat import CloseComCustomerStat
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class ClosecomLeadService(BaseService[CloseComCustomerStat,
                                         customerstat_schema.CloseComCustomerStatCreate,
                                         customerstat_schema.CloseComCustomerStatUpdate]):
    def __init__(self):
        super().__init__(model=CloseComCustomerStat)