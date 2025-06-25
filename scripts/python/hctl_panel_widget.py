import hou, inspect, platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFrame, QLineEdit, QGridLayout, QLabel, QVBoxLayout, QListWidgetItem, QBoxLayout, QDialog, QListWidget
from PySide2.QtCore import Qt
from fuzzyfinder import fuzzyfinder
import hctl_utils as hcu
from importlib import reload


class filterLine(QLineEdit):
    key_ctl_n = QtCore.Signal()
    key_ctl_p = QtCore.Signal()
    key_arrow_down = QtCore.Signal()
    key_arrow_up = QtCore.Signal()

    # Input Event
    def event(self, event):
        # Keypress
        if event.type() == QtCore.QEvent.Type.KeyPress:
            key = event.key()
            mods = event.modifiers()
            # Single Keys
            if key == Qt.Key_Up:
                self.index_down.emit()
                return True
            elif key == Qt.Key_Down:
                self.index_up.emit()
            # Modified Keys
            else:
                # macos
                if platform.system() == "Darwin":
                    if key == Qt.Key_N and mods == Qt.MetaModifier:
                        self.index_up.emit()
                        return True
                    elif key == Qt.Key_P and mods == Qt.MetaModifier:
                        self.index_down.emit()
                        return True
                    else:
                        return QLineEdit.event(self, event)
                # Linux
                else:
                    if key ==Qt.Key_N and mods == Qt.ControlModifier:
                        self.index_up.emit()
                        return True
                    elif key == Qt.Key_P and mods == Qt.ControlModifier:
                        self.index_down.emit()
                        return True
                    else:
                        return QLineEdit.event(self, event)
        else:
            return QLineEdit.event(self, event)

class dialog(QDialog):
    def __init__(self):
        super(dialog, self).__init__(hou.qt.mainWindow())
        reload(hcu)
                
                                        
