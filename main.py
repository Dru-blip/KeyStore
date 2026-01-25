import ctypes
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import dearpygui.dearpygui as dpg

ctypes.windll.user32.SetProcessDPIAware()


@dataclass
class Record:
    id: int
    name: str
    email_or_username: str
    password: str
    site: Optional[str] = None


@dataclass
class Vault:
    name: str
    records: List[Record] = field(default_factory=list)


class Store:
    def __init__(self):
        self.vaults: List[Vault] = []

    def add_vault(self, vault: Vault):
        self.vaults.append(vault)


store = Store()


class Page:
    def __init__(self, tag: str):
        self.tag = tag

    def show(self):
        dpg.configure_item(self.tag, show=True)

    def hide(self):
        dpg.configure_item(self.tag, show=False)

    def build(self):
        raise NotImplementedError


class VaultListPage(Page):
    def __init__(self):
        super().__init__("vault_list_page")
        self.vault_name: str = ""

    def set_vault_name(self, app_data):
        self.vault_name = app_data

    def create_vault(self):
        vault = Vault(self.vault_name)
        store.add_vault(vault)
        dpg.configure_item("create_vault_dialog", show=False)
        self.refresh_vault_list()

    def refresh_vault_list(self):
        if dpg.does_item_exist("vault_list"):
            dpg.delete_item("vault_list", children_only=True)

            for vault in store.vaults:
                with dpg.group(horizontal=True, parent="vault_list"):
                    dpg.add_text(vault.name)
                    dpg.add_button(label="Open")

    def build(self):
        with dpg.group(tag=self.tag):
            dpg.add_button(
                label="Create Vault",
                callback=lambda: dpg.configure_item("create_vault_dialog", show=True),
            )

        dpg.add_group(tag="vault_list")
        self.refresh_vault_list()

        with dpg.window(
            tag="create_vault_dialog", modal=True, show=False, label="Create Vault"
        ):
            dpg.add_input_text(
                label="Vault Name",
                callback=lambda sender, app_data: self.set_vault_name(app_data),
            )
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Create",
                    callback=lambda: self.create_vault(),
                )
                dpg.add_button(
                    label="Cancel",
                    callback=lambda: dpg.configure_item(
                        "create_vault_dialog", show=False
                    ),
                )


class App:
    def __init__(self):
        self.current_view: str = ""
        self.pages: Dict[str, Page] = {"vault_list_page": VaultListPage()}

        dpg.create_context()
        dpg.create_viewport(title="Key Store", width=800, height=500)

    def run(self):
        self.setup_pages()
        dpg.setup_dearpygui()
        dpg.set_primary_window("main_window", True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def setup_pages(self):
        with dpg.window(tag="main_window", pos=(100, 100), width=600, height=400):
            for page in self.pages.values():
                page.build()

    def config(self):
        with dpg.font_registry():
            font = dpg.add_font("./Roboto-Regular.ttf", 24)
            dpg.bind_font(font)


app = App()
app.config()
app.run()
