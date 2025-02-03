from fastapi import APIRouter, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from schemas.auth import TokenSchema
from schemas.user import UserCreateSchema, UserOutSchema
from dependencies import Database, FormData, check_refresh_token
from utils.auth_util import create_access_token, create_refresh_token, authenticate_user, get_password_hash, RSA_PUBLIC_KEY
from exceptions import AuthorizationError


router = APIRouter()


@router.post(path="/login",
             response_model=TokenSchema,
             status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: FormData,
):
    username, password = form_data
    user = await authenticate_user(username, password)
    if user is None:
        raise AuthorizationError("username or password is incorrect")

    token_data = {"sub": user.id, "username": user.username, "aut": user.authority_level, "created_at": user.created_at}

    access_token = create_access_token(jsonable_encoder(token_data))
    refresh_token = create_refresh_token(jsonable_encoder(token_data))

    # 设置cookie
    response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token,
        httponly=False,  # 允许前端JavaScript访问cookie
        secure=True,    # HTTPS安全传输
        samesite=None, # 允许跨站点GET请求
        max_age=60 * 60 * 24 * 7,  # 7天
        domain=None,  # 使用当前域名
        path="/"      # 根路径
    )

    return response


@router.get(path="/publickey")
async def get_public_key():
    return Response(content=RSA_PUBLIC_KEY, media_type="text/plain")


@router.post(path="/signup",
             response_model=UserOutSchema)
async def register_user(
        db: Database,
        form_data: FormData,
):
    username, password = form_data
    body_user = UserCreateSchema(username=username, hashed_password=get_password_hash(password))
    await db.add_user(body_user)
    await db.commit()

    return await login_for_access_token((username, password))

@router.post(path="/refresh_token")
async def refresh_token(
    refresh_token_payload: Annotated[dict, Depends(check_refresh_token)]
):
    access_token = create_access_token(jsonable_encoder(refresh_token_payload))
    
    return {"access_token": access_token, "token_type": "bearer"}
