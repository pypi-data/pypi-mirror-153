import os
from dotenv import load_dotenv


# pylint: disable=import-error
from utils.config_utils import read_from_cfg
from commands.auth import auth_utils

load_dotenv()

API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")
API_URL = f"http://{API_HOST}:{API_PORT}"
CGC_SECRET = os.getenv("CGC_SECRET")
USER_CONFIG_FILE = os.getenv("USER_CONFIG_FILE")


def load_user_api_keys():
    """Based on configuration getter creates pair of API keys

    :return: api_key and api_secret
    :rtype: list of strings
    """
    return read_from_cfg("api_key"), read_from_cfg("api_secret")


def get_api_url_and_prepare_headers():
    """Loads API_URL and user api keys into single function. Ment to be used as single point of truth for all andpoints except register - due to different Content-Type header

    :return: API_URL and headers
    :rtype: string and dict
    """
    api_key, api_secret = load_user_api_keys()
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "api-key": api_key,
        "api-secret": api_secret,
        "comtegra-cgc": CGC_SECRET,
    }
    return API_URL, headers


def get_api_url_and_prepare_headers_register(user_id: str, access_key: str):
    """Creates and returns url and headers for register request.

    :return: url, headers
    :rtype: string and dict
    """
    url = f"{API_URL}/v1/api/user/register?user_id={user_id}&access_key={access_key}"
    headers = {
        "accept": "application/json",
        "comtegra-cgc": CGC_SECRET,
        "Content-Type": "octet-stream",
    }
    return url, headers


def prepare_headers_api_key():
    headers = {
        "accept": "application/json",
        "comtegra-cgc": CGC_SECRET,
        "Authorization": f"Bearer {auth_utils.get_jwt()}",
    }
    return headers
