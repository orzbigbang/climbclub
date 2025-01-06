from fastapi import Request
from time import time
from datetime import datetime, timedelta

from utils.logger_util import logger


class TimeRecorder:
    def __init__(self):
        pass

    async def __call__(self, request: Request, call_next):
        st = time()
        logger.info({"start_time_jst": self.get_current_local_time_isoformat()}, extra={"api_call": request.url.path})
        response = await call_next(request)
        ed = time()
        duration = f"{ed - st:.5f}"
        logger.info({"end_time_jst": self.get_current_local_time_isoformat(), "duration": duration}, extra={"api_call": request.url.path})
        return response

    @staticmethod
    def get_current_local_time_isoformat() -> str:
        return (datetime.now() + timedelta(hours=9)).isoformat()
