import hou
from fuzzyfinder import fuzzyfinder
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QLineEdit, QDialog
from .core.hcglobal import HCGlobal


class inputBox(QLineEdit):
    onTab = QtCore.Signal()
    def event(self, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.onTab.emit()
            return True
        else:
            return QLineEdit.event(self, event)


class newTabPanel(QDialog):
    def __init__(self):
        super(newTabPanel, self).__init__(hou.qt.mainWindow())

        self.hc_global = HCGlobal()

        # Input box
        self.input_box = inputBox()
        self.input_box.onTab.connect(self.nextItem)
        self.input_box.textEdited.connect(self.filter)
        self.input_box.returnPressed.connect(self.execAction)

        # Item array
        self.items = []
        self.items.append(("Geometry Spreadsheet", hou.paneTabType.DetailsView))
        self.items.append(("Network Editor", hou.paneTabType.NetworkEditor))
        self.items.append(("Parameters", hou.paneTabType.Parm))
        self.items.append(("Python Shell", hou.paneTabType.PythonShell))
        self.items.append(("Scene Viewer", hou.paneTabType.SceneViewer))

        # List widget
        self.list_widget = QtWidgets.QListWidget()
        for item in self.items:
            self.list_widget.addItem(item[0])
        self.list_widget.itemClicked.connect(self.execAction)

        # Make layout
        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)
        self.setIndex(0)

    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

    def execAction(self):
        current_item = self.list_widget.selectedItems()[0]
        items = self.getItems()
        index = items.index(current_item)
        tab = self.hc_global.tab()
        tab.createTab(self.items[index][1])
        self.accept()

    def filter(self):
        text = self.input_box.text()
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
        item_count = self.list_widget.count()
        items = [self.list_widget.item(i) for i in range(item_count)]
        return(items)

    def getVisibleItems(self):
        item_count = self.list_widget.count()
        items = []
        for i in range(item_count):
            item = self.list_widget.item(i)
            if not item.isHidden():
                items.append(item)
        return(items)

    def nextItem(self):
        items = self.getVisibleItems()
        selected_item = self.list_widget.selectedItems()[0]
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
