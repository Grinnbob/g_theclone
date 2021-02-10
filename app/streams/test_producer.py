from app.streams import get_stream_app
from app.schemas.topics.lists import ListDataTopicModel

from app.streams.topics.lists import list_data_topic
from app.streams.tables.lists import list_data_table, list_stats_table
import random

app = get_stream_app()

LIST_ID = '5f7c8841b077ea9783aa71e1'

@app.timer(1)
async def add_message():
    rand_id = int(random.random() * 10)
    email = 'ks.shilov' + str(int(random.random() * 10)) + '@gmail.com'
    incoming = int(random.random() * 10) % 2

    message = ListDataTopicModel(
        action='update',
        list_id=LIST_ID,
        email=email,
        incoming=incoming
    )

    await list_data_topic.send(
        key=str(rand_id),
        value=message
    )

@app.timer(2)
async def show_table():
    print(f'TABLE NOW:\n{list_data_table.as_ansitable()}')
    print(f'TABLE STATS NOW:\n{list_stats_table.as_ansitable()}')

if __name__ == '__main__':
    app = get_stream_app()

    app.main()

#TEST IT

# LIST_ID = '5f7c8841b077ea9783aa71e1'
#
# @app.timer(1)
# async def add_message():
#     rand_id = int(random.random() * 10)
#     email = 'ks.shilov' + str(int(random.random() * 10)) + '@gmail.com'
#     incoming = int(random.random() * 100) % 2
#
#     message = ListDataTopicModel(
#         action='update',
#         list_id=LIST_ID,
#         email=email,
#         incoming=incoming
#     )
#
#     await list_data_topic.send(
#         key=str(rand_id),
#         value=message
#     )
#
# @app.timer(2)
# async def show_table():
#     print(f'TABLE NOW:\n{list_data_table.as_ansitable()}')
#     print(f'TABLE STATS NOW:\n{list_stats_table.as_ansitable()}')
