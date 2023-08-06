""" Load config. """

import appdirs
from .__version__ import __app_name__, __author_name__, __version__
import os
import yaml

def get_config_dir_name():
    config_dir = appdirs.user_config_dir(__app_name__, __author_name__)
    return config_dir


def get_config_file_name(name="config.yaml"):
    config_dir = get_config_dir_name()
    config_file = os.path.join(config_dir, name)
    return config_file


def get_config(name="config.yaml"):
    config_file = get_config_file_name(name=name)
    try:
        with open(config_file) as f:
            yaml_config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"can't open config file: {config_file}")
        exit(-1)
    return yaml_config


def get_data_dir_name():
        data_dir = appdirs.user_data_dir(__app_name__, __author_name__)
        return data_dir


def get_data_file_name(name="data.yaml"):
        data_dir = get_data_dir_name()
        data_file = os.path.join(data_dir, name)
        return data_file

