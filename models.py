from dataclasses import dataclass
from typing import List, Optional

import jsonpickle


@dataclass
class Record:
    name: str
    username: str
    password: str


class Vault:
    def __init__(
        self,
        key: bytes,
        records: List[Record] = [],
    ):
        self.key = key
        self.records: List[Record] = records

    def add_record(self, name: str, username: str, password: str):
        self.records.append(Record(name, username, password))

    def toJson(self):
        return jsonpickle.encode(self.records)

    def __repr__(self) -> str:
        return f"Vault<{self.key}>"


class Store:
    def __init__(self, vault: Optional[Vault] = None):
        self.vault: Optional[Vault] = vault

    def set_vault(self, vault: Vault):
        self.vault = vault


store = Store()
