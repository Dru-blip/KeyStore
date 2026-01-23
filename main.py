from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("Welcome to KeyStore!")
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_vault)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.open_button)
        self.setLayout(self.vlayout)

    def open_vault(self):
        self.parent().setCurrentIndex(1)


class VaultWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("Welcome to Vault!")
        self.go_back_button = QPushButton("Go Back")
        self.go_back_button.clicked.connect(self.go_back)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.go_back_button)
        self.setLayout(self.vlayout)

    def go_back(self):
        self.parent().setCurrentIndex(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        self.setup_menubar()
        self.container = QStackedWidget()
        self.container.addWidget(HomeWidget())
        self.container.addWidget(VaultWidget())

        self.setCentralWidget(self.container)

    def setup_menubar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        new_vault_action = QAction(QIcon.fromTheme("document-new"), "&New Vault", self)
        new_vault_action.setShortcut(QKeySequence.New)
        new_vault_action.setStatusTip("Create a new vault")
        new_vault_action.triggered.connect(self.new_vault)

        file_menu.addAction(new_vault_action)
        exit_action = file_menu.addAction("Exit")
        exit_action.setIcon(QIcon.fromTheme("application-exit"))
        exit_action.triggered.connect(self.close)

    def new_vault(self):
        pass


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
