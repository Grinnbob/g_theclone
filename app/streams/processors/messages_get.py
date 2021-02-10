import faust
from app.schemas.globals import *

from app.streams import get_stream_app
from app.streams.agents.messages_get_agent import MsgGetAgent
from app.core.config import settings
import traceback
import os

from app.streams.topics.lists import list_update_topic
app = get_stream_app()

@app.agent(list_update_topic)
async def list_update_processor(stream: faust.Stream) -> None:
    msg_get_agent = MsgGetAgent()

    async for change in stream:
        try:
            await msg_get_agent.execute_list_change(change)
        except Exception as e:
            traceback.print_exc()
            print(f"...: list_update_processor error: {str(e)}")


@app.timer(settings.GET_SYNC_PRODUCER_PERIOD, on_leader=True)
async def task_producer():
    msg_get_agent = MsgGetAgent()

    requests = await msg_get_agent.get_requests()
    async for req in requests:
        try:
            await msg_get_agent.produce_task(req)
        except Exception as e:
            traceback.print_exc()
            print(f"..{os.path.basename(__file__)} messages_get_producer ERROR: {str(e)}")


@app.timer(settings.GET_SYNC_PRODUCER_PERIOD, on_leader=True)
async def request_producer():
    msg_get_agent = MsgGetAgent()

    bulks = await msg_get_agent.get_messages()
    async for bulk in bulks:
        try:
            await msg_get_agent.produce_request(bulk)
        except Exception as e:
            traceback.print_exc()
            print(f"..{os.path.basename(__file__)} msg_request_producer ERROR: {str(e)}")

