import click, requests, json, os, shutil, glob, base64, urllib


# pylint: disable=import-error
from telemetry.basic import incrementMetric
from utils.config_utils import add_to_config
from utils.config_utils import read_from_cfg
from utils.cryptography import rsa_crypto
from utils import prepare_headers


API_URL = os.getenv("API_URL")
CGC_SECRET = os.getenv("CGC_SECRET")
TMP_DIR = os.getenv("TMP_DIR")


def get_jwt() -> str:
    """Command to get JWT token and api key for user

    :param username: _description_
    :type username: str
    :param password: _description_
    :type password: str
    """

    user_id = urllib.parse.quote(read_from_cfg("user_id"))
    passwd = urllib.parse.quote(read_from_cfg("passwd"))
    url = f"{API_URL}/v1/api/user/create/token"
    payload = f"grant_type=&username={user_id}&password={passwd}"

    jwt_headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        res = requests.post(
            url,
            payload,
            headers=jwt_headers,
            timeout=10,
        )

        if res.status_code != 200:
            click.echo(f"JWT error: {res.status_code}, error: {res.text}")
            incrementMetric("jwt.error")
            return None
        incrementMetric("jwt.ok")

        data = json.loads(res.text)
        jwt = data["access_token"]
        return jwt

    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


def auth_create_api_key():
    url = f"{API_URL}/v1/api/user/create/api-key"
    headers = prepare_headers.prepare_headers_api_key()
    try:
        res = requests.post(
            url,
            headers=headers,
            timeout=10,
        )

        if res.status_code != 200:
            click.echo(f"error: {res.status_code}, error: {res.text}")
            incrementMetric("api-key.error")
            return None
        incrementMetric("api-key.ok")

        data = json.loads(res.text)

        api_key = data["details"].get("_id")
        secret = data["details"].get("secret")

        add_to_config(api_key=api_key, api_secret=secret)

    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


def auth_list_api_key():
    url = f"{API_URL}/v1/api/user/list/api-key"
    headers = prepare_headers.prepare_headers_api_key()
    try:
        res = requests.post(
            url,
            headers=headers,
            timeout=10,
        )
        if res.status_code != 200:
            click.echo(f"error: {res.status_code}, error: {res.text}")
            return

        print_list = []
        data = json.loads(res.text)
        api_keys = data["details"].get("api_keys")

        if api_keys:
            for key in api_keys:
                _id = key.get("_id")
                secret = key.get("secret")
                print_list.append({_id: secret})

        click.echo(f"{print_list}")

    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


def get_unzip_dir(res: requests.Response) -> str:
    zip_file = res.headers.get("content-disposition").split('"')[1]

    if not os.path.isdir(TMP_DIR):
        os.mkdir(TMP_DIR)
    zip_file_path = f"{TMP_DIR}/{zip_file}"
    with open(zip_file_path, "wb") as f:
        f.write(res.content)

    unzip_dir = zip_file_path[:-4]
    shutil.unpack_archive(zip_file_path, unzip_dir)

    return unzip_dir


def get_aes_key_and_passwd(unzip_dir: str, priv_key_bytes: bytes):
    encrypted_passwd_path = ""
    encrypted_aes_path = ""
    for file in glob.glob(
        f"{unzip_dir}/**/*encrypted*",
        recursive=True,
    ):
        if file.endswith("priv"):
            encrypted_aes_path = f"{file}"
        elif file.endswith("password"):
            encrypted_passwd_path = f"{file}"

    rsa_key = rsa_crypto.import_create_RSAKey(priv_key_bytes)

    with open(encrypted_aes_path, "rb") as aes, open(
        encrypted_passwd_path, "rb"
    ) as pwd:
        aes_key = rsa_crypto.decrypt_rsa(aes.read(), rsa_key).decode("ascii")
        passwd = base64.b64decode(rsa_crypto.decrypt_rsa(pwd.read(), rsa_key)).decode(
            "utf-8"
        )

    return aes_key, passwd
