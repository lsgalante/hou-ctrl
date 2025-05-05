import hou
from fuzzyfinder import fuzzyfinder
from importlib import reload
import hctl_utils as hcu
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt, QEvent

class filterBox(QtWidgets.QLineEdit):
    # Key handler
    onTab = QtCore.Signal()
    
    def event(self, event):

        if event.type() == QEvent.Type.KeyPress:
            key = event.key()

            if key == Qt.Key_Tab:
                self.onTab.emit()
                return True

        return QtWidgets.QLineEdit.event(self, event)
        

class visualizerMenu(QtWidgets.QDialog):
    
    def __init__(self):	
        super(visualizerMenu, self).__init__(hou.qt.mainWindow())
        reload(hcu)

        # Resources
        self.viewport = hcu.paneTabGetCurViewport()

        # Filter box
        self.filterBox = filterBox()
        self.filterBox.onTab.connect(self.listNext)
        self.filterBox.returnPressed.connect(self.itemToggle)
        self.filterBox.textEdited.connect(self.listFilter)

        # Resources
        self.vis_arr = hcu.viewportGetVisualizers()
        self.curViewport = hcu.paneTabGetCurViewport()
        
        # List widget
        self.listWidget = QtWidgets.QListWidget()
        if self.vis_arr:
            for vis in self.vis_arr:
                listItem = QtWidgets.QListWidgetItem()
                itemLabel = vis.label()
                itemState = vis.isActive(self.curViewport)
            
                listItem.setText(itemLabel)

                if itemState:
                    listItem.setCheckState(Qt.Checked)
                else:
                    listItem.setCheckState(Qt.Unchecked)
                
                self.listWidget.addItem(listItem)
            
        self.listWidget.itemClicked.connect(self.itemToggle)

        # Layout
        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        self.layout.addWidget(self.filterBox)
        self.layout.addWidget(self.listWidget) 
        self.setLayout(self.layout)
        self.listSetIndex(0)
        
        
    def closeEvent(self, event):
        print("Closing")
        self.setParent(None)
        
        
    def itemToggle(self):
        curItem = self.listWidget.selectedItems()[0]
        item_name = curItem.text()
        items = self.listGetItems()
        item_names = [item.text() for item in items]
        index = item_names.index(item_name)

        vis = self.vis_arr[index]
        state = vis.isActive(self.viewport)

        vis.setIsActive(not state, self.viewport)

        if state:
            curItem.setCheckState(Qt.Unchecked)
        else:
            curItem.setCheckState(Qt.Checked)

        
    def listFilter(self):
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
        self.listSetIndex(0)

        
    def listGetItems(self):
        item_count = self.listWidget.count()
        items = [self.listWidget.item(i) for i in range(item_count)]
        return(items)

    
    def listGetVisibleItems(self):
        item_count = self.listWidget.count()
        items = []
        for i in range(item_count):
            item = self.listWidget.item(i)
            if not item.isHidden(): 
                items.append(item)
        return(items)

            
    def listNext(self):
        visibleItems = self.listGetVisibleItems()
        curItem = self.listWidget.selectedItems()[0]
        index = visibleItems.index(curItem)
        index = (index + 1) % len(visibleItems)
        self.listSetIndex(index)

        
    def listPrev(self):
        visibleItems = self.listGetVisibleItems()
        curItem = self.listWidget.selectedItems()[0]
        index = visibleItems.index(curItem)
        index = (index - 1) % len(visibleItems)
        self.listSetIndex(index)

        
    def listSetIndex(self, index):
        visibleItems = self.listGetVisibleItems()
        counter = 0
        for visibleItem in visibleItems:
            if counter == index:
                self.listWidget.setItemSelected(visibleItem, 1)
                return
            counter += 1

