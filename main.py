import pyperclip
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
    with ui.column().classes("w-full h-screen items-center justify-center"):
        with ui.card().classes("w-96 p-8"):
            if not vault_created:
                ui.label("Create Your Vault").classes(
                    "text-2xl font-bold mb-2 self-center"
                )
                ui.label("Set a master password to secure your credentials").classes(
                    "text-sm text-gray-500 mb-6 self-center text-center"
                )

                ui.input(
                    label="Master Password",
                    password=True,
                    password_toggle_button=True,
                    on_change=set_master_password,
                    validation={
                        "Master Password exceeds 16 characters": lambda value: len(
                            value
                        )
                        < 17
                    },
                ).classes("w-full").props("outlined")

                ui.button(
                    "Create Vault", on_click=handle_create_vault, icon="add_circle"
                ).classes("w-full mt-4").props("size=lg color=primary")
            else:
                ui.label("Enter your master password to unlock").classes(
                    "text-sm text-gray-500 mb-6 self-center text-center"
                )

                ui.input(
                    label="Master Password",
                    password=True,
                    password_toggle_button=True,
                    on_change=set_master_password,
                    validation={
                        "Master Password exceeds 16 characters": lambda value: len(
                            value
                        )
                        < 17
                    },
                ).classes("w-full").props("outlined")

                ui.button(
                    "Unlock Vault", on_click=handle_open_vault, icon="lock_open"
                ).classes("w-full mt-4").props("size=lg color=primary")


@ui.page("/vault")
def vault():
    @ui.refreshable
    def records_ui():
        if not store.vault.records:
            with ui.column().classes("w-full items-center justify-center mt-16"):
                ui.icon("folder_open", size="64px").classes("text-gray-500 mb-4")
                ui.label("No records yet").classes("text-xl text-gray-500")
                ui.label("Click 'Add Record' to create your first entry").classes(
                    "text-sm text-gray-400"
                )
        else:
            with ui.grid(columns=1).classes("gap-4 w-full"):
                for record in store.vault.records:
                    with ui.card().classes("p-4"):
                        with ui.row().classes("w-full items-start justify-between"):
                            with ui.column().classes("gap-2 flex-grow"):
                                with ui.row().classes("items-center gap-2"):
                                    ui.icon("language", size="sm").classes(
                                        "text-primary"
                                    )
                                    ui.label(f"{record.name}").classes(
                                        "text-lg font-semibold"
                                    )

                                with ui.row().classes("items-center gap-2"):
                                    ui.icon("person", size="sm").classes(
                                        "text-gray-500"
                                    )
                                    ui.label(f"{record.username}").classes("text-sm")

                                with ui.row().classes("items-center gap-2"):
                                    ui.icon("key", size="sm").classes("text-gray-500")
                                    ui.label(f"{'•' * len(record.password)}").classes(
                                        "text-sm font-mono"
                                    )

                            with ui.column().classes("gap-2"):
                                ui.button(
                                    icon="content_copy",
                                    on_click=lambda r=record: [
                                        pyperclip.copy(r.password),
                                        ui.notify("Password copied!", type="positive"),
                                    ],
                                ).props("flat round color=primary").tooltip(
                                    "Copy password"
                                )

                                ui.button(
                                    icon="delete",
                                    on_click=lambda e, record=record: delete_record(
                                        record
                                    ),
                                ).props("flat round color=negative").tooltip(
                                    "Delete record"
                                )

    def delete_record(record):
        store.vault.delete_record(record)
        encrypt_vault(store.vault)
        records_ui.refresh()
        ui.notify("Record deleted", type="info")

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
        ui.notify("Record added successfully", type="positive")
        records_ui.refresh()
        dialog.close()

    with ui.dialog() as dialog, ui.card().classes("p-6 w-96"):
        ui.label("Add New Record").classes("text-xl font-bold mb-4")

        ui.input(label="Site", on_change=set_site).classes("w-full").props(
            "outlined"
        ).props("prepend-icon=language")
        ui.input(label="Username", on_change=set_username).classes("w-full mt-2").props(
            "outlined"
        ).props("prepend-icon=person")
        ui.input(
            label="Password",
            password=True,
            password_toggle_button=True,
            on_change=set_password,
        ).classes("w-full mt-2").props("outlined").props("prepend-icon=key")

        with ui.row().classes("w-full justify-end gap-2 mt-6"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Save", on_click=lambda: save_record(dialog), icon="save").props(
                "color=primary"
            )

    with ui.header().classes("items-center justify-between px-6"):
        with ui.row().classes("items-center gap-2"):
            ui.icon("shield", size="md").classes("text-primary")
            ui.label("Password Vault").classes("text-xl font-bold")
        ui.button("Add Record", on_click=dialog.open, icon="add").props("color=primary")

    with ui.column().classes("w-full max-w-4xl mx-auto p-6"):
        records_ui()


ui.run(native=True, dark=True, storage_secret="secret")
