from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from aiogoogle import Aiogoogle
from app.core.config import settings
from app.providers.google.utills import build_client_creds, build_aiogoogle
from bson.objectid import ObjectId
from app.database import get_db
from app.services.models import instance, Base
from app.services.models.account import Account
from app.services.models.user import User
from app.services.models.addon.sequence import Sequence
from app.services.models.addon.template import Template
from app.services.models.addon.test import Test

class AdminDashboardService():
    def __init__(self):
        initialized = False
        try:
            exist = instance.db
            if exist:
                initialized = True
        except Exception as e:
            initialized = False
            self.db = None

        if not initialized:
            self.db = get_db()
            instance.init(self.db)

####################################################################################
######################## SHOW GET methods ##########################################
####################################################################################
    async def get_templates(self,
                            limit: int = 1000):
        cursor = Template.find().limit(limit)
        return list(await cursor.to_list(length=limit))

    async def get_users(self,
                        limit: int = 1000):
        cursor = User.find().limit(limit)
        return list(await cursor.to_list(length=limit))

    async def get_accounts(self,
                           limit: int = 1000):

        cursor = Account.find().limit(limit)
        return list(await cursor.to_list(length=limit))

    async def get_sequences(self,
                            limit: int = 1000):
        cursor = Sequence.find().limit(limit)
        return list(await cursor.to_list(length=limit))


    async def get_tests(self,
                        limit: int = 1000):
        cursor = Test.find().limit(limit)
        return list(await cursor.to_list(length=limit))

####################################################################################
######################## CHANGE   methods ##########################################
####################################################################################
    async def change_account_status(self,
                                    account_id: str,
                                    active:bool):
        exist = await Account.find_one({'_id' : ObjectId(account_id)})
        if not exist:
            raise AppErrors(f"No such account {account_id}")

        exist.active = active

        await exist.commit()
        await exist.reload()

        return exist

    async def connect_account(self,
                              account_id: str,
                              user_id: str) -> Any:

        user = await User.find_one({'_id' : ObjectId(user_id)})
        if not user:
            raise AppErrors(f"No such user {user_id}")

        account = await Account.find_one({'_id' : ObjectId(account_id)})
        if not account:
            raise AppErrors(f"No such account {account_id}")

        account.owner_id = user.id

        await account.commit()
        await account.reload()

        return account



    async def disconnect_account(self,
                                 account_id: str,
                                 user_id: str) -> Any:

        account = await Account.find_one({'_id': ObjectId(account_id)})
        if not account:
            raise AppErrors(f"No such account {account_id}")

        account.owner_id = None

        await account.commit()
        await account.reload()

        return account

    async def edit_template(self,
                            template_id: str,
                            data: dict):
        template = await Template.find_one({'_id' : ObjectId(template_id)})
        if not template:
            raise AppErrors(f"template doesn't exist id={template_id}")

        current_data = {}
        if template.data:
            current_data = template.data.to_mongo()

        changed = False
        for k, v in data.items():
            if k and v:
                current_data[k] = v
                changed = True

        if changed:
            template.data = current_data
            await template.commit()
            await template.reload()

        return template


    async def change_template_status(self,
                                     template_id: str,
                                     active: bool):
        template = await Template.find_one({'_id' : ObjectId(template_id)})
        if not template:
            raise AppErrors(f"template doesn't exist id={template_id}")

        template.active = active

        await template.commit()
        await template.reload()

        return template

    async def edit_sequence(self,
                            sequence_id: str,
                            data: dict):
        sequence = await Sequence.find_one({'_id' : ObjectId(sequence_id)})
        if not sequence:
            raise AppErrors(f"sequence doesn't exist id={sequence_id}")

        current_data = {}
        if sequence.data:
            current_data = sequence.data.to_mongo()

        changed = False
        for k, v in data.items():
            if k and v:
                current_data[k] = v
                changed = True

        if changed:
            sequence.data = current_data
            await sequence.commit()
            await sequence.reload()

        return sequence


    async def change_sequence_status(self,
                                     sequence_id: str,
                                     active: bool):
        sequence = await Sequence.find_one({'_id' : ObjectId(sequence_id)})
        if not sequence:
            raise AppErrors(f"sequence doesn't exist id={sequence_id}")

        sequence.active = active

        await sequence.commit()
        await sequence.reload()

        return sequence


    async def change_user_level(self,
                           user_id: str,
                           level: int):

        user = await User.find_one({'_id' : ObjectId(user_id)})
        if not user:
            raise AppErrors(f"user doesn't exist id={user_id}")

        custom_info = {}
        if user.custom_info:
            custom_info = user.custom_info.to_mongo()

        custom_info['level'] = level
        user.custom_info = custom_info

        await user.commit()
        await user.reload()

        return user


    async def connect_template(self,
                               template_id: str,
                               account_ids: List[str],
                               to_all:bool = False,
                               limit:int = 1000):

        if (not to_all) and (not account_ids):
            raise AppErrors(f"specify account_ids for template_id={template_id}")

        template = await Template.find_one({'_id' : ObjectId(template_id)})
        if not template:
            raise AppErrors(f"there is not such template={template_id}")

        current_accounts = []
        if template.accounts:
            current_accounts = template.accounts.to_mongo()

        if to_all:
            cursor = Account.find().limit(limit)
            items = list(await cursor.to_list(length=limit))

            ids = [str(l['_id']) for l in items]
            if not ids:
                raise AppErrors(f"There is not accounts in the system")

            current_accounts.extend(ids)
        else:
            current_accounts.extend(account_ids)


        unique_accounts = set(current_accounts)
        template.accounts = list(unique_accounts)

        await template.commit()
        await template.reload()

        return template


    async def disconnect_template(self,
                                  template_id:str,
                                  account_ids: List[str],
                                  from_all: bool = False):

        if (not from_all) and (not account_ids):
            raise AppErrors(f"specify account_ids for template_id={template_id}")

        template = await Template.find_one({'_id' : ObjectId(template_id)})
        if not template:
            raise AppErrors(f"there is not such template={template_id}")

        current_accounts = []
        if template.accounts:
            current_accounts = template.accounts.to_mongo()

        if from_all:
            current_accounts = []
        else:
            current_accounts = [item for item in current_accounts if item not in account_ids]

        unique_accounts = set(current_accounts)
        template.accounts = list(unique_accounts)

        await template.commit()
        await template.reload()

        return template


####################################################################################
######################## Clients methods   #########################################
####################################################################################
    async def upload_csv(self,
                         csv):
        pass
####################################################################################
######################## CLOSE.com METHODS #########################################
####################################################################################
    async def send_sequence(self,
                              sequence_id: str):
        pass

    async def send_leads(self,
                           upload_id: str):
        pass