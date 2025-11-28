import hou
from fuzzyfinder import fuzzyfinder
from PySide6 import QtCore
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QDialog, QLineEdit, QBoxLayout
from PySide6.QtCore import Qt, QEvent


class filterBox(QLineEdit):
    def __init__(self):
        # Key handler
        self.onTab = QtCore.Signal()

    def event(self, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key == Qt.Key_Tab:
                self.onTab.emit()
                return True
        return QLineEdit.event(self, event)


class VisualizerMenu(QDialog):
    def __init__(self):
        super(VisualizerMenu, self).__init__(hou.qt.mainWindow())

        # Resources
        self.viewport = hou.session.hctlSession.viewport()
        self.vis_arr = self.viewport.visualizers()

        # Filter box
        self.filter_box = filterBox()
        self.filter_box.onTab.connect(self.listNext)
        self.filter_box.returnPressed.connect(self.itemToggle)
        self.filter_box.textEdited.connect(self.listFilter)

        # List widget
        self.list_widget = QListWidget()
        if self.vis_arr:
            for vis in self.vis_arr:
                list_item = QListWidgetItem()
                item_label = vis.label()
                item_state = vis.isActive(self.curViewport)

                list_item.setText(item_label)

                if item_state:
                    list_item.setCheckState(Qt.Checked)
                else:
                    list_item.setCheckState(Qt.Unchecked)

                self.list_widget.addItem(list_item)

        self.list_widget.itemClicked.connect(self.item_toggle)

        # Layout
        self.layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout.addWidget(self.filter_box)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)
        self.listSetIndex(0)

    def closeEvent(self, event):
        print("Closing")
        self.setParent(None)

    def itemToggle(self):
        current_item = self.list_widget.selectedItems()[0]
        item_name = current_tem.text()
        items = self.listGetItems()
        item_names = [item.text() for item in items]
        index = item_names.index(item_name)

        vis = self.vis_arr[index]
        state = vis.isActive(self.viewport)

        vis.setIsActive(not state, self.viewport)

        if state:
            current_item.setCheckState(Qt.Unchecked)
        else:
            current_item.setCheckState(Qt.Checked)

    def listFilter(self):
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
        self.listSetIndex(0)

    def listGetItems(self):
        item_count = self.list_widget.count()
        items = [self.list_widget.item(i) for i in range(item_count)]
        return(items)

    def listGetVisibleItems(self):
        item_count = self.list_widget.count()
        items = []
        for i in range(item_count):
            item = self.list_widget.item(i)
            if not item.isHidden():
                items.append(item)
        return(items)

    def listNext(self):
        visible_items = self.listGetVisibleItems()
        current_item = self.list_widget.selectedItems()[0]
        index = visible_items.index(current_item)
        index = (index + 1) % len(visible_items)
        self.listSetIndex(index)

    def listPrev(self):
        visible_items = self.listGetVisibleItems()
        current_item = self.list_widget.selectedItems()[0]
        index = visible_items.index(current_item)
        index = (index - 1) % len(visible_items)
        self.listSetIndex(index)

    def listSetIndex(self, index):
        visible_items = self.listGetVisibleItems()
        counter = 0
        for visible_item in visible_items:
            if counter == index:
                self.list_widget.setItemSelected(visible_item, 1)
                return
            counter += 1
