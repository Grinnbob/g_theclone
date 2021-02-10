import asyncio
from app.schemas.models.list import ListLabelsChanged
from app.services.list_service import ListService
from bson.objectid import ObjectId

async def change_labels(actions: dict,
                        list_id: str = "5f86ddf0ddb29b201c13ea2c"):
    list_service = ListService()

    changes = ListLabelsChanged(**actions)

    await list_service.change_labels(id=ObjectId(list_id),
                                    actions=changes)

async def main(loop):
    await change_labels(actions={'added' : {'account4' : [1,3]}, 'removed' : {'account4' : [2,5]}})

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()