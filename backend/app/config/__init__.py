from pydantic_settings import BaseSettings
import os
import platform
import pytz
import pytz.tzinfo


current_file_path = os.path.abspath(__file__)
app_dir = os.path.dirname(os.path.dirname(current_file_path))
api_dir = os.path.dirname(app_dir)

# for local env
# fill the necessary env var to local/.env or local-docker/.env to overwrite
if platform.system() != "Linux":
    from environs import Env  # this won't overwrite the env var value if the env var already set in os.environ
    Env().read_env(f"{app_dir}/config/local/.env")
elif os.getenv("BUILD_ENV") == "local":
    from environs import Env
    Env().read_env(f"{app_dir}/config/local-docker/.env")


class Settings(BaseSettings):
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    ALLOWED_IPS: str = "*"
    DB_URL: str
    DB_POOL_SIZE: int = 10
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    API_KEY: str
    HTTP_DIGEST_AUTH_PASSWORD: str
    USER_DEFAULT_AUTHORITY_CODE: int = 4
    USER_INACTIVE_AUTHORITY_CODE: int = 99

    # INIT_SCHEDULE_TASK: bool = False
    # CRONTAB_INTERVAL: str = "0 * * * *"
    # AWS_ACCOUNT_ID: str = "739616288903"
    # S3_BUCKET: str = "7cloud-media"
    # S3_REGION: str = "ap-northeast-1"
    # USER_POOL_ID: str = ""
    # USER_POOL_REGION: str = ""
    # IDENTITY_POOL_REGION: str = ""
    # IDENTITY_POOL_ID: str = ""
    # CLIENT_ID: str = ""
    # CLIENT_SECRET: str = ""

    class CONST:
        APP_NAME: str = "climb-club"
        API_VER: str = "v1"
        TINEZONE_STR: str = 'Asia/Tokyo'
        TIMEZONE: pytz.tzinfo.DstTzInfo = pytz.timezone(TINEZONE_STR)

    class SETTING:
        APP_FOLDER: str = app_dir
        LOCAL_LOG_PATH: str = os.path.join(api_dir, "log/syslog.log")
        DOCKER_LOG_PATH: str = '/var/log/syslog.log'
        BUILD_ENV: str = os.getenv("BUILD_ENV", "local")

    def __init__(self):
        temp_env = {}
        for key in self.model_fields:
            param = os.getenv(key)
            if param is not None:
                temp_env[key] = param

        super().__init__(**temp_env)


# use this instance directly as singleton
settings = Settings()
