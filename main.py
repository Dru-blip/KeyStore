from nicegui import app, ui

from utils import create_vault

vault_created = app.storage.general.get("vault_created", False)


vault_password = ""


def set_master_password(event):
    global vault_password
    vault_password = event.value


def handle_create_vault():
    global vault_created
    vault_created = True
    app.storage.general["vault_created"] = True
    vault = create_vault(vault_password.encode())


@ui.page("/", dark=True)
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
        ui.button("open vault", on_click=lambda: ui.notify("opening vault"))


ui.run(native=True, storage_secret="secret")
