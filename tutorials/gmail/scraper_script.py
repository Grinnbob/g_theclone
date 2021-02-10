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

from io import StringIO
from json import JSONDecoder

import aiohttp
import email

from requests_toolbelt.multipart import decoder

USER_CREDS = None
CLIENT_CREDS = None
PAGE_TOKEN = None

M1 = '174788a926d75917'
M2 = '174788955755acb5'


async def show_stats(db):
    count = 1000000

    res = db[STRUCTURED_DATA].find({'status': STATUS_RAW_SAVED})
    total = await res.to_list(length=count)
    print(f"....FINSIHED with STATUS_RAW_SAVED={len(total)}")

    broken = db[STRUCTURED_DATA].find({'status': STATUS_QUARANTINE})
    total = await broken.to_list(length=count)
    print(f"....FINSIHED with STATUS_QUARANTINE={len(total)}")


async def on_init(db):
    await remove_quarantene(db)

    await delete_broken(db)

    await fix_statuses(db)


async def remove_quarantene(db):
    await db[STRUCTURED_DATA].update_many({'status': STATUS_QUARANTINE}, {'$set': {'status': STATUS_READY}})


async def main():
    if not USER_CREDS:
        raise Exception(f"ERROR: user_creds={USER_CREDS}, call get_token first")

    db = db_connect()

    await on_init(db)

    service = await get_service()

    i = 0
    shit_count = 1
    while True:
        try:
            start_time = time.time()

            i = i + 1
            ids = await get_ids(db)
            if (len(ids)) <= 0:
                print("...No more ids")
                exit(0)
            print(f"...{i} Batch request ids count={len(ids)}")

            req_list = get_batch_requests_list(service, ids)

            req_tasks = [
                get_batch_response(Aiogoogle(user_creds=USER_CREDS, client_creds=CLIENT_CREDS), r) for r in req_list
            ]

            resp_list = await asyncio.gather(*req_tasks, return_exceptions=True)

            broken = True
            for n_resp in resp_list:
                if isinstance(n_resp, Response):
                    broken = False
                    break

            if broken:
                print(f"....Shit happened {shit_count} time... RESTARTING")
                shit_count = shit_count + 1
                await asyncio.sleep(120)

                await on_init(db)
                continue

            resp_tasks = [
                save_batch_response(db, r) for r in resp_list
            ]

            await asyncio.gather(*resp_tasks, return_exceptions=True)
            await show_stats(db)

            exec_time = time.time() - start_time
            print(f"...pause executing: {exec_time}")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"...Error {str(e)}")
            continue

    print("...Finished...")


if __name__ == '__main__':
    USER_CREDS = get_token()
    USER_CREDS = convert_user_creds(USER_CREDS)

    CLIENT_CREDS = convert_client_creds('./credentials.json')

    print("....Installing uvloop....")
    # uvloop.install()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    print("....Starting asyncio loop....")
    asyncio.run(main())
