# pylint: disable=import-error
import rsa_crypto
import aes_crypto

# priv_key_AES -> 32 bytes
# pub_key_RSA -> bytes opened with Cryptodome.PublicKey.RSA.importKey()
# priv_key_RSA -> bytes opened with Cryptodome.PublicKey.RSA.importKey()


def encrypt_aes(message: str, priv_key_AES: bytes = None):
    if priv_key_AES is None:
        priv_key_AES = aes_crypto.key_open_AESPriv_file()
    c1 = aes_crypto.encrypt_aes(
        message, priv_key_AES
    )  # message AES encrypted and b64 encoded
    return c1


def encrypt_hybrid(message: str, pub_key_RSA: bytes = None, priv_key_AES: bytes = None):
    if pub_key_RSA is None:
        pub_key_RSA = rsa_crypto.key_open_RSAPub_file()
    if priv_key_AES is None:
        priv_key_AES = aes_crypto.key_open_AESPriv_file()
    c1: bytes = aes_crypto.encrypt_aes(
        message, priv_key_AES
    )  # message AES encrypted and b64 encoded
    c2: bytes = rsa_crypto.encrypt_rsa(
        priv_key_AES, pub_key_RSA
    )  # AES priv key b64 encoded and RSA encrypted
    return c1, c2


def decrypt_hybrid(
    c1_message: bytes, c2_aes_priv_key: bytes, priv_key_RSA: bytes = None
):
    """AES priv key is RSA encrypted"""
    if priv_key_RSA is None:
        priv_key_RSA = rsa_crypto.key_open_RSAPriv_file()
    # self._key_open_AESPriv()
    try:
        priv_key_AES = rsa_crypto.decrypt_rsa(
            c2_aes_priv_key, priv_key_RSA
        )  # aka. priv key AES
    except:
        encrypt_hybrid(message="message")
        priv_key_AES = rsa_crypto.decrypt_rsa(c2_aes_priv_key, priv_key_RSA)
    decoded = aes_crypto.decrypt_aes(c1_message, priv_key_AES)  # message
    return decoded.decode("utf-8")


def decrypt_aes(c1_message: bytes, priv_key_AES: bytes = None):
    """AES priv key already in position"""
    if priv_key_AES is None:
        priv_key_AES = aes_crypto.key_open_AESPriv_file()
    decoded = aes_crypto.decrypt_aes(c1_message, priv_key_AES)  # message
    return decoded.decode("utf-8")
