import hou
from PySide2 import QtCore, QtGui, QtWidgets
from fuzzyfinder import fuzzyfinder
import hou_ctl_utils as hcu
from importlib import reload
#import os

class inputBox(QtWidgets.QLineEdit):
    onTab = QtCore.Signal()
    def event(self, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.onTab.emit()
            return True
        else:
            return QtWidgets.QLineEdit.event(self, event)


class finder(QtWidgets.QDialog):
    def __init__(self):
        super(finder, self).__init__(hou.qt.mainWindow())
        reload(hcu)

        # input box
        self.inputBox = inputBox() 
        self.inputBox.onTab.connect(self.nextItem)
        self.inputBox.textEdited.connect(self.filter)
        self.inputBox.returnPressed.connect(self.execAction)

        # context label
        self.contextLabel = QtWidgets.QLabel()
        self.contextLabel.setText("Context: " + str(hou.ui.paneTabUnderCursor().type()))

        # autosave item
        autosaveItem = QtWidgets.QListWidgetItem()
        autosaveItem.setText("Autosave")
        state = hcu.getAutosaveState()
        if state == "1":
            autosaveItem.setCheckState(QtCore.Qt.Checked)
        elif state == "0":
            autosaveItem.setCheckState(QtCore.Qt.Unchecked)

        # pin item
        pinItem = QtWidgets.QListWidgetItem()
        pinItem.setText("Pin")
        tab = hou.ui.paneTabUnderCursor()
        if tab.isPin():
            pinItem.setCheckState(QtCore.Qt.Checked)
        else:
            pinItem.setCheckState(QtCore.Qt.Unchecked)

        # item array
        self.items = []
        self.items.append((autosaveItem,                     hcu.toggleAutosave))
        self.items.append((pinItem,                          hcu.tabTogglePin))
        self.items.append(("Deselect All Nodes",             hcu.nodeDeselectAll))
        self.items.append(("Dim Unused Nodes",               hcu.toggleDimUnusedNodes))
        self.items.append(("Display Options Toolbar",        hcu.toggleDisplayOptionsToolbar))
        self.items.append(("Group List",                     hcu.toggleGroupList))
        self.items.append(("Hide Shelf",                     hcu.hideShelf))
        self.items.append(("Main Menubar",                   hcu.toggleMainMenubar))
        self.items.append(("Network Box",                    hcu.networkBox))
        self.items.append(("Network Controls",               hcu.toggleNetworkControls))
        self.items.append(("Network Grid - Points",          hcu.toggleNetworkGridPoints))
        self.items.append(("Network Grid - Lines",           hcu.toggleNetworkGridLines))
        self.items.append(("Network Menubar",                hcu.toggleNetworkMenubar))
        self.items.append(("New Tab",                        hcu.newTab))
        self.items.append(("Open Floating Parameter Editor", hcu.openFloatingParameterEditor))
        self.items.append(("Pane Contract",                  hcu.paneContract))
        self.items.append(("Pane Expand",                    hcu.paneExpand))
        self.items.append(("Pane Maximize",                  hcu.togglePaneMaximized))
        self.items.append(("Pane Ratio Half",                hcu.paneRatioHalf))
        self.items.append(("Pane Ratio Quarter",             hcu.paneRatioQuarter))
        self.items.append(("Pane Ratio Third",               hcu.paneRatioThird))
        self.items.append(("Pane Split Horizontal",          hcu.paneSplitHorizontal))
        self.items.append(("Pane Split Rotate",              hcu.paneSplitRotate))
        self.items.append(("Pane Split Swap",                hcu.paneSplitSwap))
        self.items.append(("Pane Split Vertical",            hcu.paneSplitVertical))
        self.items.append(("Panetabs",                       hcu.togglePanetabs))
        self.items.append(("Point Markers",                  hcu.togglePointMarkers))
        self.items.append(("Point Normals",                  hcu.togglePointNormals))
        self.items.append(("Point Numbers",                  hcu.togglePointNumbers))
        self.items.append(("Prim Numbers",                   hcu.togglePrimNumbers))
        self.items.append(("Print Layout",                   hcu.printLayout))
        self.items.append(("Reload Color Schemes",           hcu.reloadColorSchemes))
        self.items.append(("Rename Node",                    hcu.renameNode))
        self.items.append(("Scene A",                        hcu.sceneSetA))
        self.items.append(("Show Shelf",                     hcu.showShelf))
        self.items.append(("Sticky Note",                    hcu.addStickyNote))
        self.items.append(("Stowbars",                       hcu.toggleStowbars))
        self.items.append(("Tab Close",                      hcu.tabClose))
        self.items.append(("Tab Type Network",               hcu.setTabTypeNetwork))
        self.items.append(("Tab Type Parameters",            hcu.setTabTypeParameters))
        self.items.append(("Tab Type Python",                hcu.setTabTypePython))
        self.items.append(("Tab Type Scene Viewer",          hcu.setTabTypeSceneViewer))
        self.items.append(("Tab Type Spreadsheet",           hcu.setTabTypeSpreadsheet))
        self.items.append(("Toggle All Menus",               hcu.toggleAllMenus))
        self.items.append(("Toggle Backfaces",               hcu.toggleBackface))
        self.items.append(("Toggle Split Maximized",            hcu.toggleSplitMaximized))
        self.items.append(("Toggle Vectors",                 hcu.toggleVectors))
        self.items.append(("Trigger Update",                 hcu.triggerUpdate))
        self.items.append(("Update Mode Auto",               hcu.updateModeAuto))
        self.items.append(("Update Mode Manual",             hcu.updateModeManual))
        self.items.append(("Update Main Menubar",            hcu.updateMainMenubar))
        self.items.append(("Viewer Toolbars",                hcu.toggleViewerToolbars))
        self.items.append(("Open Hotkey Editor",             hcu.openHotkeyEditor))
        self.items.append(("Toggle Overlay",                 self.overlay))
        self.items.append(("Visualizer Menu",                hcu.openVisualizerMenu))
        
        # list widget
        self.listWidget = QtWidgets.QListWidget()
        for item in self.items:
            self.listWidget.addItem(item[0])
        self.listWidget.itemClicked.connect(self.execAction)

        # make layout
        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        self.layout.addWidget(self.inputBox)
        self.layout.addWidget(self.contextLabel)
        self.layout.addWidget(self.listWidget) 
        self.setLayout(self.layout)
        self.setIndex(0)

    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

    def execAction(self):
        current_item = self.listWidget.selectedItems()[0]
        items = self.getItems()
        index = items.index(current_item)
        self.items[index][1]()
        self.accept()

    def getItems(self):
        item_count = self.listWidget.count()
        items = [self.listWidget.item(i) for i in range(item_count)]
        return(items)

    def getVisibleItems(self):
        item_count = self.listWidget.count()
        items = []
        for i in range(item_count):
            item = self.listWidget.item(i)
            if not item.isHidden(): 
                items.append(item)
        return(items)

    def nextItem(self):
        items = self.getVisibleItems()
        selected_item = self.listWidget.selectedItems()[0]
        index = items.index(selected_item)
        index = (index + 1) % len(items)
        self.setIndex(index)

    def setIndex(self, idx):
        items = self.getItems()
        counter = 0
        for item in items:
            if not item.isHidden():
                if counter == idx:
                    self.listWidget.setItemSelected(item, 1)
                counter += 1

    def filter(self):
        text = self.inputBox.text()
        items = self.getItems()
        names = [item.text() for item in items]
        suggestions = fuzzyfinder(text, names)
        suggestions = list(suggestions)
        for item in items:
            if item.text() in suggestions:
                item.setHidden(0)    
            else:
                item.setHidden(1)
        self.setIndex(0)
                
    def overlay(self):
        print("overlay")
