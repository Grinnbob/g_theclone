from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.addon.test as test_schema
from ..models.addon.test import Test
from ..models.account import Account
from aiogoogle import Aiogoogle
from app.core.config import settings
from app.providers.google.utills import build_client_creds, build_aiogoogle
from bson.objectid import ObjectId
from aiogoogle.auth.creds import UserCreds, ClientCreds

class TestService(BaseService[Test, test_schema.TestCreate, test_schema.TestUpdate]):
    def __init__(self):
        super().__init__(model=Test)

    async def get_test(self,
                        account_id: str,
                        limit: int = 1000) -> Any:

        account = await Account.find_one({'_id' : ObjectId(account_id)})
        if not account:
            raise AppErrors(f"No such account id={account_id}")

        if account.owner_id:
            test = await Test.find_one({'user_id' : account.owner_id})
            return test

        return None

    async def create(self,
                     payload: test_schema.TestCreate) -> Test:

        account = await Account.find_one({'email': payload.email})
        if not account:
            raise AppErrors(f"There is no account email={payload.email}")

        if not account.owner_id:
            raise AppErrors(f"There is no user for account_id={account.id} email={account.email}")

        test = Test(
            title=payload.title,
            data=payload.data,
            user_id=account.owner_id
        )

        await test.commit()
        await test.reload()

        return test
