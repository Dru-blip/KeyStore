import flet as ft
from fletx.core import FletXPage

from app.controllers import HomeController


class HomePage(FletXPage):
    ctrl = HomeController()

    def __init__(self):
        super().__init__()
        self.master_password = ft.TextField(
            label="Master Password",
            password=True,
            can_reveal_password=True,
            width=400,
        )

        self.vault_name = ft.TextField(
            label="Vault Name",
            width=400,
        )

        self.modal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Create Vault"),
            content=ft.Container(
                width=520, 
                height=200,    
                padding=24,
                content=ft.Column(
                    spacing=16,
                    controls=[
                        self.vault_name,
                        self.master_password,
                    ],
                ),
            ),
            actions=[
                ft.TextButton(
                    "Create",
                    on_click=self.create_vault,
                ),
                ft.TextButton(
                    "Close",
                    on_click=lambda e: e.page.close(self.modal_dialog),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )


    def create_vault(self, e):
        vault_name = self.vault_name.value
        master_password = self.master_password.value

        if not vault_name or not master_password:
            print("Missing fields")
            return

        print("Creating vault:", vault_name)
        e.page.close(self.modal_dialog)


    def build(self):
        vaults = self.ctrl.vaults
        
    
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Button(
                        content=ft.Text("Create New Vault"),
                        on_click=lambda e:e.page.open(self.modal_dialog),
                    ),
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Card(
                                width=400,
                                content=ft.Container(
                                    padding=10,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(vault.name),
                                            ft.Button(
                                                content=ft.Text("Open Vault"),
                                            ),
                                        ],
                                    ),
                                ),
                            )
                            for vault in vaults
                        ],
                    ),
                ]
            )
        )
