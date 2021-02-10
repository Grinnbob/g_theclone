from aiogoogle import Aiogoogle
import asyncio
import json
from google.cloud import pubsub_v1
from google.auth import jwt

GOOGLE_PUB_SUB_TOPIC="projects/outreacher24/topics/theclone-dev"
GOOGLE_PUB_SUB_SUBSCRIPTION_NAME="projects/outreacher24/subscriptions/gmail-updates-dev"


class Test():
    def __init__(self):
        self.x = 12

    def _no_args(self):
        with open('./theclone_pub_sub_key_dev.json') as f:
            print(f"..._no_args, x={self.x}")

        return self.x

    def _args(self, a):
        with open('./theclone_pub_sub_key_dev.json') as f:
            print(f"..._args, x={self.x} a={a}")

    async def pull(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._no_args)

    async def ack(self, ids):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._args, ids)


async def main():
    t = Test()

    #res = await t.pull()
    #print(f"..res={res}")

    res = await t.ack(ids=[1,2,3])
    print(f"..res={res}")

if __name__ == '__main__':
    asyncio.run(main())


# def explicit():
#     service_account_info = json.load(open("./theclone_pub_sub_key_dev.json"))
#     audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
#
#     credentials = jwt.Credentials.from_service_account_info(
#         service_account_info, audience=audience
#     )
#
#     return credentials
#
#
# credentials = explicit()
# subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
#
# def call_pull():
#     with subscriber:
#         # The subscriber pulls a specific number of messages.
#         response = subscriber.pull(subscription=GOOGLE_PUB_SUB_SUBSCRIPTION_NAME,
#                                    max_messages=2)
#
#         ack_ids = []
#         for received_message in response.received_messages:
#             print(f"Received: {received_message.message.data}.")
#             ack_ids.append(received_message.ack_id)
#
#         # Acknowledges the received messages so they will not be sent again.
#         subscriber.acknowledge(subscription=GOOGLE_PUB_SUB_SUBSCRIPTION_NAME, ack_ids=ack_ids)
#
#         print(
#             f"Received and acknowledged {len(response.received_messages)} messages from {GOOGLE_PUB_SUB_SUBSCRIPTION_NAME}."
#         )
#
# async def async_call_pull():
#     loop = asyncio.get_event_loop()
#     # start time.sleep(x) in a separate thread, suspend
#     # the current coroutine, and resume when it's done
#     return await loop.run_in_executor(None, call_pull)
#


#api: https://www.googleapis.com/discovery/v1/apis/pubsub/v1/rest


#API_KEY="AIzaSyC229lBnY3CYLE5z0Qypx5YT_FikRTwPbA"   # NOT SUPPORTED BY pub/sub API

#async def build_service(name, version):
#    async with Aiogoogle() as aiogoogle:
#        return await aiogoogle.discover(name, version)

#async def main():
#    service = await build_service(name="pubsub", version="v1")

#    async with Aiogoogle(api_key=API_KEY) as g:
#        request = service.projects.subscriptions.pull(subscription=GOOGLE_PUB_SUB_SUBSCRIPTION_NAME)

#        res = await g.as_api_key(request, full_res=True)
#        print(res)

#if __name__ == '__main__':
#    asyncio.run(main())
