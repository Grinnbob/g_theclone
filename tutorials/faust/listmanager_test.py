import faust
import random

app = faust.App('myapp', broker='kafka://localhost')

list_messages = app.topic('list_messages', internal=True)

list_12_table = app.Table('list_12_table', partitions=1)
list_12_stats = app.Table('list_12_stats', partitions=1)

@app.timer(1)
async def add_message():
    rand_id = int(random.random() * 10)
    email = 'ks.shilov' + str(int(random.random() * 10)) + '@gmail.com'
    incoming = int(random.random() * 10) % 2

    message = {
        'list_id' : 12,
        'email' : email,
        'incoming' : incoming
    }

    await list_messages.send(
        key=str(rand_id),
        value=message
    )

@app.agent(app.topic('list_messages'))
async def list_message_handlers(list_message_stream):
    async for key, data in list_message_stream.items():
        email = data['email']
        incoming = data['incoming']

        new = {
            'sent' : 1,
            'received' : 0
        }
        if incoming:
            new = {
                'sent' : 0,
                'received' : 1
            }
        if not list_12_table.get(email, None):
            list_12_table[email] = new
        else:
            if incoming:
                list_12_table[email]['received'] += 1
            else:
                list_12_table[email]['sent'] += 1

@app.agent(app.topic('list_messages'))
async def table_stats(list_message_stream):
    async for key, data in list_message_stream.items():
        email = data['email']
        incoming = data['incoming']

        total = 0
        if list_12_stats.get('stats', None):
            total = list_12_stats['stats']['total']

        new = {
            'total' : 1,
            'replied' : 0,
            'contacted' : 1
        }
        if incoming:
            new = {
                'total': 1,
                'replied': 1,
                'contacted': 0
            }
        if not list_12_stats.get('stats', None):
            list_12_table['stats'] = new
        else:
            if incoming:
                list_12_table[email]['received'] += 1
            else:
                list_12_table[email]['sent'] += 1


@app.timer(2)
async def show_table():
    print(f'TABLE NOW:\n{list_12_table.as_ansitable()}')
    print(f'TABLE STATS NOW:\n{list_12_stats.as_ansitable()}')