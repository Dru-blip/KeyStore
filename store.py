from models import Vault


class DataStore:
    def __init__(self):
        self.index = 0
        self.vault = Vault("dummy")

    def set_vault(self, vault):
        self.vault = vault
        print("setting vault", self.vault.name)

    def get_vault(self):
        return self.vault

    def get_vault_name(self):
        return self.vault.name


Store = DataStore()
