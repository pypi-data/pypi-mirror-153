import click, requests, os, shutil
from dotenv import load_dotenv


# pylint: disable=import-error
from commands.auth import auth_utils
from utils.cryptography import rsa_crypto
from utils.config_utils import add_to_config
from utils.prepare_headers import get_api_url_and_prepare_headers_register
from telemetry.basic import incrementMetric


load_dotenv()

API_URL = os.getenv("API_URL")
CGC_SECRET = os.getenv("CGC_SECRET")
TMP_DIR = os.getenv("TMP_DIR")


@click.command("register")
@click.option("--user_id", "-u", "user_id", prompt=True)
@click.option("--access_key", "-k", "access_key", prompt=True)
def auth_register(user_id: str, access_key: str):
    """Command to obtain user password, aes key and API key pair and save it to config

    :param user_id: username received in invite
    :type user_id: str
    :param access_key: access key received in invite
    :type access_key: str
    """

    url, headers = get_api_url_and_prepare_headers_register(user_id, access_key)
    pub_key_bytes, priv_key_bytes = rsa_crypto.key_generate_pair()
    payload = pub_key_bytes

    try:
        res = requests.post(
            url,
            data=payload,
            headers=headers,
            allow_redirects=True,
            timeout=10,
        )

        if res.status_code != 200:
            click.echo(f"{res.status_code}, {res.text}")
            incrementMetric("register.error")
            return
        incrementMetric("register.ok")

        unzip_dir = auth_utils.get_unzip_dir(res)
        aes_key, passwd = auth_utils.get_aes_key_and_passwd(unzip_dir, priv_key_bytes)

        add_to_config(user_id=user_id, passwd=passwd, aes_key=aes_key)
        auth_utils.auth_create_api_key()

        click.echo("User_id, password, and API key pair saved")
        shutil.rmtree(TMP_DIR)
    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )
