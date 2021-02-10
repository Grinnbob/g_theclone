from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.schemas.topics.lists import ListDataTopicModel
from app.core.config import settings
import traceback

class LstDataTableAgent():
    def __init__(self, table):
        if not table:
            raise AppErrors(f"ERROR: LstDataTableAgent must be initialiaed with data table")
        self.app = get_stream_app()
        self.data_table = table

    async def create_list(self,
                          list_id:str):
        if not list_id:
            return

        self.data_table[list_id] = {}

    async def delete_list(self,
                          list_id:str):
        if not list_id:
            return

        self.data_table.pop(list_id, None)

    async def add_data(self,
                       data:ListDataTopicModel):

        list_id = data.list_id
        if not list_id:
            raise AppErrors(f"LstDataTableAgent.add_data ERROR: list_id can't be empty for data={data}")

        email = data.email
        if not email:
            raise AppErrors(f"LstDataTableAgent.add_data ERROR: email can't be empty for data={data}")

        incoming = data.incoming

        list_data = self.data_table.get(list_id)
        if not list_data:
            raise AppErrors(f"LstDataTableAgent.add_data ERROR: there is not list_data for list_id={list_id} data={data}")

        new = {
            'sent': int(not incoming),
            'received': incoming
        }

        if not list_data.get(email, None):
            list_data[email] = new
        else:
            if incoming:
                list_data[email]['received'] += 1
            else:
                list_data[email]['sent'] += 1

    async def delete_data(self,
                          data: ListDataTopicModel):

        list_id = data.list_id
        if not list_id:
            raise AppErrors(f"LstDataTableAgent.delete_data ERROR: list_id can't be empty for data={data}")

        email = data.email
        if not email:
            raise AppErrors(f"LstDataTableAgent.delete_data ERROR: email can't be empty for data={data}")

        list_data = self.data_table.get(list_id)
        if not list_data:
            return

        return list_data.pop(email, None)