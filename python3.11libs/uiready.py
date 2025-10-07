import hou
from hctl.core.hcsession import HCSession
from hctl.utils.hclistener import HCListener
from PySide6.QtCore import Qt

hou.session.hCSession = HCSession()

# Settings
hotkeys = 1
qt_commands = 0
layout = 0
listener = 0


# Hotkeys
if hotkeys:
    session = hou.session.hCSession.reloadHotkeys()


# Layout
if layout:
    hou.session.hCSession.toggleMenus()
    hou.session.hCSession.toggleMainMenuBar()
    hou.session.hCSession.togglePaneTabs()

    # Set network grid points to on
    # networkEditors = desktop.getNetworkEditors()
    # for networkEditor in networkEditors:
        # networkEditor.setPref("gridmode", "1")


# Listener
if listener:
    hou.ui.addEventLoopCallback(HCListener().listener)


# Qt
if qt_commands:
    window = hou.qt.mainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setFixedWidth(1710)
    window.setFixedHeight(1100)
