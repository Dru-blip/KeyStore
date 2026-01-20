import flet as ft

from fletx.app import FletXApp
from fletx.core import (
    FletXPage, FletXController, RxInt, RxStr,RxList
)
from fletx.navigation import router_config
from fletx.decorators import (
    obx
)

class CounterController(FletXController):
    def __init__(self):
        self.count = RxInt(0)
        super().__init__()

class CounterPage(FletXPage):
    ctrl = CounterController()

    @obx
    def counter_text(self):
        return ft.Text(
            value=f'Count: {self.ctrl.count.value}',
            size=50,
            weight="bold",
            color='red' if not self.ctrl.count.value % 2 == 0 else 'white'
        )

    def build(self):
        return ft.Column(
            controls=[
                self.counter_text(),
                ft.ElevatedButton(
                    "Increment",
                    on_click=lambda e: self.ctrl.count.increment()
                )
            ]
        )

def main():
    router_config.add_route(path='/', component=CounterPage)
    app = FletXApp(
        title="My Counter",
        initial_route="/",
        debug=True
    ).with_window_size(400, 600).with_theme(
        ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    )

    app.run_async()


if __name__ == "__main__":
    main()