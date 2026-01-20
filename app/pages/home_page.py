import flet as ft
from fletx.core import FletXPage

from app.controllers import HomeController


class HomePage(FletXPage):
    ctrl = HomeController()

    def build(self):
        vaults = self.ctrl.vaults
        return ft.Container(
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.ListView(
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
                    )
                ],
            )
        )
