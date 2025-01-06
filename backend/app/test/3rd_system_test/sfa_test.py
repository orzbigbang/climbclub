"""
HOW TO USE:
no need to get the access token in advance so
just call the function that you want to validate
"""
import asyncio

from utils import SFAClient

sfa_client = SFAClient()

# EMAIL_ADDRESS = "hiroko.kamide@mirai.nagoya-u.ac.jp"
EMAIL_ADDRESS = "grp-pepper-ux@g.softbank.co.jp"


def get_access_token():  # validated
    sfa_client.get_access_token()
    print(sfa_client.access_token)


async def get_company_info():  # validated
    res: dict = await sfa_client.get_user_company_info(EMAIL_ADDRESS)
    print(res)


async def get_user_robots():  # validated
    res: dict = await sfa_client.get_user_robots(EMAIL_ADDRESS)
    print(res)


async def get_all_robots():  # validated
    res = await sfa_client.get_robot_by_service_id("230906001")
    print(res)


async def get_one_robot():
    head_id = "AP991003171729702989085970"
    head_id = "hiroko.kamide@mirai.nagoya-u.ac.jp"
    res: dict = await sfa_client.get_one_robot(head_id)
    print(res)


def main():
    asyncio.run(get_all_robots())
    # get_all_robots()
    # get_user_robots()
    # get_one_robot()


if __name__ == '__main__':
    main()
