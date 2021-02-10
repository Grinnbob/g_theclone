import faust
import random
import string

app = faust.App('myapp', broker='kafka://localhost')

raw_message_topic = app.topic('raw_messages')
tokenized_message_topic = app.topic('tokenized_messages')

async def fetch_message():
    message = {
        'id' : str(int(random.random() * 1000000)),
        'payload' : ''.join(random.choice(string.ascii_letters) for _ in range(1000))
    }

    return message

@app.timer(3)
async def generate_messages1():
    message = await fetch_message()

    message_data = {
        'id' : message['id'],
        'data' : "Body should be here"
    }

    await raw_message_topic.send(
        key=message_data['id'],
        value=message_data
    )

@app.agent(app.topic('raw_messages'))
async def tokenize_message(message_stream):
    async for key, data in message_stream.items():
        mod_data = data['data'] + "aa"

        new_data = {
            'probability' : 1,
            'mod_data' : mod_data
        }
        await tokenized_message_topic.send(
            key=key,
            value=new_data
        )
