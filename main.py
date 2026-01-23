from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        self.setup_menubar()

    def setup_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        new_vault_action = QAction(QIcon.fromTheme("document-new"), "&New Vault", self)
        new_vault_action.setShortcut(QKeySequence.New)
        new_vault_action.setStatusTip("Create a new vault")
        new_vault_action.triggered.connect(self.new_vault)

        file_menu.addAction(new_vault_action)
        exit_action=file_menu.addAction("Exit")
        exit_action.setIcon(QIcon.fromTheme("application-exit"))
        exit_action.triggered.connect(self.close)

    
    def new_vault(self):
        pass


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
