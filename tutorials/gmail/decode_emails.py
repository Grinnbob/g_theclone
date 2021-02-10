import asyncio
from pprint import pprint
from aiogoogle import Aiogoogle
from aiogoogle.models import Request, Response
from config import *
from gmail_service import get_service, convert_user_creds, convert_client_creds
from google_oauth import get_token
from gmail_api import *
from db import db_connect
from db_routines import *
from urllib3.util import parse_url
import time
import uvloop
import base64
from io import StringIO
from json import JSONDecoder

import aiohttp
import email

from requests_toolbelt.multipart import decoder

USER_CREDS = None
CLIENT_CREDS = None
PAGE_TOKEN = None


async def decode_test(db):
    message = await db['raw_message'].find_one()

    payload = message.get('payload', None)
    data = payload['body']['data']

    print(payload['headers'])

    # DECODE data to string
    decoded = base64.urlsafe_b64decode(data)
    final = decoded.decode('utf-8')
    print(final)


def show_content_type(headers):
    for header in headers:
        name = header.get('name')
        if name == 'Content-Type':
            print(header.get('value'))
            break


def show_headers(headers):
    for header in headers:
        name = header.get('name')
        print(name)


def show_from_to_subject(message, headers):
    found = []
    for header in headers:
        name = header.get('name')
        if name.lower() in ['from', 'to', 'subject']:
            val = header.get('value')
            found.append({name: val})

    if len(found) < 3:
        print(f"....ERROR: not all headers found = {found} for id={message['id']}")
    else:
        pass
        # print(found)


async def decode_num(db, count):
    cursor = db['raw_message'].find().limit(count)
    async for message in cursor:
        payload = message.get('payload', None)
        if not payload:
            print("payload not found")
        else:
            show_from_to_subject(message, payload.get('headers'))


async def get_by_id(db, msg_id):
    res = await db['raw_message'].find_one({'id': msg_id})
    return res


def decode_multipart(msg):
    print(msg)


MULTIPART_ID = '16eea31be63e35ad'


async def main():
    db = db_connect()

    # service = await get_service()
    # await decode_num(database, 100000)
    msg = await get_by_id(db, msg_id=MULTIPART_ID)

    decode_multipart(msg)

    print("...Finished...")


if __name__ == '__main__':
    # USER_CREDS = get_token()
    # USER_CREDS = convert_user_creds(USER_CREDS)

    # CLIENT_CREDS = convert_client_creds('./credentials.json')

    print("....Installing uvloop....")
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    print("....Starting asyncio loop....")
    asyncio.run(main())
