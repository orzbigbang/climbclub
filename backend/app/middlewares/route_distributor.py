from fastapi import Request, status
from fastapi.responses import JSONResponse

from config import settings


class RouteDistributor:
    def __init__(self):
        self.health_check_endpoint = f"/api/{settings.CONST.API_VER}/ping"
        self.health_check_response = JSONResponse({"status": "OK"}, status.HTTP_200_OK)

    async def __call__(self, request: Request, call_next):
        path = request.url.path

        if path == self.health_check_endpoint:
            return self.health_check_response

        response = await call_next(request)
        return response
