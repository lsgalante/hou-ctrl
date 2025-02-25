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
        self.inputBox.onTab.connect(self.changeIndex)
        self.inputBox.textEdited.connect(self.filter)
        self.inputBox.returnPressed.connect(self.execAction)
        self.layout0.addWidget(self.inputBox)

        # context label
        self.contextLabel = QtWidgets.QLabel()
        self.contextLabel.setText("Context: " + str(hou.ui.paneTabUnderCursor().type()))
        self.layout0.addWidget(self.contextLabel)

        # list widget
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.itemClicked.connect(self.execAction)
        self.listWidget.addItem("Toggle All Menus")
        self.listWidget.addItem("Toggle Panetabs")
        self.listWidget.addItem("Dim Unused Nodes")
        self.listWidget.addItem("Toggle Main Menubar")
        self.listWidget.addItem("Toggle Path")
        self.listWidget.addItem("Toggle Network Menubar")
        self.listWidget.addItem("Toggle Viewer Toolbars")
        self.listWidget.addItem("Toggle Point Markers")
        self.listWidget.addItem("Rename Node")
        self.listWidget.addItem("Hide Shelf")
        self.listWidget.addItem("Show Shelf")
        self.listWidget.addItem("Reload Color Schemes")
        self.listWidget.addItem("Trigger Update")
        self.listWidget.addItem("Update Mode Auto")
        self.listWidget.addItem("Update Mode Manual")
        self.listWidget.addItem("Update Main Menubar")
        self.listWidget.addItem("Toggle Vectors")
        self.listWidget.addItem("Pane Expand")
        self.listWidget.addItem("Pane Contract")
        #self.listWidget.addItem("Toggle Stowbars")
        #self.listWidget.addItem("Autosave")
        #self.listWidget.addItem("Toggle Overlay")
        #self.listWidget.addItem("Open Hotkey Editor")
        self.layout0.addWidget(self.listWidget) 

        # layout1

        #self.autosave_b = QtWidgets.QCheckBox("autosave")
        #self.autosave_b.setChecked(int(hcu.get_autosave_state()))
        #self.autosave_b.stateChanged.connect(hcu.toggle_autosave)
        #self.button_arr.append("autosave")
        #self.layout1.addWidget(self.autosave_b)

        ## apply final layout
        self.setLayout(self.layout0)
        self.setSelection(0)

    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

    def execAction(self):
        currentItem = self.listWidget.selectedItems()[0].text()
        if   currentItem == "Dim Unused Nodes":        hcu.toggleDimUnusedNodes()
        elif currentItem == "Hide Shelf":              hcu.hideShelf()
        elif currentItem == "Open Hotkey Editor":      hcu.openHotkeyEditor()
        elif currentItem == "Pane Expand":             hcu.paneExpand()
        elif currentItem == "Pane Contract":           hcu.paneContract()
        elif currentItem == "Reload Color Schemes":    hcu.reloadColorSchemes()
        elif currentItem == "Rename Node":             hcu.renameNode()
        elif currentItem == "Show Shelf":              hcu.showShelf()
        elif currentItem == "Toggle All Menus":        hcu.toggleAllMenus()
        elif currentItem == "Toggle Main Menubar":     hcu.toggleMainMenubar()
        elif currentItem == "Toggle Network Controls": hcu.toggleNetworkControls()
        elif currentItem == "Toggle Network Menubar":  hcu.toggleNetworkMenubar()
        elif currentItem == "Toggle Overlay":          self.overlay()
        elif currentItem == "Toggle Panetabs":         hcu.togglePanetabs()
        elif currentItem == "Toggle Point Markers":    hcu.togglePointMarkers()
        elif currentItem == "Toggle Stowbars":         hcu.toggleStowbars()
        elif currentItem == "Toggle Vectors":          hcu.toggleVectors()
        elif currentItem == "Toggle Viewer Toolbars":  hcu.toggleViewerToolbars()
        elif currentItem == "Trigger Update":          hcu.triggerUpdate()
        elif currentItem == "Update Main Menubar":     hcu.updateMainMenubar()
        elif currentItem == "Update Mode Auto":        hcu.updateModeAuto()
        elif currentItem == "Update Mode Manual":      hcu.updateModeManual()
        self.accept()

    def changeIndex(self):
        item = self.listWidget.selectedItems()[0]
        idx = self.listWidget.indexFromItem(item).row()
        self.setSelection(idx + 1)

    def setSelection(self, idx):
        item_ct = self.listWidget.count()
        items = [self.listWidget.item(i) for i in range(item_ct)]
        counter = 0
        for item in items:
            if not item.isHidden():
                if counter == idx:
                    self.listWidget.setItemSelected(item, 1)
                counter += 1

    def filter(self):
        text = self.inputBox.text()
        ct = self.listWidget.count()
        items = [self.listWidget.item(i) for i in range(ct)]
        names = [item.text() for item in items]
        suggestions = fuzzyfinder(text, names)
        suggestions = list(suggestions)
        for item in items:
            if item.text() in suggestions:
                item.setHidden(0)    
                ct += 1
            else:
                item.setHidden(1)
        self.setSelection(0)
                
    def overlay(self):
        print("overlay")
