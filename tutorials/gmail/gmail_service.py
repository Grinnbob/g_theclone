from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import UserCreds, ClientCreds
import json
from config import *

async def get_service(name='gmail', version='v1'):
    async with Aiogoogle() as aiogoogle:
        return await aiogoogle.discover(name, version)

def convert_user_creds(user_creds):
    creds = UserCreds(
        access_token=user_creds.token,
        refresh_token=user_creds.refresh_token,
        expires_at=user_creds.expiry or None,
    )
    return creds

def convert_client_creds(filename):
    client_creds = {}
    with open(filename, 'r') as reader:
        data = reader.read()

        credentials = json.loads(data)
        client_creds = ClientCreds(
            client_id=credentials["installed"]["client_id"],
            client_secret=credentials["installed"]["client_secret"],
            scopes=DEFAULT_SCOPES
        )

    return client_creds