import faust
from app.schemas.globals import *
from app.exceptions import *
from app.streams import get_stream_app
from app.core.config import settings
import traceback

from app.schemas.topics.message import MessageModelChange

from app.streams.topics.lists import list_data_topic
from app.streams.topics.message import message_model_update_topic
from app.streams.tables.lists import list_data_table, list_stats_table

from app.streams.agents.list_data_table_agent import LstDataTableAgent
from app.streams.agents.list_stats_table_agent import LstStatsTableAgent
from app.streams.agents.message_model_update_agent import MsgModelUpdateAgent


app = get_stream_app()


# WE NEED TO MONITOR
@app.agent(message_model_update_topic)
async def message_model_update_processor(stream: faust.Stream) -> None:
    msg_update_agent = MsgModelUpdateAgent()

    async for raw_change in stream:
        try:
            change = MessageModelChange.loads(raw_change)
            await msg_update_agent.execute_message_change(change)
        except Exception as e:
            traceback.print_exc()
            print(f"...: message_model_update_processor error: {str(e)}")



@app.agent(list_data_topic)
async def list_table_data_processor(stream: faust.Stream) -> None:
    data_agent = LstDataTableAgent(list_data_table)
    async for data in stream:
        try:
            if data.action == 'insert':
                await data_agent.create_list(list_id=data.list_id)
            elif data.action == 'delete':
                await data_agent.delete_list(list_id=data.list_id)
            elif data.action == 'add_data':
                await data_agent.add_data(data=data)
            elif data.action == 'delete_data':
                await data_agent.delete_data(data=data)
            else:
                raise AppErrors(f"list_table_data_processor ERROR: unknown action={data.action} for data={data}")
        except Exception as e:
            traceback.print_exc()
            print(f"...lists: list_id_data_stream error: {str(e)}")


@app.agent(list_data_topic)
async def list_table_stats_processor(stream: faust.Stream) -> None:
    stats_agent = LstStatsTableAgent(list_stats_table)
    async for data in stream:
        try:
            if data.action == 'insert':
                await stats_agent.create_list(list_id=data.list_id)
            elif data.action == 'delete':
                await stats_agent.delete_list(list_id=data.list_id)
            elif data.action == 'add_data':
                await stats_agent.add_data(data=data)
            elif data.action == 'delete_data':
                await stats_agent.delete_data(data=data)
            else:
                raise AppErrors(f"list_table_data_processor ERROR: unknown action={data.action} for data={data}")
        except Exception as e:
            traceback.print_exc()
            print(f"...lists: list_id_stats_stream error: {str(e)}")
