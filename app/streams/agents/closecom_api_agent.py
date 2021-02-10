from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.schemas.topics.closecom_commands import CloseCommandModel
from app.core.config import settings
import traceback
import os

class CloseComApiAgent():
    def __init__(self, api_provider):
        if not api_provider:
            raise AppErrors("CloseComApiAgent ERROR: need an api_provider")

        self.api_provider = api_provider
        self.app = get_stream_app()

    async def execute_command(self,
                              command: CloseCommandModel):
        command_name = command.command
        if command_name == 'list_accounts':
            pass
        elif command_name == 'list_email_sequences':
            pass
        elif command_name == 'list_active_email_sequences':
            pass
        elif command_name == 'list_smartviews':
            pass
        elif command_name == 'bulk_sequence_subscribe':
            pass
        elif command_name == 'bulk_sequence_pause':
            pass
        elif command_name == 'bulk_sequence_resume':
            pass
        else:
            print(f"CloseComApiAgent.execute_command no handler for command_name={command_name} command={command}")
