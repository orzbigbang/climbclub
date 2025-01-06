from fastapi import Request
from config import settings
from exceptions import ForbiddenError

from utils import logger


# List of allowed IP addresses
ALLOWED_IPS = settings.ALLOWED_IPS.split(",")


def ip_whitelist(request: Request):
    client_ip = request.client.host
    logger.info({"host": client_ip}, extra="ip_whitelist")
    if "*" in ALLOWED_IPS:
        return

    if client_ip not in ALLOWED_IPS:
        raise ForbiddenError("your ip is not allowed")
