import hou
from hctl.core.session import HctlSession
from hctl.utils.listener import HctlListener
from PySide6.QtCore import Qt

hou.session.hctlSession = HctlSession()

# Settings
hotkeys = 1
qt_commands = 0
layout = 0
listener = 0


# Hotkeys
if hotkeys:
    session = hou.session.hctlSession.reloadHotkeys()


# Layout
if layout:
    hou.session.hctlSession.toggleMenus()
    hou.session.hctlSession.toggleMainMenuBar()
    hou.session.hctlSession.togglePaneTabs()

    # Set network grid points to on
    # networkEditors = desktop.getNetworkEditors()
    # for networkEditor in networkEditors:
        # networkEditor.setPref("gridmode", "1")


# Listener
if listener:
    hou.ui.addEventLoopCallback(HctlListener().listener)


# Qt
if qt_commands:
    window = hou.qt.mainWindow()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setFixedWidth(1710)
    window.setFixedHeight(1100)
