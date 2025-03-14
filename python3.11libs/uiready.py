import hou_ctl_utils as hcu
from PySide2.QtCore import Qt

print("--BEGIN uiready.py--")

# Disable titlebar
flags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
# hou.qt.mainWindow().setWindowFlags(flags)

# Houdini seems to start some menus and stowbars enabled by default,
# regardless of the previous ui state.
hcu.toggleAllMenus()

# Re-enable main menu bar and pane tabs# Re-enable main menu bar and pane tabs# Re-enable main menu bar and pane tabs
hcu.toggleMainMenubar()
hcu.togglePanetabs()

# Set network grid points to on
networks = hcu.getNetworks()
for network in networks:
    network.setPref("gridmode", "1")

print("--END uiready.py--")
