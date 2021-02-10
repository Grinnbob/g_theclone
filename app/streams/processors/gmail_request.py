import faust
from app.schemas.globals import *

from app.streams import get_stream_app
from app.streams.topics.reqres import gmail_request_topic
from app.streams.agents.gmail_request_agent import GmailRequestAgent
from app.core.config import settings
import traceback

app = get_stream_app()

@app.agent(gmail_request_topic)
async def gmail_requests_actions(stream: faust.Stream):
    req_agent = GmailRequestAgent()

    async for req in stream:
        try:
            await req_agent.execute_request(req)
        except Exception as e:
            traceback.print_exc()
            print(f"..sync: gmail_requests_actions error: {str(e)}")
