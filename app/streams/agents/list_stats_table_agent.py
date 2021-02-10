from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.schemas.topics.lists import ListDataTopicModel
from app.core.config import settings
import traceback

class LstStatsTableAgent():
    def __init__(self, table):
        if not table:
            raise AppErrors(f"ERROR: LstStatsTableAgent must be initialiaed with stats table")
        self.app = get_stream_app()
        self.stats_table = table

    async def create_list(self,
                          list_id:str):
        if not list_id:
            return

        self.stats_table[list_id] = {}

    async def delete_list(self,
                          list_id:str):
        if not list_id:
            return

        self.stats_table.pop(list_id, None)


    async def add_data(self,
                       data: ListDataTopicModel):
        list_id = data.list_id
        if not list_id:
            raise AppErrors(f"LstStatsTableAgent.add_data ERROR: list_id can't be empty for data={data}")

        email = data.email
        if not email:
            raise AppErrors(f"LstStatsTableAgent.add_data ERROR: email can't be empty for data={data}")

        incoming = data.incoming

        list_stats = self.stats_table.get(list_id, None)
        if not list_stats:
            raise AppErrors(f"LstStatsTableAgent.add_data ERROR: stats never created for list_id={list_id} data={data}")

        # it's the first record ever
        if not list_stats.get('total', None):
            list_stats['replied'] = {}
            list_stats['contacted'] = {}
            list_stats['total'] = {
                'count' : 0,
                'replied' : 0,
                'contacted' : 0
            }

        # it's the first record for the email
        if not list_stats.get(email, None):
            list_stats['total']['count'] += 1
            list_stats[email] = {
                'replied' : 0,
                'contacted' : 0
            }

        if incoming:
            list_stats[email]['replied'] += 1

            # we need only unique replied
            if not list_stats['replied'].get(email, None):
                list_stats['replied'][email] = True
                list_stats['total']['replied'] += 1

        else:
            list_stats[email]['contacted'] += 1

            # we need only unique contacted
            if not list_stats['contacted'].get(email, None):
                list_stats['contacted'][email] = True
                list_stats['total']['replied'] += 1


    async def delete_data(self,
                          data: ListDataTopicModel):

        list_id = data.list_id
        if not list_id:
            raise AppErrors(f"LstStatsTableAgent.delete_data ERROR: list_id can't be empty for data={data}")

        email = data.email
        if not email:
            raise AppErrors(f"LstStatsTableAgent.delete_data ERROR: email can't be empty for data={data}")

        list_stats = self.stats_table.get(list_id, None)
        if not list_stats:
            raise AppErrors(f"LstStatsTableAgent.delete_data ERROR: stats never created for list_id={list_id} data={data}")

        if not list_stats.get(email, None):
            print(f"SRANGE BEHAVOR: trying to add email={email} that there is no ina tanle")
            return

        # This email counted as replied
        if list_stats['replied'].get(email, None):
            list_stats['total']['replied'] -= 1
            list_stats['replied'].pop(email, None)

        if list_stats['contacted'].get(email, None):
            list_stats['total']['contacted'] -= 1
            list_stats['contacted'].pop(email, None)

        list_stats['total']['count'] -= 1
        list_stats.pop(email, None)