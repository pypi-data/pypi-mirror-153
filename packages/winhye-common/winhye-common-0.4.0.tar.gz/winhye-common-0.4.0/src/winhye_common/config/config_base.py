import os

from .config_json import config_json

__all__ = ["config"]


class Config:
    def __init__(self):
        idc = os.environ.get('IDC')
        if idc:
            self.config = config_json[idc]
        else:
            self.config = config_json["kaifa"]

    def get_log_level_config(self):
        return self.config["log_level"]

    def get_alarm_config(self):
        return self.config["alarm"]


config = Config()
