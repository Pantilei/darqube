from typing import Union, Literal, Union

from datetime import datetime

from app.models.mongo_model import OID, MongoModel


class UserBase(MongoModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    role: Literal['admin', 'dev', 'simple mortal'] = 'simple mortal'
    is_active: Union[bool, True] = True


class UserCreate(UserBase):
    first_name: str
    last_name: str
    password: str


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: OID
    created_at: datetime
    last_login: Union[datetime, None] = None
    hashed_pass: str


class UserToDB(UserBase):
    id: OID
    created_at: datetime
    last_login: Union[datetime, None] = None
    hashed_pass: str


class User(UserBase):
    id: OID
    created_at: Union[datetime, None] = None
    last_login: Union[datetime, None] = None
