import faust
from app.schemas.globals import *

from app.streams import get_stream_app
from app.core.config import settings
import traceback
import os
from app.streams.agents.push_updates_agent import PushUpdatesAgent
from app.streams.topics.google_push import push_updates_topic

app = get_stream_app()

@app.timer(settings.PULL_GOOGLE_PERIOD, on_leader=True)
async def pull_updates_producer():
    push_agent = PushUpdatesAgent()

    try:
        messages = await push_agent.pull()

        ack_ids = []
        for ack, data in messages.items():
            try:
                ack = await push_agent.process_gmail_update(ack=ack,
                                                            data=data)
                if ack:
                    ack_ids.append(ack)
            except Exception as e:
                print(f"..{os.path.basename(__file__)} for ERROR: {str(e)}")

        if ack_ids:
            await push_agent.ack(ack_ids=ack_ids)

    except Exception as e:
        traceback.print_exc()
        print(f"..{os.path.basename(__file__)} pull_updates_producer ERROR: {str(e)}")


@app.agent(push_updates_topic)
async def push_updates_processor(stream: faust.Stream) -> None:
    push_agent = PushUpdatesAgent()

    async for update in stream:
        try:
            await push_agent.process_update(update)
        except Exception as e:
            traceback.print_exc()
            print(f"..{os.path.basename(__file__)} push_updates_processor ERROR: {str(e)}")
