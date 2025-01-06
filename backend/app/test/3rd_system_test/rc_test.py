from utils import RCUtil, datetime_to_rc_string, to_datetime
from requests import Response
# from script.sso_make_token import token


token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IjEifQ.eyJzdWIiOiJkNTIwZDJkOC0zNWFkLTQ1ZDQtOTg4ZC03NzBiMGI5ZGU4MTAiLCJmaXJzdG5hbWUiOiJWYWxpZGF0aW9uMTExIiwidXNlckdVSUQiOiJkNTIwZDJkOC0zNWFkLTQ1ZDQtOTg4ZC03NzBiMGI5ZGU4MTAiLCJmdWxsaGVhZElEIjoibnVsbCIsImdyb3VwcyI6IkNOPUNvbW11bml0eSxPVT1Hcm91cHMsT1U9SWRzdG9yZSxEQz1pZHN0b3JlLERDPWxhbiIsInVzZXJUeXBlIjoic2JiMmIiLCJib2R5SUQiOiJudWxsIiwiZW52IjoicHBkLWV1IiwiZW1haWwiOiJzYnJqdmFsaWRhdGlvbjExMUBnbWFpbC5jb20iLCJzYnJfbWVtYmVyIjoiZiIsImxhc3RuYW1lIjoiU0JSSiIsImV4cCI6MTcwNjYwNTc1MCwic2NvcGUiOltdLCJjbGllbnRfaWQiOiJzYXRvcmlfZnJvbnRlbmRfdXNlciJ9.ozGWIvxM1J_icbhkxNqKiKAAwgic2ojwhYKMQRa6c8IMXVCEm79p0Ms7ObuBpy-q55MbyEXDRHen8cJWeOU3bGlPZURBduSqGWSz_C_2se7u0PjIlUUqezquv6OrKC31GclV4h56jz53zu9_CWpR0GZH68msd5ILro2ydD1EJ93U_zvXcGBbE2XZRCcfDhH8dPbSbq6KaBhSikrkDg1Rj6PozYCCOwM1RCrCAG3dCHGlCzzorQ6dLmpOhmC0g-Tm5KxrjvsQf5EIRR-jogiCV7JehsByZNjPhktmRtPnxCYpsLNdk80A9NVnVMhUnoRbxM6-fo4IJYq8pyuE2KgT6Q"


rc_client = RCUtil()
rc_client.headers.update({'Authorization': 'Bearer ' + token})


def get_command():  # return 503 - Service Unavailable: Back-end server is at capacity
    from_date = "2023-09-09-09-09-09"
    to_date = "2023-11-11-11-11-11"
    head_id ="AP990237I00Y61100707"
    from_date_str = datetime_to_rc_string(to_datetime(from_date))
    to_datestr = datetime_to_rc_string(to_datetime(to_date))

    filters = {
        'robot_head_id': head_id,
        'from_creation_date': from_date_str + "+0900",
        'to_creation_date': to_datestr + "+0900"
    }
    result_get: Response = rc_client.get_command_v2(params=filters)
    res = result_get
    print(res.__dict__)


def main():
    get_command()


if __name__ == '__main__':
    main()
