from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from app.exceptions import *
from .base import BaseService
import app.schemas.models.user as user_schema
from .models.user import User
from pymongo.errors import DuplicateKeyError
from marshmallow.exceptions import ValidationError
from bson.objectid import ObjectId
from app.core.security import get_password_hash, verify_password

class UserService(BaseService[User, user_schema.UserRegister, user_schema.UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def create(self,
                     obj_in: user_schema.UserRegister) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password)
        )

        try:
            await db_obj.commit()

            await db_obj.reload()
        except ValidationError as e:
            raise AppValidationError(original=e,
                                        message="User already exist")

        return db_obj

    async def get_by_id(self,
                        user_id: str) -> User:
        return await User.find_one({'_id' : ObjectId(user_id)})

    async def get_by_email(self,
                           email : str) -> Optional[User]:
        return await User.find_one({ 'email' : email})

    async def authenticate(self,
                           obj_in: user_schema.UserLogin) -> Optional[User]:

        user = await self.get_by_email(email=obj_in.email)
        if not user:
            raise AppErrors("No such user")

        if not verify_password(obj_in.password, user.hashed_password):
            raise AppErrors("Wrong password")

        return user

    async def update_oauth_state(self,
                                 user:User,
                                 state:str) -> User:
        if not state:
            raise AppErrors("State can't be empty")

        user.oauth_state = state

        await user.commit()
        await user.reload()

        return user


    async def get_by_state(self,
                           state:str) -> User:
        if not state:
            raise AppErrors("State can't be empty")

        return await User.find_one({'oauth_state': state})
