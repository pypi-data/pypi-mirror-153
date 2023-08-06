import base58
from os import urandom


def new_nonce():
    return base58.b58encode(urandom(32)).decode("utf-8")


def job_id_from_nonce(nonce):
    # return hashlib.sha256(nonce.encode()).hexdigest()
    return nonce
