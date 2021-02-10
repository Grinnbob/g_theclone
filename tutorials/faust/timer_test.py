import faust
import random
import asyncio

app = faust.App('myapp', broker='kafka://localhost')


@app.timer(1)
async def add_message():
    try:
        print("...Timer started")
        await asyncio.sleep(10)
        print("...finished long action")
    except:
        print("...Exception")