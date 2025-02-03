from fastapi import APIRouter, status
import time

from dependencies import Database
from exceptions import NotFoundError

router = APIRouter()

@router.get(path="/exists",
            status_code=status.HTTP_200_OK)
async def has_user(
    username: str,
    db: Database
):
    user = await db.get_user_by_username(username)
    if user is None:
        raise NotFoundError("user not found")
    