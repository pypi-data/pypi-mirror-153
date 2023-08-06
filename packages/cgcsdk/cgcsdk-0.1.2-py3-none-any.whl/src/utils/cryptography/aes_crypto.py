from Cryptodome.Cipher import AES  # to encrypt and decrypt long messages

# from hashlib import sha256  # to work with aes, generates sha256 based on input v1.0
from Cryptodome.Protocol.KDF import (
    PBKDF2,
)  # to work with aes, generates key better than sha256 of password v2.0
from Cryptodome import Random  # to generate random numbers
import base64  # to work with bytes
import os  # to work with path on OS

aes_password = os.getenv("AES_PRIVATE_KEY_PASSWORD")
if aes_password is None:
    aes_password = "apd4XNPn5t6GDtzzJbfZLsHFEPUvFEfkxCng9wwJm5DD"

aes_salt = os.getenv("AES_PRIVATE_KEY_SALT")
if aes_salt is None:
    aes_salt = "SALTGDtzzJFORHFEPUvFEfAES9wwJisHEREm5DD"

key_path = "./keys/00001-key"


def __pbkdf2_for_aes(
    password: str, salt: str, iterations: int = 1000000, desired_size: int = 32
):
    """
    AES private key

    It must be 16, 24 or 32 bytes long (respectively for *AES-128*,
    *AES-192* or *AES-256*).
    For ``MODE_SIV`` only, it doubles to 32, 48, or 64 bytes.
    """
    salt = bytes(salt, "utf-8")
    kdf = PBKDF2(
        str(password), salt, desired_size, iterations
    )  # default 1000, recommended 1000000 iterations
    key = kdf[:desired_size]
    return key


def _find_key_path():
    path_finder = None
    increment = 1
    while path_finder == None:
        try:
            path_finder = "%s-key" % (str(increment).zfill(5))
            file = open(path_finder, "rb")  # exception or NOT
            file.close()  # finds first not set filename for .key
            #!!! IT WILL OVERWRITE .pub and .aes FILES !!!
        except FileNotFoundError:
            increment += 1
            continue
    return path_finder


def key_open_AESPriv_file():
    try:
        private_key_aes = None
        file = open(key_path + ".aes", "rb")
        private_key_aes = file.read()
        file.close()

    except FileNotFoundError:
        # generate AES private key based on high entrophy self generated password
        # private_key_aes = sha256(self.__aes_password.encode("utf-8")).digest() # this was v1.0
        private_key_aes = __pbkdf2_for_aes(aes_password, aes_salt)  # this is v2.0
        with open(key_path + ".aes", "wb") as fp:
            fp.write(
                private_key_aes
            )  # saves priv key to file @ self._key_path "ex.: ./key.key"
            fp.close()
        pass
    return private_key_aes


def generate_bytes(length: int):
    return __pbkdf2_for_aes(
        password=str(Random.new().read(64)),
        salt=str(Random.new().read(64)),
        desired_size=length,
    )


def encrypt_aes(message: str, private_key_aes: bytes) -> bytes:  # output = C1
    pad_function = lambda s, BLOCK_SIZE: bytes(
        s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE),
        "utf-8",
    )
    message = pad_function(message, AES.block_size)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key_aes, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(message))


def decrypt_aes(c1: bytes, private_key_aes: bytes) -> bytes:
    unpad_function = lambda s: s[: -ord(s[len(s) - 1 :])]
    c1 = base64.b64decode(c1)
    iv = c1[: AES.block_size]
    cipher = AES.new(private_key_aes, AES.MODE_CBC, iv)
    return unpad_function(cipher.decrypt(c1[AES.block_size :]))
