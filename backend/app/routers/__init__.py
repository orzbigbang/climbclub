from .login_router import router as login_router
from .test_router import router as test_router


from fastapi import APIRouter


router = APIRouter()

router.include_router(login_router)
router.include_router(test_router)


import os
from .private import router as private_router
SHOW_PRIVATE_ROUTER = os.getenv("BUILD_ENV", "local") == "local"
router.include_router(router=private_router, include_in_schema=SHOW_PRIVATE_ROUTER)
