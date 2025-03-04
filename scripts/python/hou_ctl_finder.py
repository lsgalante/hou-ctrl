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

        # layout0
        self.layout0 = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        
        # input box
        self.inputBox = inputBox() 
        self.inputBox.onTab.connect(self.nextItem)
        self.inputBox.textEdited.connect(self.filter)
        self.inputBox.returnPressed.connect(self.execAction)
        self.layout0.addWidget(self.inputBox)

        # context label
        self.contextLabel = QtWidgets.QLabel()
        self.contextLabel.setText("Context: " + str(hou.ui.paneTabUnderCursor().type()))
        self.layout0.addWidget(self.contextLabel)

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

        # list item array
        self.itemArray = []
        self.itemArray.append((autosaveItem,                     hcu.toggleAutosave))
        self.itemArray.append((pinItem,                          hcu.tabTogglePin))
        self.itemArray.append(("Deselect All Nodes",             hcu.nodeDeselectAll))
        self.itemArray.append(("Dim Unused Nodes",               hcu.toggleDimUnusedNodes))
        self.itemArray.append(("Group List",                     hcu.toggleGroupList))
        self.itemArray.append(("Hide Shelf",                     hcu.hideShelf))
        self.itemArray.append(("Main Menubar",                   hcu.toggleMainMenubar))
        self.itemArray.append(("Network Box",                    hcu.networkBox))
        self.itemArray.append(("Network Controls",               hcu.toggleNetworkControls))
        self.itemArray.append(("Network Grid - Points",          hcu.toggleNetworkGridPoints))
        self.itemArray.append(("Network Grid - Lines",           hcu.toggleNetworkGridLines))
        self.itemArray.append(("Network Menubar",                hcu.toggleNetworkMenubar))
        self.itemArray.append(("Open Floating Parameter Editor", hcu.openFloatingParameterEditor))
        self.itemArray.append(("Pane Contract",                  hcu.paneContract))
        self.itemArray.append(("Pane Expand",                    hcu.paneExpand))
        self.itemArray.append(("Pane Maximize",                  hcu.togglePaneMaximized))
        self.itemArray.append(("Pane Ratio Half",                hcu.paneRatioHalf))
        self.itemArray.append(("Pane Ratio Quarter",             hcu.paneRatioQuarter))
        self.itemArray.append(("Pane Ratio Third",               hcu.paneRatioThird))
        self.itemArray.append(("Pane Split Horizontal",          hcu.paneSplitHorizontal))
        self.itemArray.append(("Pane Split Rotate",              hcu.paneSplitRotate))
        self.itemArray.append(("Pane Split Swap",                hcu.paneSplitSwap))
        self.itemArray.append(("Pane Split Vertical",            hcu.paneSplitVertical))
        self.itemArray.append(("Panetabs",                       hcu.togglePanetabs))
        self.itemArray.append(("Point Markers",                  hcu.togglePointMarkers))
        self.itemArray.append(("Point Numbers",                  hcu.togglePointNumbers))
        self.itemArray.append(("Prim Numbers",                   hcu.togglePrimNumbers))
        self.itemArray.append(("Print Layout",                   hcu.printLayout))
        self.itemArray.append(("Reload Color Schemes",           hcu.reloadColorSchemes))
        self.itemArray.append(("Rename Node",                    hcu.renameNode))
        self.itemArray.append(("Scene A",                        hcu.sceneSetA))
        self.itemArray.append(("Show Shelf",                     hcu.showShelf))
        self.itemArray.append(("Sticky Note",                    hcu.addStickyNote))
        self.itemArray.append(("Stowbars",                       hcu.toggleStowbars))
        self.itemArray.append(("Tab Close",                      hcu.tabClose))
        self.itemArray.append(("Tab Type Network",               hcu.setTabTypeNetwork))
        self.itemArray.append(("Tab Type Parameters",            hcu.setTabTypeParameters))
        self.itemArray.append(("Tab Type Python",                hcu.setTabTypePython))
        self.itemArray.append(("Tab Type Scene Viewer",          hcu.setTabTypeSceneViewer))
        self.itemArray.append(("Tab Type Spreadsheet",           hcu.setTabTypeSpreadsheet))
        self.itemArray.append(("Toggle All Menus",               hcu.toggleAllMenus))
        self.itemArray.append(("Toggle Vectors",                 hcu.toggleVectors))
        self.itemArray.append(("Trigger Update",                 hcu.triggerUpdate))
        self.itemArray.append(("Update Mode Auto",               hcu.updateModeAuto))
        self.itemArray.append(("Update Mode Manual",             hcu.updateModeManual))
        self.itemArray.append(("Update Main Menubar",            hcu.updateMainMenubar))
        self.itemArray.append(("Viewer Toolbars",                hcu.toggleViewerToolbars))
        self.itemArray.append(("Open Hotkey Editor",             hcu.openHotkeyEditor))
        self.itemArray.append(("Toggle Overlay",                 self.overlay))
        self.itemArray.append(("Vis Menu",                       hcu.visMenu))
        
        self.listWidget = QtWidgets.QListWidget()
        for item in self.itemArray:
            self.listWidget.addItem(item[0])

        self.listWidget.itemClicked.connect(self.execAction)
        self.layout0.addWidget(self.listWidget) 

        self.setLayout(self.layout0)
        self.setIndex(0)

    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

    def execAction(self):
        items = self.getItems()
        currentItem = self.listWidget.selectedItems()[0]
        index = items.index(currentItem)
        self.itemArray[index][1]()
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
