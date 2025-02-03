import dataclasses
from typing import TypedDict
from enum import Enum


class Gender(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class SystemUser(str, Enum):
    Satori = "Satori"
    PTO = "PTO"


class AWSCredentials(TypedDict, total=False):
    AccessKeyId: str
    SecretKey: str
    SessionToken: str


@dataclasses.dataclass
class UserWithToken:
    id_token: str


CurrentUser = UserWithToken
