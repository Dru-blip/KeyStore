import os
from typing import Union

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from nicegui import app

from models import Vault

storage_path = app.storage.path


def _derive_key(password: bytes) -> bytes:
    salt = app.storage.general.get("salt")

    if salt is None:
        salt = os.urandom(32)
        app.storage.general["salt"] = str(salt)
    elif isinstance(salt, str):
        salt = salt.encode()

    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=200,
        lanes=2,
        memory_cost=64 * 1024,
    )

    return kdf.derive(password)


def create_vault(password: bytes):
    key = _derive_key(password)
    records = []
    vault = Vault(key, records)
    print(vault)
    return vault
