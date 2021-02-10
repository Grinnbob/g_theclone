import faust
from app.schemas.globals import *

from app.streams import get_stream_app
from app.core.config import settings
import traceback
import os
from app.streams.topics.closecomcommands import closecom_commands_topic
from app.providers.closecom.closecom_api import CloseComApiProvider
from app.streams.agents.closecom_api_agent import CloseComApiAgent
app = get_stream_app()

@app.timer(settings.PULL_CLOSECOM_PERIOD, on_leader=True)
async def closecom_stats_timer():
    try:
        pass
        #push command to get stats to closecom_commands_topic
    except Exception as e:
        traceback.print_exc()
        print(f"..{os.path.basename(__file__)} closecom_stats_timer ERROR: {str(e)}")


@app.agent(closecom_commands_topic)
async def closecom_commands_processor(stream: faust.Stream) -> None:
    api_provider = await CloseComApiProvider.create_api_provider()

    api_session = await api_provider.get_client_session()
    async with api_session as session:
        agent = CloseComApiAgent(api_provider)
        async for command in stream:
            try:
                await agent.execute_command(command=command)
            except Exception as e:
                traceback.print_exc()
                print(f"..{os.path.basename(__file__)} closecom_commands_processor ERROR: {str(e)}")
