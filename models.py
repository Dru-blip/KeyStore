from typing import List


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

    def __repr__(self) -> str:
        return f"Vault<{self.key}>"
