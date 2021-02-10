from app.streams import get_stream_app
from app.schemas.topics.reqres import GmailRequestModel, KeyBase, GmailResponseModel, ParsedKeyBase, GmailParsedResponseModel
from app.core.config import settings

app = get_stream_app()

gmail_request_topic = app.topic('gmail_request_topic', key_type=KeyBase, value_type=GmailRequestModel)
gmail_response_topic = app.topic('gmail_response_topic', key_type=KeyBase, value_type=GmailResponseModel)
gmail_parsed_response_topic = app.topic('gmail_parsed_response_topic', key_type=ParsedKeyBase, value_type=GmailParsedResponseModel)