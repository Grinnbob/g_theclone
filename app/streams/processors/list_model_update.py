import faust
from app.streams import get_stream_app
from app.streams.agents.list_model_update_agent import ListModelUpdateAgent
from app.schemas.topics.lists import ListModelChange, ListDataTopicModel

from app.streams.topics.lists import list_model_update_topic, list_data_topic
from app.streams.tables.lists import list_data_table, list_stats_table
import traceback

app = get_stream_app()

#GOAL: monitor changes in SyncList table
#send updates to list_data_topic: to initialize list stats, and collect data
#send updates to list_update_topic: to start sync actions based on it

@app.agent(list_model_update_topic)
async def list_model_update_processor(stream: faust.Stream) -> None:
    list_agent = ListModelUpdateAgent()

    async for raw_change in stream:
        try:
            change = ListModelChange.loads(raw_change)
            await list_agent.execute_list_change(change)
        except Exception as e:
            traceback.print_exc()
            print(f"...lists: list_changes_actions error: {str(e)}")
