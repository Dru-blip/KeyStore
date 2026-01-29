import base64
import os

import jsonpickle
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from nicegui import app

from models import Vault, store

storage_path = app.storage.path


def _derive_key(password: bytes) -> bytes:
    salt = app.storage.general.get("salt")
    if salt is None:
        salt = os.urandom(32)
        app.storage.general["salt"] = base64.b64encode(salt).decode("ascii")
    elif isinstance(salt, str):
        salt = base64.b64decode(salt)

    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=20,
        lanes=2,
        memory_cost=64 * 1024,
    )

    return kdf.derive(password)


def create_vault(password: bytes):
    key = _derive_key(password)
    records = []
    vault = Vault(key, records)
    store.set_vault(vault)
    encrypt_vault(vault)


def encrypt_vault(vault: Vault):
    key = vault.key
    data = vault.toJson().encode()
    cipher = AESGCM(key)
    nonce = os.urandom(16)
    ciphertext = cipher.encrypt(nonce, data, None)
    vault_path = storage_path / "vault.enc"
    with open(vault_path, "wb") as f:
        f.write(nonce + b"ENC" + ciphertext)


def decrypt_vault(password: bytes):
    key = _derive_key(password)
    vault_path = storage_path / "vault.enc"
    with open(vault_path, "rb") as f:
        nonce = f.read(16)
        f.read(3)
        ciphertext = f.read()

    cipher = AESGCM(key)
    data = cipher.decrypt(nonce, ciphertext, None)
    vault = Vault(key, jsonpickle.decode(data))
    store.set_vault(vault)
