from utils import RHMUtil
from requests import Response
# from script.sso_make_token import token

token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IjEifQ.eyJzdWIiOiJhNmE4Y2U1My03ZjUwLTRlOWEtYTEyYS00NjVkYWMzNjAwMmYiLCJmaXJzdG5hbWUiOiJPcmFuZ2V0dGUiLCJ1c2VyR1VJRCI6ImE2YThjZTUzLTdmNTAtNGU5YS1hMTJhLTQ2NWRhYzM2MDAyZiIsImZ1bGxoZWFkSUQiOiJudWxsIiwiZ3JvdXBzIjoiQ049Q29tbXVuaXR5LE9VPUdyb3VwcyxPVT1JZHN0b3JlLERDPWlkc3RvcmUsREM9bGFuIiwidXNlclR5cGUiOiJhY2FkZW1pYyIsImJvZHlJRCI6Im51bGwiLCJlbnYiOiJwcGQtZXUiLCJlbWFpbCI6ImVudXNvcHktOTIxM0B5b3BtYWlsLmNvbSIsInNicl9tZW1iZXIiOiJmIiwibGFzdG5hbWUiOiJDaG9jb2xhdCIsImV4cCI6MTcxOTgwOTcwMywic2NvcGUiOltdLCJjbGllbnRfaWQiOiJzYXRvcmlfZnJvbnRlbmRfdXNlciJ9.RcEJAbtCj3seBMdxs0eYQBZGg4WdS8tsOglMdPA8vkWI_6fm8O1RtgJVXk5INGTTm2aWrbdo8jIThhj5SkO7tZawWrfliRS3zapAfS7cquaI2N_FqQmAbwvdDvJv9N4wdaWq_B9Jk8hKOCmSodoi8AVQOLG17mvcAN7MsjYDK2imj_5R-BEwGkkI2Z9Ak4VjBkA8Gmoau5ej2bag7MhCP5Quo5AH0eBAjXSLOtsUwiEbOfx9jwEzVfD873It0lvf8H3KXq8UbnxW6-kb8C2SvnPOBSsmR1xi1FcjWI46AWKt--Qr_Hr-TH5DxlBftYELw7A5uVBwDW5z0J5vmSMNZg"

rhm_client = RHMUtil()
rhm_client.headers.update({'Authorization': 'Bearer ' + token})
robot_head_id = "AP990237I00Y63100316"
robot_body_id = "AP990438B01Y64100033"


def get_robot():  # validated
    res: Response = rhm_client.get_robot(robot_head_id, robot_body_id, access_token=token)
    res: dict = res.json()
    print(res)


def get_robots():  # validated
    res = rhm_client.get_robots()
    print(res)
    return res


def main():
    robots = get_robots()
    import json
    with open("rhm_robots.json", "w", encoding="utf-8") as fp:
        json.dump(robots, fp)


if __name__ == '__main__':
    main()
