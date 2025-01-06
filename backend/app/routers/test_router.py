from fastapi import APIRouter, status, Depends
from typing import Annotated

from dependencies import Database


router = APIRouter(prefix="/api/1/test", tags=["test"])


@router.get("/")
async def get_data(db: Database):
    res = await db.get_user_base_info('abcd')
    return {"user": res[0], "base_info": res[1]}
