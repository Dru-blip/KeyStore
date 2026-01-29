from cryptography.exceptions import InvalidTag
from nicegui import app, ui

from models import store
from utils import create_vault, decrypt_vault, encrypt_vault

vault_created = app.storage.general.get("vault_created", False)
vault_password = ""


new_site = ""
new_username = ""
new_password = ""


def set_master_password(event):
    global vault_password
    vault_password = event.value


def set_site(e):
    global new_site
    new_site = e.value


def set_username(e):
    global new_username
    new_username = e.value


def set_password(e):
    global new_password
    new_password = e.value


def handle_create_vault():
    global vault_created
    vault_created = True
    app.storage.general["vault_created"] = True
    create_vault(vault_password.encode())
    ui.navigate.to("/vault")


def handle_open_vault():
    try:
        decrypt_vault(vault_password.encode())
        ui.navigate.to("/vault")
    except InvalidTag:
        ui.notify("Incorrect master password")


@ui.page("/")
def main():
    if not vault_created:
        ui.input(
            label="Master Password",
            on_change=set_master_password,
            validation={
                "Master Password exceeds 16 characters": lambda value: len(value) < 17
            },
        )
        ui.button("create vault", on_click=handle_create_vault)
    else:
        ui.input(
            label="Master Password",
            on_change=set_master_password,
            validation={
                "Master Password exceeds 16 characters": lambda value: len(value) < 17
            },
        )
        ui.button("open vault", on_click=handle_open_vault)


@ui.page("/vault")
def vault():
    ui.button("Back", on_click=lambda: ui.navigate.to("/"))

    @ui.refreshable
    def records_ui():
        with ui.grid(columns=1):
            for record in store.vault.records:
                with ui.card().props("flat bordered"):
                    ui.label(record.name)
                    ui.button(
                        icon="delete",
                        on_click=lambda e, record=record: delete_record(record),
                    )

    def delete_record(record):
        store.vault.delete_record(record)
        encrypt_vault(store.vault)
        records_ui.refresh()

    def save_record(dialog):
        if not new_site or not new_username or not new_password:
            ui.notify("All fields are required", type="warning")
            return

        store.vault.add_record(
            name=new_site,
            username=new_username,
            password=new_password,
        )
        encrypt_vault(store.vault)
        ui.notify("Record added")
        records_ui.refresh()
        dialog.close()

    with ui.dialog() as dialog, ui.card():
        ui.input(label="Site", on_change=set_site)
        ui.input(label="Username", on_change=set_username)
        ui.input(label="Password", password=True, on_change=set_password)

        ui.button("Save", on_click=lambda: save_record(dialog))
        ui.button("Cancel", on_click=dialog.close)

    ui.button("Add Record", on_click=dialog.open)
    records_ui()


ui.run(native=True, dark=True, storage_secret="secret")
