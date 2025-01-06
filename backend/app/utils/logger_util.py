import logging
from logging.handlers import RotatingFileHandler
import inspect
import platform

from config import settings


class Logger(logging.Logger):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance

        instance = super().__new__(cls)
        cls.instance = instance
        return instance

    def __init__(self):
        super().__init__("cc_data_api_log", level=logging.INFO)
        self.file_handler = None
        self.console_handler = None
        self._get_file_handler()
        self._set_format()

    def _get_file_handler(self):
        if platform.system() != "Linux":
            self.file_handler = RotatingFileHandler(settings.SETTING.LOCAL_LOG_PATH, maxBytes=100 * 1024, backupCount=3)
        else:
            self.file_handler = RotatingFileHandler('/var/log/syslog.log', maxBytes=100 * 1024, backupCount=3)

        self.file_handler.setLevel(logging.INFO)
        self.addHandler(self.file_handler)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        self.addHandler(self.console_handler)

    def _set_format(self):
        log_format = "%(asctime)s - %(levelname)s - [ stack: blm, app: cc_data_api, api_call: %(api_call)s ] - message: %(message)s"
        formatter = logging.Formatter(log_format)
        self.file_handler.setFormatter(formatter)
        self.console_handler.setFormatter(formatter)

    def info(self, msg, *args, **kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {"api_call": self.get_caller_info()}
        elif isinstance(kwargs["extra"], str):
            kwargs["extra"] = {"api_call": kwargs["extra"]}
        super().info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {"api_call": self.get_caller_info()}
        elif isinstance(kwargs["extra"], str):
            kwargs["extra"] = {"api_call": kwargs["extra"]}
        super().error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if "extra" not in kwargs:
            kwargs["extra"] = {"api_call": self.get_caller_info()}
        elif isinstance(kwargs["extra"], str):
            kwargs["extra"] = {"api_call": kwargs["extra"]}
        super().warning(msg, *args, **kwargs)

    @staticmethod
    def get_caller_info() -> str:
        return inspect.stack()[2].function


logger = Logger()
