import hou, inspect, platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFrame, QLineEdit, QGridLayout, QLabel, QVBoxLayout, QListWidgetItem, QBoxLayout, QDialog, QListWidget
from PySide2.QtCore import Qt
from fuzzyfinder import fuzzyfinder
import hctl_utils as hcu
from importlib import reload


class Controls(QtWidgets.QFrame):
    def __init__(self, owner, parent=None):
        super().__init__(parent)
        self.owner = owner

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("File:"),     0, 0)
        layout.addWidget(QtWidgets.QLabel("Node:    "), 1, 0)
        layout.addWidget(QtWidgets.QLabel("Context:"),  2, 0)
        layout.addWidget(QtWidgets.QLabel("Pant Tab:"), 3, 0)
        layout.addWidget(self.AutoSaveCheckBox(owner),  4, 0)
        layout.addWidget(self.PinCheckBox(owner),       5, 0)

        layout.addWidget(QtWidgets.QLabel(owner.filePath), 0, 1)
        layout.addWidget(QtWidgets.QLabel(owner.networkPath + "/" + str(owner.node)), 1, 1)
        layout.addWidget(self.PaneTabTypeMenu(owner), 2, 1)
        layout.addWidget(self.PaneTabMenu(owner), 3, 1)

        top_frame_h = 190
        row_h = top_frame_h / 5
        layout.setRowMinimumHeight(0, row_h)
        layout.setRowMinimumHeight(1, row_h)
        layout.setRowMinimumHeight(2, row_h)
        layout.setRowMinimumHeight(3, row_h)
        layout.setRowMinimumHeight(4, row_h)
        layout.setRowMinimumHeight(5, row_h)

        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(1)
        self.setLayout(layout)
        self.setFixedHeight(top_frame_h)


    class PaneTabMenu(QtWidgets.QComboBox):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.pane_tab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
            self.pane_tab_names = [paneTab.name() for paneTab in owner.paneTabs]
            self.pane_tab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
            self.pane_tab_labels = []
            for paneTab in owner.paneTabs:
                index = self.pane_tab_types.index(paneTab.type())
                label = self.pane_tab_type_names[index]
                self.pane_tab_labels.append(label)
            self.addItems(self.pane_tab_labels)
            self.activated.connect(self.change)

        def change(self):
            index = self.tabMenu.currentIndex()
            paneTab = self.paneTabs[index]
            paneTab.setIsCurrentTab()


    class PaneTabTypeMenu(QtWidgets.QComboBox):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.pane_tab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
            self.pane_tab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
            self.addItems(self.pane_tab_type_names)
            key = str(owner.context)
            key = key.lstrip("paneTabType")
            key = key.lstrip(".")
            self.setCurrentIndex(self.pane_tab_type_names.index(key))
            self.activated.connect(self.change)

        def change(self):
            index = self.paneTabTypeMenu.currentIndex()
            self.paneTab = self.paneTab.setType(self.pane_tab_types[index])


    class AutoSaveCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner, parent=None):
            super().__init__("Check me", parent)
            state = owner.session.autosave_state
            if state == "1":
                self.setCheckState(Qt.Checked)
            elif state == "0":
                self.setCheckState(Qt.Unchecked)
            self.clicked.connect(owner.session.autosave_state)


    class PinCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner, parent=None):
            super().__init__("Pin x", parent)
            if owner.paneTab.isPin:
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)
                self.clicked.connect(self.togglePin)

        def togglePin(self):
            hcu.paneTabTogglePin(self.paneTab)



class FunctionList(QtWidgets.QFrame):
    def __init__(self, owner, parent=None):
        super().__init__(parent)
        self.owner = owner
        layout = QtWidgets.QVBoxLayout()

        self.filterBox = self.FilterBox(owner)
        self.list = self.List(owner)
        layout.addWidget(self.filterBox)
        layout.addWidget(self.list)
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.Panel)
        frame.setLineWidth(1)
        frame.setLayout(layout)
        self.setIndex(0)
        self.filterBox.setFocus()

    def exec(self):
        items = self.getItems()
        currentItem = self.selectedItems()[0]
        index = items.index(currentItem)
        self.items[index][1](self.owner.paneTab)
        self.accept()

    def setIndex(self, index):
        items = self.list.getItems()
        counter = 0
        for item in items:
            if not item.isHidden():
                if counter == index:
                    self.functionList.setItemSelected(item, 1)
                counter += 1

    class List(QtWidgets.QListWidget):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.items = self.getItems()
            self.itemClicked.connect(owner.exec)
            self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
            self.setFocusPolicy(Qt.StrongFocus)

        def getItems(self):
            item_count = self.count()
            items = [self.item(i) for i in range(item_count)]
            return(items)

    class FilterBox(QtWidgets.QLineEdit):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            # Callbacks
            self.returnPressed.connect(owner.exec)
            self.key_ctl_n = QtCore.Signal()
            self.key_ctl_p = QtCore.Signal()
            self.key_down = QtCore.Signal()
            self.key_up = QtCore.Signal()
            # self.key_ctl_n.connect(self.listNext)
            # self.key_ctl_p.connect(self.listPrev)
            # self.key_down.connect(self.listNext)
            # self.key_up.connect(self.listPrev)
            self.textEdited.connect(self.filter)

        def event(self, event):
            if event.type() == QtCore.QEvent.Type.KeyPress:
                key = event.key()
                mods = event.modifiers()
                os = platform.system()
                if mods == Qt.MetaModifier and os == "Darwin":
                    if key == Qt.Key_N:
                        self.listNext(); return True
                        # self.key_ctl_n.emit(); return True
                    elif key == Qt.Key_P:
                        self.listPrev(); return True
                        # self.key_ctl_p.emit(); return True
                        #
                elif mods == Qt.ControlModifier and os == "linux":
                    if key == Qt.Key_N:
                        self.listNext(); return True
                        # self.key_ctl_n.emit(); return True
                    elif key == Qt.Key_P:
                        self.listPrev(); return True
                        # self.key_ctl_p.emit(); return True

                elif key == Qt.Key_Up:
                    self.listPrev(); return True
                    # self.key_ctl_p.emit(); return True
                elif key == Qt.Key_Down:
                    self.listNext(); return True
                    # self.key_ctl_n.emit(); return True
                return QtWidgets.QLineEdit.event(self, event)
            else:
                return QtWidgets.QLineEdit.event(self, event)

        def filter(self):
            query = self.text()
            items = self.getItems()
            item_names = [item.text() for item in items]
            matches = list( fuzzyfinder(query, item_names) )
            for item in items:
                if item.text() in matches:
                    item.setHidden(0)
                else:
                    item.setHidden(1)
            self.setIndex(0)

        def getVisibleItems(self):
            item_count = self.functionList.count()
            items = []
            for i in range(item_count):
                item = self.functionList.item(i)
                if not item.isHidden():
                    items.append(item)
            return(items)

        def next(self):
            items = self.getVisibleItems()
            currentItem = self.functionList.selectedItems()[0]
            index = items.index(currentItem)
            index = (index + 1) % len(items)
            self.setIndex(index)

        def populate(self):
            self.items = []
            funcs = inspect.getmembers(hcu)
            for func in funcs:
                name = func[0]
                obj = func[1]
                if hasattr(obj, "interactive_contexts"):
                    if "all" in obj.interactive_contexts:
                        self.items.append((name, obj))
                    elif str(self.context) in obj.interactive_contexts:
                        self.items.append((name, obj))

            for item in self.items:
                self.addItem(item[0])

        def prev(self):
            items = self.getVisibleItems()
            currentItem = self.selectedItems()[0]
            index = items.index(currentItem)
            index = (index - 1) % len(items)
            self.setIndex(index)



class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__(hou.qt.mainWindow())
        self.session = hcu.Session()
        self.update()

        self.controls = Controls(self)
        self.functionList = FunctionList(self)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.controls)
        self.layout.addWidget(self.functionList)
        self.setLayout(self.layout)
        # Window Appearance
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.resize(600, 400)
        self.setWindowTitle("hctl")

    # Listeners
    def closeEvent(self, event):
        self.setParent(None)

    def update(self):
        reload(hcu)
        # Parameters
        self.pane = hcu.Pane(hou.ui.paneUnderCursor())
        self.paneTab = hcu.PaneTab(hou.ui.paneTabUnderCursor())
        self.paneTabs = self.pane.getTabs()
        self.networkPath = self.paneTab.getPath()
        self.node = self.paneTab.currentNode()
        self.filePath = hou.hipFile.name()
        self.context = self.paneTab.getType()
        if self.context == hou.paneTabType.SceneViewer:
            self.sceneViewer = hcu.SceneViewer(self.paneTab.paneTab)
            self.viewport = self.sceneViewer.viewport
