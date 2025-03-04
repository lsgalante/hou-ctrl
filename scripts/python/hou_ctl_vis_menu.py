import hou
from fuzzyfinder import fuzzyfinder
from importlib import reload
import hou_ctl_utils as hcu
from PySide2 import QtCore, QtGui, QtWidgets

class inputBox(QtWidgets.QLineEdit):
    onTab = QtCore.Signal()
    def event(self, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.onTab.emit()
            return True
        else:
            return QtWidgets.QLineEdit.event(self, event)

class visMenu(QtWidgets.QDialog):
    def __init__(self):	
        super(visMenu, self).__init__(hou.qt.mainWindow())
        reload(hcu)

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)

        # input box
        self.inputBox = inputBox() 
        self.inputBox.onTab.connect(self.nextItem)
        self.inputBox.textEdited.connect(self.filter)
        self.inputBox.returnPressed.connect(self.execAction)
        self.layout.addWidget(self.inputBox)
        self.itemArray = []

        # fetch list of visualizers
        category = hou.viewportVisualizerCategory.Scene
        self.vis_arr = hou.viewportVisualizers.visualizers(category)
        for vis in self.vis_arr:
            name = vis.label()
            self.itemArray.append(name)

        # add list widget to layout
        self.listWidget = QtWidgets.QListWidget()
        for item in self.itemArray:
            self.listWidget.addItem(item)
        self.listWidget.itemClicked.connect(self.execAction)
        self.layout.addWidget(self.listWidget) 

        self.setLayout(self.layout)
        self.setIndex(0)


    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

    def execAction(self):
        viewports = []
        viewers = hcu.getSceneViewers()
        for viewer in viewers:
            for viewport in viewer.viewports():
                viewports.append(viewport)

        for viewport in viewports:
            for vis in self.vis_arr:
                vis.setIsActive(False, viewport)


        current_vis_name = self.listWidget.selectedItems()[0].text()
        index = self.itemArray.index(current_vis_name)
        current_vis = self.vis_arr[index]
        for viewport in viewports:
            current_vis.setIsActive(True, viewport)
        
        self.accept()


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

