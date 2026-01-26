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

    def get_record(self, id):
        for record in self.records:
            if record.id == id:
                return record
        return None

    def add_record(self, name: str, email_or_username: str, password: str, site: str):
        new_record = Record(
            id=len(self.records),
            name=name,
            email_or_username=email_or_username,
            password=password,
            site=site,
        )
        self.records.append(new_record)
        return new_record

    def delete_record(self, id: int):
        self.records = [record for record in self.records if record.id != id]

    def update_record(
        self, id: int, name: str, email_or_username: str, password: str, site: str
    ):
        record = self.get_record(id)
        if record:
            record.name = name
            record.email_or_username = email_or_username
            record.password = password
            record.site = site


class Store:
    def __init__(self):
        self.vaults: List[Vault] = []

    def add_vault(self, vault: Vault):
        self.vaults.append(vault)


store = Store()


class Page:
    def __init__(self, tag: str, app: App):
        self.tag = tag
        self.app = app

    def show(self) -> None:
        dpg.configure_item(self.tag, show=True)

    def hide(self) -> None:
        dpg.configure_item(self.tag, show=False)

    def build(self) -> None:
        raise NotImplementedError


class VaultDetailsPage(Page):
    def __init__(self, app: App):
        super().__init__("vault_details_page", app)
        self.current_vault: Vault = None
        self.revealed_passwords: set[int] = set()
        self.editing_record_id: int = None

    def set_vault(self, vault: Vault):
        self.current_vault = vault
        self.revealed_passwords = set()

    def toggle_password_reveal(self, record_id: int):
        if record_id in self.revealed_passwords:
            self.revealed_passwords.remove(record_id)
        else:
            self.revealed_passwords.add(record_id)
        self.refresh_records()

    def open_add_dialog(self):
        self.editing_record_id = None
        self.clear_form()
        dpg.configure_item("record_dialog", show=True, label="Add Record")

    def open_edit_dialog(self, record_id: int):
        self.editing_record_id = record_id
        record = self.current_vault.get_record(record_id)
        if record:
            dpg.set_value("record_name_input", record.name)
            dpg.set_value("record_email_input", record.email_or_username)
            dpg.set_value("record_password_input", record.password)
            dpg.set_value("record_site_input", record.site or "")
            dpg.configure_item("record_dialog", show=True, label="Edit Record")

    def clear_form(self):
        dpg.set_value("record_name_input", "")
        dpg.set_value("record_email_input", "")
        dpg.set_value("record_password_input", "")
        dpg.set_value("record_site_input", "")

    def save_record(self):
        name: str = dpg.get_value("record_name_input")
        email: str = dpg.get_value("record_email_input")
        password: str = dpg.get_value("record_password_input")
        site: str = dpg.get_value("record_site_input")

        if not name or not email or not password:
            return

        if self.editing_record_id is None:
            self.current_vault.add_record(name, email, password, site if site else None)
        else:
            self.current_vault.update_record(
                self.editing_record_id,
                name,
                email,
                password,
                site if site else None,
            )

        dpg.configure_item("record_dialog", show=False)
        self.refresh_records()

    def delete_record(self, record_id: int):
        self.current_vault.delete_record(record_id)
        if record_id in self.revealed_passwords:
            self.revealed_passwords.remove(record_id)
        self.refresh_records()

    def refresh_records(self):
        if not self.current_vault:
            return

        if dpg.does_item_exist("vault_title"):
            dpg.set_value("vault_title", f"Vault: {self.current_vault.name}")

        if dpg.does_item_exist("records_container"):
            dpg.delete_item("records_container", children_only=True)
            self._render_list_view()

    def build(self):
        with dpg.group(tag=self.tag, show=False):
            dpg.add_button(
                label="Back", callback=lambda: self.app.show_page("vault_list_page")
            )
            dpg.add_spacer(height=10)

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Add Record", callback=lambda: self.open_add_dialog()
                )

            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)

            dpg.add_child_window(tag="records_container", height=-1)

        with dpg.window(
            tag="record_dialog",
            modal=True,
            show=False,
            label="Record",
            width=400,
            height=300,
        ):
            dpg.add_input_text(label="Name", tag="record_name_input")
            dpg.add_input_text(label="Email/Username", tag="record_email_input")
            dpg.add_input_text(
                label="Password", tag="record_password_input", password=True
            )
            dpg.add_input_text(label="Site (optional)", tag="record_site_input")

            dpg.add_spacer(height=10)

            with dpg.group(horizontal=True):
                dpg.add_button(label="Save", callback=lambda: self.save_record())
                dpg.add_button(
                    label="Cancel",
                    callback=lambda: dpg.configure_item("record_dialog", show=False),
                )

    def _render_list_view(self):
        for record in self.current_vault.records:
            with dpg.group(parent="records_container"):
                with dpg.group(horizontal=True):
                    dpg.add_text(f"Name: {record.name}", color=(100, 200, 255))

                with dpg.group(horizontal=True):
                    dpg.add_text(f"Email/Username: {record.email_or_username}")

                with dpg.group(horizontal=True):
                    if record.id in self.revealed_passwords:
                        dpg.add_text(f"Password: {record.password}")
                    else:
                        dpg.add_text(f"Password: {'•' * len(record.password)}")
                    dpg.add_button(
                        label="show"
                        if record.id not in self.revealed_passwords
                        else "hide",
                        callback=lambda s, a, u: self.toggle_password_reveal(u),
                        user_data=record.id,
                        width=30,
                    )

                if record.site:
                    with dpg.group(horizontal=True):
                        dpg.add_text(f"Site: {record.site}")

                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Edit",
                        callback=lambda s, a, u: self.open_edit_dialog(u),
                        user_data=record.id,
                    )
                    dpg.add_button(
                        label="Delete",
                        callback=lambda s, a, u: self.delete_record(u),
                        user_data=record.id,
                    )

                dpg.add_separator()


class VaultListPage(Page):
    def __init__(self, app: App):
        super().__init__("vault_list_page", app)
        self.vault_name: str = ""

    def set_vault_name(self, app_data):
        self.vault_name = app_data

    def create_vault(self):
        vault = Vault(self.vault_name)
        store.add_vault(vault)
        dpg.configure_item("create_vault_dialog", show=False)
        self.refresh_vault_list()

    @staticmethod
    def open_vault(sender, app_data, user_data):
        page = user_data["app"].pages["vault_details_page"]
        page.set_vault(user_data["vault"])
        user_data["app"].show_page(page.tag)

    def refresh_vault_list(self):
        if dpg.does_item_exist("vault_list"):
            dpg.delete_item("vault_list", children_only=True)

            for vault in store.vaults:
                with dpg.group(horizontal=True, parent="vault_list"):
                    dpg.add_text(vault.name)
                    dpg.add_button(
                        label="Open",
                        callback=self.open_vault,
                        user_data={"app": self.app, "vault": vault},
                    )

    def build(self):
        with dpg.group(tag=self.tag):
            dpg.add_button(
                label="Create Vault",
                callback=lambda: dpg.configure_item("create_vault_dialog", show=True),
            )

            dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_spacer(height=10)
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
        self.current_page: str = ""
        self.pages: Dict[str, Page] = {"vault_list_page": VaultListPage(self)}
        self.pages["vault_details_page"] = VaultDetailsPage(self)

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

        self.show_page("vault_list_page")

    def show_page(self, page_name: str):
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].hide()

        if page_name in self.pages:
            self.pages[page_name].show()
            self.current_page = page_name

    def config(self):
        with dpg.font_registry():
            font = dpg.add_font("./Roboto-Regular.ttf", 24)
            dpg.bind_font(font)


app = App()
app.config()
app.run()
