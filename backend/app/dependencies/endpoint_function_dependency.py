from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
import jwt.algorithms
from jwt.exceptions import InvalidTokenError

from utils.crud_util import Session
from exceptions import TokenInvalidError, ForbiddenError
from custom_types import CurrentUser
from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/1/login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def check_auth(*, access_level: int, get_user: bool = True) -> CurrentUser | None:
    async def func(token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_guid: str = payload.get("sub")
            authority_code: int = payload.get("aut", None)

            if user_guid is None or authority_code is None:
                raise TokenInvalidError

            if authority_code > access_level:
                raise ForbiddenError

            yield None
        except InvalidTokenError:
            raise TokenInvalidError

        if get_user:
            async with Session() as db:
                user = await db.get_user_by_user_guid(user_guid)
                if user is None:
                    raise TokenInvalidError

                setattr(user, "id_token", token)
                yield user

    return func
