import hou
from hctl import HCGlobal
from PySide6.QtCore import Qt

hcglobal = HCGlobal()

# Settings
hotkeys = 1
qt_commands = 0
layout = 0
listener = 0

# Hotkeys
if hotkeys:
    hcglobal.reloadHotkeys()

# Layout
if layout:
    hcglobal.toggleMenus()
    hcglobal.toggleMainMenuBar()
    hcglobal.togglePaneTabs()

    # Set network grid points to on
    # networkeditors = desktop.getNetworkEditors()
    # for networkeditor in networkeditors:
        # networkeditor.setPref("gridmode", "1")

# Listener
# if listener:
    # hou.ui.addEventLoopCallback(HCListener().listener)

# Qt
if qt_commands:
    window = hou.qt.mainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setFixedWidth(1710)
    window.setFixedHeight(1100)
