from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreateSchema(BaseModel):
    username: EmailStr
    authority_level: int = 4
    hashed_password: str


class UserOutSchema(BaseModel):
    user_guid: str
    username: str
    authority_level: int
    insert_datetime: datetime
    update_datetime: datetime
