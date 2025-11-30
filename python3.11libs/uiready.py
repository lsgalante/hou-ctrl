import hou
from hclib import HCGlobal
from PySide6.QtCore import Qt

hcglobal = HCGlobal()

hcglobal.reloadHotkeys()
hcglobal.toggleStowbars()

## Set network grid points to on
# networkeditors = desktop.getNetworkEditors()
# for networkeditor in networkeditors:
    # networkeditor.setPref("gridmode", "1")


## Qt
# if qt_commands:
#     window = hou.qt.mainWindow()
#     window.setWindowFlags(Qt.FramelessWindowHint)
#     window.setFixedWidth(1710)
#     window.setFixedHeight(1100)
