from pydantic import BaseModel, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class EmailForm(BaseModel):
    username: EmailStr
    password: str
    