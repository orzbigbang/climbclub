from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class UserCreateSchema(BaseModel):
    username: EmailStr
    hashed_password: str


class UserOutSchema(BaseModel):
    id: str
    username: str
    authority_level: int
    created_at: datetime
    update_datetime: datetime | None
