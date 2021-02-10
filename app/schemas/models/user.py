from typing import Optional
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Schema
from .base import DBModelMixin
from datetime import datetime


# Major idea:
# THREE Schemas always exist:
#    * Base - contain all fields that can be shared outside. Also mark required fields
#    * DbBase - has id with a type
#    * InDb - inherit both. Should be used in all returns

# 1. For create schema - inherit Base and add password fields
# 2. For update schema - inherit DbBase and put all fields optional

# For update and return from create: need to have ID
# Base fields for user that we can return
class UserBase(BaseModel):
    email: EmailStr

class UserLogin(UserBase):
    password: str

    @validator('email')
    def email_match(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Email can't be empty")

        return v

    @validator('password')
    def password_match(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Passowrd  can't be emapty")

        return v

class UserRegister(UserBase):
    password: str
    password_repeat: str

    @validator('password_repeat')
    def passwords_match(cls, v, values, **kwargs):
        if (not v) or ('password' not in values):
            raise ValueError("password can't be empty")

        if v != values['password']:
            raise ValueError('passwords do not match')

        return v


class UserUpdate(BaseModel):
    password: str
    password_repeat: str

    @validator('password_repeat')
    def passwords_match(cls, v, values, **kwargs):
        if (not v) or ('password' not in values):
            raise ValueError("password can't be empty")

        if v != values['password']:
            raise ValueError('passwords do not match')

        return v

class UserInDB(DBModelMixin, UserBase):
    pass

class UserAddonProfile(BaseModel):
    level: int = 0
    is_logged: int = 0
    stats: dict = {}
    tests: dict = {}
