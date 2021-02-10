from app.exceptions import *
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import UserCreds, ClientCreds
from app.core.config import settings
import json
async def build_service(name, version):
    async with Aiogoogle() as aiogoogle:
        return await aiogoogle.discover(name, version)

def build_user_creds(user_creds):
    creds = UserCreds(
        access_token=user_creds['access_token'],
        refresh_token=user_creds['refresh_token'],
        expires_at=user_creds.get('expires_at'),
    )

    return creds

def build_client_creds(client_creds, scopes, redirect_url=None):
    redirect_url=redirect_url
    if not redirect_url:
        redirect_url = settings.GOOGLE_OAUTH_MAJOR_REDIRECT_URL

    creds = ClientCreds(
        client_id=client_creds["client_id"],
        client_secret=client_creds["client_secret"],
        redirect_uri=redirect_url,
        scopes=scopes
    )

    return creds

def build_aiogoogle(redirect_url=None):
    client_creds = build_client_creds(client_creds=settings.GOOGLE_CLIENT_SETTINGS['credentials'],
                                      scopes=settings.GOOGLE_CLIENT_SETTINGS['gmail_scopes'],
                                      redirect_url=redirect_url)

    return (client_creds, Aiogoogle(client_creds=client_creds))
