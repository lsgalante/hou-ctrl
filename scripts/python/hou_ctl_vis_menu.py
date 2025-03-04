import hou
from fuzzyfinder import fuzzyfinder
from importlib import reload
import hou_ctl_utils as hcu
from PySide2 import QtCore, QtGui, QtWidgets

class inputBox(QtWidgets.QLineEdit):
    # setup key events
    onTab = QtCore.Signal()
    def event(self, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.onTab.emit()
            return True
        else:
            return QtWidgets.QLineEdit.event(self, event)


class visualizerMenu(QtWidgets.QDialog):
    def __init__(self):	
        super(visualizerMenu, self).__init__(hou.qt.mainWindow())
        reload(hcu)

        # input box
        self.inputBox = inputBox() 
        self.inputBox.onTab.connect(self.nextItem)
        self.inputBox.textEdited.connect(self.filter)
        self.inputBox.returnPressed.connect(self.execAction)

        # fetch list of visualizers
        category = hou.viewportVisualizerCategory.Scene
        self.vis_arr = hou.viewportVisualizers.visualizers(category)
        self.items = []
        for vis in self.vis_arr:
            name = vis.label()
            self.items.append(name)

        # add items to list widget
        self.listWidget = QtWidgets.QListWidget()
        for item in self.items:
            self.listWidget.addItem(item)
        self.listWidget.itemClicked.connect(self.execAction)

        # construct layout
        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        self.layout.addWidget(self.inputBox)
        self.layout.addWidget(self.listWidget) 
        self.setLayout(self.layout)
        self.setIndex(0)

    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

    def execAction(self):
        viewports = hcu.getViewports()
        for viewport in viewports:
            for vis in self.vis_arr:
                vis.setIsActive(False, viewport)

        vis_name = self.listWidget.selectedItems()[0].text()
        index = self.items.index(vis_name)
        vis = self.vis_arr[index]
        for viewport in viewports:
            vis.setIsActive(True, viewport)

        viewer = hcu.getSceneViewers()[0]
        viewer.openVisualizerEditor(vis)

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

