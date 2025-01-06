from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from exceptions import AuthorizationError
from schemas.auth import TokenSchema
from schemas.user import UserCreateSchema, UserOutSchema
from dependencies import Database
from utils.auth_util import create_access_token, authenticate_user, get_password_hash


router = APIRouter(prefix="/api/1/account", tags=["login"])


@router.post(path="/login",
             response_model=TokenSchema,
             status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise AuthorizationError("Incorrect username or password")

    token_data = {"sub": user.user_guid, "aut": user.authority_level}

    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(path="/signup",
             response_model=UserOutSchema)
async def main(
        db: Database,
        body_user: UserCreateSchema,
):
    body_user.hashed_password = get_password_hash(body_user.hashed_password)
    return await db.add_user(body_user)

