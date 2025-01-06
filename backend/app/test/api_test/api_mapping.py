"""
API_MAPPING dict key name: should be test-methods-name.lstrip("test_"). (e.g. test_ping -> ping)

verify_mode:
    - json: verify the fixed api response (e.g. ping response is always {"status": "OK"})
    - type: verify the data structure is valid or not
    - status_code: verify the status_code is equal or not

dependencies: put the list of key name which the test have to wait for. put empty list when no dependencies

expected: put the expected return value of the api
    - json: put the dict of the api response
    - type: put a pydantic BaseModel
    - status_code: put a status_code(int)
"""

API_MAPPING = {
    "ping": {"endpoint": "api/1/ping", "verify_mode": "json", "expected": {"status": "OK"}, "dependencies": [], "status": ""},
    "ping2": {"endpoint": "api/1/ping", "verify_mode": "json", "expected": {"status": "OK"}, "dependencies": ["ping"], "status": ""},
    "ping3": {"endpoint": "api/1/ping", "verify_mode": "status_code", "expected": 200, "dependencies": ["ping"], "status": ""},
}


from httpx import Response, AsyncClient
import asyncio
import json
from typing import Callable, NoReturn
from pydantic import BaseModel, ValidationError


class Meta(type):
    """
    usage:
        1. check method's name startswith "test_" or not
        2. decorate the methods
        3. gather the decorated methods for running the test
    """
    def __new__(cls, name, bases, attrs):
        test_methods = []
        known_dependencies = []

        assertion: Callable = bases[0].assertion
        depends: Callable = bases[0].depends

        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and attr_name.startswith('test_'):
                print(f"Found test method: {attr_name}")
                known_dependencies.append(attr_name.lstrip("test_"))
                decorated_func = assertion(attr_value)
                decorated_func = depends(decorated_func)
                test_methods.append(decorated_func)
            elif callable(attr_value) and not attr_name.startswith('test_'):
                raise TypeError(f"Method {attr_name} should start with 'test_'")

        attrs["_test_methods"] = test_methods
        attrs["_known_dependencies"] = known_dependencies
        return super(Meta, cls).__new__(cls, name, bases, attrs)


class BaseAPITest:
    """
    usage: define basic support functions
    """
    def __init__(self, base_url: str, mapping: dict) -> NoReturn:
        self.client = AsyncClient()
        self.base_url = base_url
        self.mapping = mapping
        self.events: dict[str, asyncio.Event] = {}
        self.setup()

    async def __call__(self, *args, **kwargs) -> NoReturn:
        task_list: list = []
        for m in self._test_methods:
            task_list.append(asyncio.create_task(m(self)))
        await asyncio.gather(*task_list)

        await self.client.aclose()
        print(self.mapping)

    def setup(self) -> NoReturn:
        for dep in self._known_dependencies:
            self.events[dep] = asyncio.Event()

    @staticmethod
    def assertion(func) -> Callable:
        async def myfunc(self, *args, **kwargs):
            __key = func.__name__.lstrip("test_")
            __endpoint = self.mapping[__key]["endpoint"]
            __expected = self.mapping[__key]["expected"]
            __mode = self.mapping[__key]["verify_mode"]
            result = await func(self, __endpoint, *args, **kwargs)
            try:
                if __mode == "json":
                    assert BaseAPITest.check_json_value(result, __expected)
                elif __mode == "type":
                    assert BaseAPITest.check_type_format(result, __expected)
                elif __mode == "status_code":
                    assert BaseAPITest.check_status_code(result, __expected)
                else:
                    pass

                self.mapping[__key]["status"] = "succeeded"
                print(f"test {func.__name__} succeeded. get response {result}, expected {__expected}")

            except AssertionError:
                self.mapping[__key]["status"] = "failed"
                print(f"test {func.__name__} failed. get response {result}, expected {__expected}")

        myfunc.__name__ = func.__name__
        return myfunc

    @staticmethod
    def check_json_value(actual: Response, expected: dict) -> bool:
        return json.dumps(actual.json()) == json.dumps(expected)

    @staticmethod
    def check_type_format(actual: Response, expected: BaseModel) -> bool:
        try:
            expected.model_validate(actual.json())
            return True
        except ValidationError:
            return False

    @staticmethod
    def check_status_code(actual: Response, expected: int) -> bool:
        return actual.status_code == expected

    @staticmethod
    def depends(func) -> Callable:
        async def myfunc(self, *args, **kwargs):
            __key = func.__name__.lstrip("test_")
            dependencies: list[str] = self.mapping[__key]["dependencies"]

            if dependencies:
                await asyncio.gather(*(self.events[dep].wait() for dep in dependencies))

            result = await func(self, *args, **kwargs)

            self.events[__key].set()

            return result

        myfunc.__name__ = func.__name__
        return myfunc

    async def get(self, endpoint: str, query_params: dict | None = None) -> Response:
        __url = self.get_url(endpoint)
        return await self.client.get(__url, params=query_params)

    async def post(self, endpoint: str, body_params: dict | None = None) -> Response:
        __url = self.get_url(endpoint)
        return await self.client.post(__url, params=body_params)

    def get_url(self, endpoint) -> str:
        if endpoint.startswith("/"):
            return self.base_url + endpoint
        else:
            return self.base_url + "/" + endpoint
