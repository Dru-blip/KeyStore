import json
from typing import List, Optional


class Record:
    def __init__(self, name: str, username: str, password: str):
        self.name = name
        self.username = username
        self.password = password


class Vault:
    def __init__(
        self,
        key: bytes,
        records: List[Record] = [],
    ):
        self.key = key
        self.records: List[Record] = records

    def __str__(self):
        return json.dumps(self.records)

    def __repr__(self) -> str:
        return f"Vault<{self.key}>"


class Store:
    def __init__(self, vault: Optional[Vault] = None):
        self.vault: Optional[Vault] = vault

    def set_vault(self, vault: Vault):
        self.vault = vault


store = Store()
