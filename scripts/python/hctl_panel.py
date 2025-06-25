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

        # Window
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.resize(600, 400)
        self.setWindowTitle("hctl")


    def update(self):
        reload(hcu)

        pane = hou.ui.paneUnderCursor()
        self.paneTab = hcu.HctlPaneTab(hou.ui.paneTabUnderCursor())
        self.paneTabs = pane.tabs()

        self.paneTab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
        self.paneTab_names = [paneTab.name() for paneTab in self.paneTabs]
        self.paneTab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
        self.paneTab_labels = []
        for paneTab in self.paneTabs:
            index = self.paneTab_types.index(paneTab.type())
            label = self.paneTab_type_names[index]
            self.paneTab_labels.append(label)


        self.session = hcu.HctlSession()
        self.pane = hcu.HctlPane(pane)
        # self.paneTab = hcu.PaneTab(self, paneTab)
        # self.printer = hcu.Printer()
        print()
        self.context = self.paneTab.type()

        # if self.context == hou.paneTabType.SceneViewer:
            # self.sceneViewer = hcu.SceneViewer(self, paneTab)
            # self.viewport = self.sceneViewer.viewport
        # if self.context == hou.paneTabType.NetworkEditor:
            # self.networkEditor = hcu.NetworkEditor(self, paneTab)

        self.project_path= hou.hipFile.name()
        self.network_path = self.paneTab.pwd()
        self.node = self.paneTab.currentNode()


    def closeEvent(self, event):
        self.setParent(None)



class UpperPanel(QtWidgets.QFrame):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

        layout = QtWidgets.QGridLayout()

        layout.addWidget(QtWidgets.QLabel("Project path:"), 0, 0)
        layout.addWidget(QtWidgets.QLabel(owner.project_path), 0, 1)

        layout.addWidget(QtWidgets.QLabel("Network path:"), 1, 0)
        layout.addWidget(QtWidgets.QLabel(str(owner.network_path) + "/" + str(owner.node)), 1, 1)

        layout.addWidget(QtWidgets.QLabel("Tab index:"), 2, 0)
        layout.addWidget(self.PaneTabMenu(owner), 2, 1)

        layout.addWidget(QtWidgets.QLabel("Tab type:"), 3, 0)
        layout.addWidget(self.PaneTabTypeMenu(owner), 3, 1)

        layout.addWidget(self.AutoSaveCheckBox(owner),  4, 0)
        layout.addWidget(self.PinCheckBox(owner), 5, 0)

        layout.setRowMinimumHeight(0, 20)
        layout.setRowMinimumHeight(1, 20)
        layout.setRowMinimumHeight(2, 20)
        layout.setRowMinimumHeight(3, 20)
        layout.setRowMinimumHeight(4, 20)
        layout.setRowMinimumHeight(5, 20)

        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(1)
        self.setLayout(layout)
        self.setFixedHeight(180)



    class PaneTabMenu(QtWidgets.QComboBox):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            self.addItems(owner.paneTab_labels)
            self.activated.connect(self.change)


        def change(self):
            index = self.tabMenu.currentIndex()
            paneTab = self.owner.paneTabs[index]
            paneTab.setIsCurrentTab()



    class PaneTabTypeMenu(QtWidgets.QComboBox):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            self.addItems(owner.paneTab_type_names)
            key = str(owner.context)
            key = key.lstrip("paneTabType")
            key = key.lstrip(".")
            self.setCurrentIndex(owner.paneTab_type_names.index(key))
            self.activated.connect(self.change)


        def change(self):
            index = self.paneTabTypeMenu.currentIndex()
            self.paneTab = self.paneTab.setType(self.owner.paneTab_types[index])



    class AutoSaveCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner):
            super().__init__("Autosave")
            state = owner.session.autosave_state
            if state == "1": self.setCheckState(Qt.Checked)
            elif state == "0": self.setCheckState(Qt.Unchecked)
            self.clicked.connect(owner.session.toggleAutoSave)



    class PinCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner):
            super().__init__("Pin tab")
            self.owner = owner
            self.clicked.connect(self.togglePin)
            if owner.paneTab.paneTab.isPin():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)


        def togglePin(self):
            self.owner.paneTab.togglePin()



class LowerPanel(QtWidgets.QFrame):
    def __init__(self, owner):
        super().__init__()
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
            self.populate()
            self.itemClicked.connect(self.execute)
            self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
            self.setFocusPolicy(Qt.StrongFocus)
            self.setIndex(0)


        def execute(self):
            items = self.items()
            currentItem = self.selectedItems()[0]
            index = items.index(currentItem)
            item = items[index]
            label = item.text()
            obj_name, method_name = label.split(".")

            if obj_name == "HctlNetworkEditor":
                method = getattr(self.owner.networkEditor, method_name)
                method()
            elif obj_name == "HctlPane":
                method = getattr(self.owner.pane, method_name)
                method()
            elif obj_name == "HctlPaneTab":
                method = getattr(self.owner.paneTab, method_name)
                method()
            elif obj_name == "HctlSceneViewer":
                method = getattr(self.owner.sceneViewer, method_name)
                method()
            elif obj_name == "HctlSession":
                method = getattr(self.owner.session, method_name)
                method()

            # self.accept()


        def items(self):
            item_count = self.count()
            items = [self.item(i) for i in range(item_count)]
            return(items)


        def populate(self):
            items = []
            for class_name, class_obj in inspect.getmembers(hcu, inspect.isclass):
                if class_obj.__module__ == hcu.__name__: # skip over imported modules
                    for func_name, func_obj in inspect.getmembers(class_obj, inspect.isfunction):
                        if hasattr(func_obj, "interactive_contexts"):
                            # print(self.owner.context, func_obj.interactive_contexts)
                            if "all" in func_obj.interactive_contexts:
                                return
                                # items.append((class_name, func_name))
                            # elif str(self.owner.context) in func_obj.interactive_contexts:
                                # items.append((class_name, func_name))
            for item in items:
                self.addItem(item[0] + "." + item[1])


        def setIndex(self, index):
            items = self.items()
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
            self.textEdited.connect(self.filter)


        def event(self, event):
            if event.type() == QtCore.QEvent.Type.KeyPress:
                key = event.key()
                mods = event.modifiers()
                sys = platform.system()
                modifier = None
                if sys == "Darwin": modifier = Qt.MetaModifier
                elif sys == "linux": modifier = Qt.ControlModifier
                if mods == modifier and key == Qt.Key_N: self.next(); return True
                elif mods == modifier and key == Qt.Key_P: self.prev(); return True
                elif key == Qt.Key_Up: self.prev(); return True
                elif key == Qt.Key_Down: self.next(); return True
                return QtWidgets.QLineEdit.event(self, event)
            else:
                return QtWidgets.QLineEdit.event(self, event)


        def filter(self):
            query = self.text()
            items = self.functionList.items()
            item_names = [item.text() for item in items]
            matches = list( fuzzyfinder(query, item_names) )
            for item in items:
                if item.text() in matches: item.setHidden(0)
                else: item.setHidden(1)
            self.functionList.setIndex(0)


        def visibleItems(self):
            item_count = self.functionList.count()
            items = []
            for i in range(item_count):
                item = self.functionList.item(i)
                if not item.isHidden():
                    items.append(item)
            return(items)


        def next(self):
            items = self.visibleItems()
            currentItem = self.functionList.selectedItems()[0]
            index = items.index(currentItem)
            index = (index + 1) % len(items)
            self.functionList.setIndex(index)


        def prev(self):
            items = self.visibleItems()
            currentItem = self.functionList.selectedItems()[0]
            index = items.index(currentItem)
            index = (index - 1) % len(items)
            self.functionList.setIndex(index)
