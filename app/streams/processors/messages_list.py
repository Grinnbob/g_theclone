import faust
from app.schemas.globals import *

from app.streams import get_stream_app
from app.streams.agents.messages_list_agent import MsgListAgent
from app.core.config import settings
import traceback
import os

from app.streams.topics.lists import list_update_topic

app = get_stream_app()

# WE NEED TO MONITOR
@app.agent(list_update_topic)
async def list_update_processor(stream: faust.Stream) -> None:
    msg_list_agent = MsgListAgent()

    async for change in stream:
        try:
            await msg_list_agent.execute_list_change(change)
        except Exception as e:
            traceback.print_exc()
            print(f"...: message_model_update_processor error: {str(e)}")


@app.timer(settings.LIST_SYNC_PRODUCER_PERIOD, on_leader=True)
async def task_producer():
    msg_list_agent = MsgListAgent()

    requests = await msg_list_agent.get_requests()
    async for req in requests:
        try:
            await msg_list_agent.produce_task(req)
        except Exception as e:
            traceback.print_exc()
            print(f"..{os.path.basename(__file__)} messages_list_producer ERROR: {str(e)}")
