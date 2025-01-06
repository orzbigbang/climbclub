from fastapi import Depends
from typing import Annotated

from utils.crud_util import Session, get_session
from .endpoint_function_dependency import check_auth
from custom_types import CurrentUser


Database = Annotated[Session, Depends(get_session)]

ExternalUser = Annotated[CurrentUser, Depends(check_auth(access_level=4))]
InternalUser = Annotated[CurrentUser, Depends(check_auth(access_level=3))]
AdminUser = Annotated[CurrentUser, Depends(check_auth(access_level=0))]

ExternalAccess = Annotated[None, Depends(check_auth(access_level=4, get_user=False))]
InternalAccess = Annotated[None, Depends(check_auth(access_level=3, get_user=False))]
AdminAccess = Annotated[None, Depends(check_auth(access_level=0, get_user=False))]
