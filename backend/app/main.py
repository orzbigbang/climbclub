from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from contextlib import asynccontextmanager
from typing import Any
import orjson

from middlewares import *
from config import settings
from utils.logger_util import logger


# startup and end event
# add startup event before yield clause
# add end event after yield clause
@asynccontextmanager
async def lifespan(__app: FastAPI):
    import asyncio
    logger.info(f"Using event loop: {asyncio.get_running_loop()}")

    # create db tables and metadata
    import socket
    from database import Base, engine
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except socket.gaierror as e:
        logger.warning(f"db disconnected. error message: {e}")

    # check redis connection
    try:
        if settings.SETTING.USE_REDIS:
            client = redis.from_url(f"redis://{settings.REDIS_HOST}", decode_responses=True)
            client.ping()
            logger.info("redis connection SUCCEEDED. using redis to cache")

            # preload redis cache here
            if settings.SETTING.PRELOAD_REDIS:
                from utils.redis_util import preload_redis
                await asyncio.get_running_loop().create_task(preload_redis())
        else:
            logger.warning("USE_REDIS setting is False. no-redis cache")

    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
        settings.SETTING.USE_REDIS = False
        logger.error("redis connection FAILED. no-redis cache")

    yield


# custom default response type
class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(jsonable_encoder(content), option=orjson.OPT_NON_STR_KEYS | orjson.OPT_OMIT_MICROSECONDS)


app = FastAPI(lifespan=lifespan, default_response_class=CustomORJSONResponse)


# custom exception
@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    logger.error({
            'error_message': exc.detail,
            'step': 'send_back_error',
            'returned_status_code': exc.status_code,
        }, extra=request.url.path)
    return CustomORJSONResponse(
        status_code=exc.status_code,
        content={"msg": exc.detail},
        headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error({"detail": exc.errors(),
                  "body": exc.body}, extra="request_body_validation")
    return CustomORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"step": "request_body_validation",
                 "detail": exc.errors(),
                 "body": exc.body},
    )


@app.exception_handler(redis.exceptions.ConnectionError)
async def redis_exception_handler_1(request: Request, exc: redis.exceptions.ConnectionError):
    logger.error({"detail": "redis connection error"}, extra=request.url.path)
    settings.SETTING.USE_REDIS = False


@app.exception_handler(redis.exceptions.TimeoutError)
async def redis_exception_handler_2(request: Request, exc: redis.exceptions.TimeoutError):
    logger.error({"detail": "redis timeout error"}, extra=request.url.path)
    settings.SETTING.USE_REDIS = False


# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(RouteDistributor())
app.middleware("http")(AddHeader())
app.middleware("http")(TimeRecorder())


# routers
from routers import router
app.include_router(router=router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8088, reload=True)
