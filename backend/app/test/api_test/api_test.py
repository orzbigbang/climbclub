import sys
from pathlib import Path
import asyncio
from httpx import Response

sys.path.append(Path.cwd().__str__())
from api_mapping import API_MAPPING, BaseAPITest, Meta


class APITest(BaseAPITest, metaclass=Meta):
    """
    usage: define test cases
    """
    async def test_ping(self, endpoint) -> Response:
        response = await self.get(endpoint)
        return response

    async def test_ping2(self, endpoint) -> Response:
        response = await self.get(endpoint)
        return response


if __name__ == '__main__':
    host = r"http://localhost:8080"
    test_client = APITest(host, API_MAPPING)
    asyncio.run(test_client())
