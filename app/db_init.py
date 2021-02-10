from app.services.models import instance
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
import asyncio
from app.database import get_db

from app.services.models.list import SyncList
from app.services.models.user import User
from app.services.models.account import Account

from app.services.models.addon.template import Template
from app.services.models.addon.sequence import Sequence
from app.services.models.addon.test import Test

from app.services.models.closecom.subscription import CloseComSubscription
from app.services.models.closecom.account import CloseComAccount
from app.services.models.closecom.sequence import CloseComSequence
from app.services.models.closecom.dailylaunch import CloseComDailyLaunch, CloseComSmartView

from app.services.models.closecom.pagination import CloseComPagination
from app.services.models.closecom.contactemail import CloseComContactEmail

from bson.objectid import ObjectId

db = get_db()
instance.init(db)

async def _ensure_index():
    await SyncList.ensure_indexes()
    await User.ensure_indexes()
    await Account.ensure_indexes()
    await Template.ensure_indexes()
    await Sequence.ensure_indexes()
    await Test.ensure_indexes()

    await CloseComSubscription.ensure_indexes()
    await CloseComAccount.ensure_indexes()
    await CloseComSequence.ensure_indexes()
    await CloseComDailyLaunch.ensure_indexes()
    await CloseComSmartView.ensure_indexes()

    await CloseComPagination.ensure_indexes()
    await CloseComContactEmail.ensure_indexes()

async def add_sync_list_item():
    item = SyncList(
            owner_id=ObjectId("5f75d8a2e0bb55e2040b461f"),
            title="Random title",
            account_labels= {'account1' : [1,2,3], 'account2':[4,5,6]})
    await item.commit()

async def main(loop):
    await _ensure_index()
    #await add_sync_list_item()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()