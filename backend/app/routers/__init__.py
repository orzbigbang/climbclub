from .login import router as login_router
from .openai import router as openai_router
from .user import router as user_router

from config import settings

from fastapi import APIRouter


router = APIRouter(prefix=f"/api/{settings.CONST.API_VER}")

router.include_router(login_router, prefix="/account", tags=["login"])
router.include_router(openai_router, prefix="/openai", tags=["openai"])
router.include_router(user_router, prefix="/users", tags=["user"])

import os
from .private import router as private_router
SHOW_PRIVATE_ROUTER = os.getenv("BUILD_ENV", "local") == "local"
router.include_router(router=private_router, include_in_schema=SHOW_PRIVATE_ROUTER)
