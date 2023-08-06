import json, os
from dotenv import load_dotenv

load_dotenv()
USER_CONFIG_FILE = os.getenv("USER_CONFIG_FILE")


def add_to_config(**kwargs):
    """Function allowing adding a variable number of key-value pairs to the config file.
    If config file does not exist, it is created, otherwise key-value pairs are appended to existing config.
    Values for existing keys are overwritten.

    :param kwargs: key-value pairs to be saved in the config file
    :type kwargs: dict
    """
    read_cfg = {}

    try:
        f = open(USER_CONFIG_FILE, "r+", encoding="UTF-8")
        read_cfg = json.load(f)
    except FileNotFoundError:
        pass

    with open(USER_CONFIG_FILE, "w", encoding="UTF-8") as f:
        final_cfg = read_cfg | kwargs
        json.dump(final_cfg, f)


def read_from_cfg(key: str):
    """Function to read a single value from config

    :param key: key name to read the value from config
    :type key: str
    :return: value for the provided key
    :rtype: _type_
    """
    try:
        f = open(USER_CONFIG_FILE, "r+", encoding="UTF-8")
        read_cfg = json.load(f)
        return read_cfg[key]
    except FileNotFoundError:
        print("No config file found. Please use cgc register first.")
        exit()
    except KeyError:
        print("Config file is corrupted. Please contact support at support@comtegra.pl")
        exit()
