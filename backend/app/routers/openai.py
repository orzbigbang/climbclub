from fastapi import APIRouter, status, Depends
from typing import Annotated

from dependencies import Database


router = APIRouter()


@router.post("/message")
async def post_message(msg: str):
    return f"你输入了{msg}"
