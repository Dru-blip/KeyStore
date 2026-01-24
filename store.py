from PySide6.QtCore import QObject, Signal

from models import Vault


class DataStore(QObject):
    vault_changed = Signal(name="vault_changed")

    def __init__(self):
        super().__init__()
        self.index = 0
        self.vault = Vault("dummy")

    def set_vault(self, vault):
        self.vault = vault
        self.vault_changed.emit()

    def get_vault(self):
        return self.vault

    def get_vault_name(self):
        return self.vault.name

    def get_records(self):
        return self.vault.records


Store = DataStore()
