import flet as ft

from fletx.app import FletXApp
from app.pages import HomePage
from fletx.navigation import router_config

def main():
    router_config.add_route(path='/', component=HomePage)
    app = FletXApp(
        title="KeyStore",
        initial_route="/",
        debug=True
    ).with_window_size(600, 600)
    app.run_async()


if __name__ == "__main__":
    main()
