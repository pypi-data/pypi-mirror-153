import configparser
from os.path import expanduser
import os


class QuantplayConfig:
    """Commands for easy backtesting strategy"""

    config_path = "{}/.quantplay".format(expanduser("~"))

    def __init__(self):
        pass

    @staticmethod
    def get_credentials():
        isExist = os.path.exists(QuantplayConfig.config_path)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(QuantplayConfig.config_path)

        credentials = configparser.ConfigParser()
        credentials.read("{}/config".format(QuantplayConfig.config_path))

        return credentials

    @staticmethod
    def get_config():
        return QuantplayConfig.get_credentials()
