from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from importlib import reload


class HCButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("text-align: left; padding: 0 0 0 0")
        self.setFlat(1)


class HCMenu(QtWidgets.QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.setStyleSheet("text-align: left; padding: 0 0 0 0")
        self.setFlat(1)
