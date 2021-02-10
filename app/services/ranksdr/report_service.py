from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.ranksdr.report as report_schema
from ..models.ranksdr.report import RankSdrReport
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class RankSdrReportService(BaseService[RankSdrReport,
                                         report_schema.RankSdrReportCreate,
                                         report_schema.RankSdrReportUpdate]):
    def __init__(self):
        super().__init__(model=RankSdrReport)


    async def save_report(self,
                          data: List[dict]) -> Any:
        res = None
        if not data:
            raise AppErrors(f"data can't be empty")

        try:
            # low level operations start here because of poor implamentation of umongo
            collection = RankSdrReport.collection

            for report in data:
                res = await collection.update_one({'email' : report['email'], 'report_type' : report['report_type']},
                                                  { '$set' : {
                                                      'data' : report['data'],
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"RankSdrReportService.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def load_report(self, email, report_type):
        return await RankSdrReport.find_one({'email': email, 'report_type': report_type})