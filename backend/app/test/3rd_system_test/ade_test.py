"""
HOW TO USE

"""


from utils import ADEUtil
from requests import Response
# from script.sso_make_token import token


token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IjEifQ.eyJzdWIiOiJkNTIwZDJkOC0zNWFkLTQ1ZDQtOTg4ZC03NzBiMGI5ZGU4MTAiLCJmaXJzdG5hbWUiOiJWYWxpZGF0aW9uMTExIiwidXNlckdVSUQiOiJkNTIwZDJkOC0zNWFkLTQ1ZDQtOTg4ZC03NzBiMGI5ZGU4MTAiLCJmdWxsaGVhZElEIjoibnVsbCIsImdyb3VwcyI6IkNOPUNvbW11bml0eSxPVT1Hcm91cHMsT1U9SWRzdG9yZSxEQz1pZHN0b3JlLERDPWxhbiIsInVzZXJUeXBlIjoic2JiMmIiLCJib2R5SUQiOiJudWxsIiwiZW52IjoicHBkLWV1IiwiZW1haWwiOiJzYnJqdmFsaWRhdGlvbjExMUBnbWFpbC5jb20iLCJzYnJfbWVtYmVyIjoiZiIsImxhc3RuYW1lIjoiU0JSSiIsImV4cCI6MTcwNjYwNTc1MCwic2NvcGUiOltdLCJjbGllbnRfaWQiOiJzYXRvcmlfZnJvbnRlbmRfdXNlciJ9.ozGWIvxM1J_icbhkxNqKiKAAwgic2ojwhYKMQRa6c8IMXVCEm79p0Ms7ObuBpy-q55MbyEXDRHen8cJWeOU3bGlPZURBduSqGWSz_C_2se7u0PjIlUUqezquv6OrKC31GclV4h56jz53zu9_CWpR0GZH68msd5ILro2ydD1EJ93U_zvXcGBbE2XZRCcfDhH8dPbSbq6KaBhSikrkDg1Rj6PozYCCOwM1RCrCAG3dCHGlCzzorQ6dLmpOhmC0g-Tm5KxrjvsQf5EIRR-jogiCV7JehsByZNjPhktmRtPnxCYpsLNdk80A9NVnVMhUnoRbxM6-fo4IJYq8pyuE2KgT6Q"
ade_client = ADEUtil(token)


def get_user_type():
    res: Response = ade_client.get_user_types()
    res: dict = res.json()
    print(res)


def get_all_user_robots():
    ade_client.get_robots_from_ade()
    print(ade_client.result.text)
    # res = ade_client.result.json()
    # print(res)


def main():
    get_all_user_robots()


if __name__ == '__main__':
    main()
