import hou, inspect, platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from fuzzyfinder import fuzzyfinder
import hctl_utils as hcu
from importlib import reload


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__(hou.qt.mainWindow())
        self.update()
        self.upperPanel = UpperPanel(self)
        self.lowerPanel = LowerPanel(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.upperPanel)
        self.layout.addWidget(self.lowerPanel)
        self.setLayout(self.layout)
        # Window Appearance
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.resize(600, 400)
        self.setWindowTitle("hctl")


    def update(self):
        # pane = hou.ui.paneUnderCursor()
        # paneTab = hou.ui.paneTabUnderCursor()

        reload(hcu)
        self.session = hcu.HctlSession()
        # self.desktop = hcu.Desktop(self)
        # self.pane = hcu.Pane(self, pane)
        # self.paneTab = hcu.PaneTab(self, paneTab)
        # self.printer = hcu.Printer()

        # self.context = self.paneTab.getType()

        # if self.context == hou.paneTabType.SceneViewer:
            # self.sceneViewer = hcu.SceneViewer(self, paneTab)
            # self.viewport = self.sceneViewer.viewport
        # if self.context == hou.paneTabType.NetworkEditor:
            # self.networkEditor = hcu.NetworkEditor(self, paneTab)

        # self.networkPath = self.paneTab.getPath()
        # self.paneTabs = self.pane.getTabs()
        # self.node = self.paneTab.currentNode()
        # self.filePath = hou.hipFile.name()


    def closeEvent(self, event):
        self.setParent(None)


class UpperPanel(QtWidgets.QFrame):
    def __init__(self, owner, parent=None):
        super().__init__(parent)
        self.owner = owner

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("File:"),     0, 0)
        layout.addWidget(QtWidgets.QLabel("Node:    "), 1, 0)
        layout.addWidget(QtWidgets.QLabel("Context:"),  2, 0)
        layout.addWidget(QtWidgets.QLabel("Pane Tab:"), 3, 0)
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

        self.pane_tab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
        self.pane_tab_names = [paneTab.name() for paneTab in owner.paneTabs]
        self.pane_tab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
        self.pane_tab_labels = []
        for paneTab in owner.paneTabs:
            index = self.pane_tab_types.index(paneTab.type())
            label = self.pane_tab_type_names[index]
            self.pane_tab_labels.append(label)


    class PaneTabMenu(QtWidgets.QComboBox):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
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
            # self.clicked.connect(owner.session.autosave_state)


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


class LowerPanel(QtWidgets.QFrame):
    def __init__(self, owner, parent=None):
        super().__init__(parent)
        self.owner = owner
        self.functionList = self.FunctionList(owner)
        self.inputLine = self.InputLine(owner)
        self.inputLine.functionList = self.functionList
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.inputLine)
        layout.addWidget(self.functionList)
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(1)
        self.setLayout(layout)
        self.inputLine.setFocus()


    class FunctionList(QtWidgets.QListWidget):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.owner = owner
            self.items = self.getItems()
            self.populate()
            self.itemClicked.connect(self.exec)
            self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
            self.setFocusPolicy(Qt.StrongFocus)
            self.setIndex(0)


        def exec(self):
            items = self.getItems()
            currentItem = self.selectedItems()[0]
            index = items.index(currentItem)
            item = self.items[index]
            print(item)
            if item[0] == "Desktop":
                eval("self.owner.desktop." + item[1] + "()")

            # self.items[index][1](self.owner.paneTab)
            # self.accept()

        def getItems(self):
            item_count = self.count()
            items = [self.item(i) for i in range(item_count)]
            return(items)


        def populate(self):
            self.items = []
            for class_name, class_obj in inspect.getmembers(hcu, inspect.isclass):
                if class_obj.__module__ == hcu.__name__:
                    for func_name, func_obj in inspect.getmembers(class_obj, inspect.isfunction):
                        if hasattr(func_obj, "interactive_contexts"):
                            if "all" in func_obj.interactive_contexts:
                                self.items.append((class_name, func_name))
                            elif str(self.owner.context) in func_obj.interactive_contexts:
                                # print(class_name + "." + func_name)
                                self.items.append((class_name, func_name))
            for item in self.items:
                # print(item[0])
                self.addItem(item[0] + "." + item[1])


        def setIndex(self, index):
            items = self.getItems()
            counter = 0
            for item in items:
                if not item.isHidden():
                    if counter == index:
                        self.setItemSelected(item, 1)
                    counter += 1


    class InputLine(QtWidgets.QLineEdit):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.owner = owner
            # self.returnPressed.connect(self.functionList.exec)
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
                sys = platform.system()
                modifier = None
                if sys == "Darwin":
                    modifier = Qt.MetaModifier
                elif sys == "linux":
                    modifier = Qt.ControlModifier
                if mods == modifier and key == Qt.Key_N:
                    self.next()
                    # self.key_ctl_n.emit(); return True
                    return True
                elif mods == modifier and key == Qt.Key_P:
                    self.prev()
                    # self.key_ctl_p.emit(); return True
                    return True
                elif key == Qt.Key_Up:
                    self.prev()
                    # self.key_ctl_p.emit(); return True
                    return True
                elif key == Qt.Key_Down:
                    self.next()
                    # self.key_ctl_n.emit(); return True
                    return True
                return QtWidgets.QLineEdit.event(self, event)
            else:
                return QtWidgets.QLineEdit.event(self, event)


        def filter(self):
            query = self.text()
            items = self.functionList.getItems()
            item_names = [item.text() for item in items]
            matches = list( fuzzyfinder(query, item_names) )
            for item in items:
                if item.text() in matches:
                    item.setHidden(0)
                else:
                    item.setHidden(1)
            self.functionList.setIndex(0)


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


        def prev(self):
            items = self.getVisibleItems()
            currentItem = self.selectedItems()[0]
            index = items.index(currentItem)
            index = (index - 1) % len(items)
            self.setIndex(index)
