import hctl_utils as hcu
from PySide2.QtCore import Qt

print("--BEGIN uiready.py--")

qt_commands = 0
ui_setup = 0
hotkey_setup = 1

if qt_commands:
    window = hou.qt.mainWindow()
    flags = Qt.FramelessWindowHint
    window.setWindowFlags(flags)
    window.setFixedWidth(1710)
    window.setFixedHeight(1100)

# if ui_setup:
    # Houdini starts with some ui elements visible regardless of desktop file.
    # desktop = hcu.Desktopx("test")
    # desktop.toggleMenus()
    # desktop.toggleMainMenuBar()
    # hcu.desktopTogglePaneTabs()

    # Set network grid points to on
    # networkEditors = desktop.getNetworkEditors()
    # for networkEditor in networkEditors:
        # networkEditor.setPref("gridmode", "1")

if hotkey_setup:
    session = hcu.Session()
    session.reloadKeyBindings()

print("--END uiready.py--")
