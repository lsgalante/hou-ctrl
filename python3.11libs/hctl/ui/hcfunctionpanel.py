import hou, inspect, platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from fuzzyfinder import fuzzyfinder
import hctl_utils as hcu
from .core.hcsession import HCSession
from .core.hcpane import HCPane
from .core.hcpanetab import HCPaneTab
from importlib import reload


class HCFunctionPanel(QtWidgets.QDialog):
    def __init__(self):
        super(HCFunctionPanel, self).__init__( hou.qt.mainWindow() )
        ## WINDOW PARAMETERSs
        self.resize(900, 400)
        self.setWindowTitle("hcfunctionpanel")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        # Focus the input line AFTER setting window flags
        self.functionPanel.inputLine.setFocus()

        ## OBJECTS
        # hou objects
        pane = hou.ui.paneUnderCursor()
        paneTab = hou.ui.paneTabUnderCursor()
        # hc objects
        self.hCSession = HCSession()
        self.hCPane = HCPane(pane)
        self.hCPaneTab = HCPaneTab(paneTab)
        # self.hCviewport = self.hCPaneTab.viewport

        ## PATHS
        self.project_path = hou.hipFile.name()
        ct = self.project_path.count("/")
        self.project_path = self.project_path.split("/", ct - 2)[-1]
        self.network_path = self.paneTab.pwd()

        ## LAYOUT
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.functionPanel = FunctionPanel(self)
        self.mainLayout.addWidget(self.functionPanel)
        # Apply layout
        self.setLayout(self.mainLayout)


    def closeEvent(self, event):
        self.setParent(None)


    def lists(self):
        # Define various arrays for navigating pane tabs
        self.paneTab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
        self.paneTab_names = [paneTab.name() for paneTab in self.hctlSession.tabs()]
        self.paneTab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
        # Populate pane tab labels array
        self.paneTab_labels = []
        for paneTab in self.hctlSession.tabs():
            index = self.paneTab_types.index(paneTab.type())
            label = self.paneTab_type_names[index]
            self.paneTab_labels.append(label)


    def nodes(self):
        self.node = self.hctlPaneTab.currentNode()


class FunctionPanel(QtWidgets.QFrame):
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
        self.setFixedWidth(300)


    class InputLine(QtWidgets.QLineEdit):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.owner = owner
            # self.returnPressed.connect(self.functionList.exec)
            self.key_ctl_n = QtCore.Signal()
            self.key_ctl_p = QtCore.Signal()
            self.key_down = QtCore.Signal()
            self.key_up = QtCore.Signal()
            # Enable fuzzy finding filter
            self.textEdited.connect(self.filter)


        def event(self, event):
            if event.type() == QtCore.QEvent.Type.KeyPress:
                key = event.key()
                mods = event.modifiers()
                # Choose modifiers based on platform
                sys = platform.system()
                modifier = None

                # Macos or linux
                if sys == "Darwin":
                    modifier = Qt.MetaModifier
                elif sys == "linux":
                    modifier = Qt.ControlModifier

                # Highlight next item
                if mods == modifier and key == Qt.Key_N:
                    self.next()
                    return True
                elif key == Qt.Key_Down:
                    self.next()
                    return True

                # Highlight previous item
                elif mods == modifier and key == Qt.Key_P:
                    self.prev()
                    return True
                elif key == Qt.Key_Up:
                    self.prev()
                    return True

                # Upon nothing
                return QtWidgets.QLineEdit.event(self, event)
            else:
                return QtWidgets.QLineEdit.event(self, event)


        def filter(self):
            query = self.text()
            items = self.functionList.items()
            item_names = [item.text() for item in items]
            matches = list( fuzzyfinder(query, item_names) )
            for item in items:
                if item.text() in matches:
                    item.setHidden(0)
                else:
                    item.setHidden(1)
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


    class FunctionList(QtWidgets.QListWidget):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.owner = owner
            self.populate()
            self.itemClicked.connect(self.execute)
            self.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
            self.setIndex(0)


        def execute(self):
            items = self.items()
            currentItem = self.selectedItems()[0]
            index = items.index(currentItem)
            item = items[index]
            label = item.text()
            obj_name, method_name = label.split(".")
            # Populate functions based on context
            if obj_name == "HctlNetworkEditor":
                method = getattr(self.owner.hctlNetworkEditor, method_name)
                method()
            elif obj_name == "HctlPane":
                method = getattr(self.owner.hctlPane, method_name)
                method()
            elif obj_name == "HctlPaneTab":
                method = getattr(self.owner.hctlPaneTab, method_name)
                method()
            elif obj_name == "HctlSceneViewer":
                method = getattr(self.owner.hctlSceneViewer, method_name)
                method()
            elif obj_name == "HctlSession":
                method = getattr(self.owner.hctlSession, method_name)
                method()
            # Close window on function execution
            # self.accept()


        def items(self):
            item_count = self.count()
            items = [self.item(i) for i in range(item_count)]
            return(items)


        def populate(self):
            items = []

            for name, obj in inspect.getmembers(hcu.HctlNetworkEditor, inspect.isfunction):
                if hasattr(obj, "interactive") and obj.interactive:
                    items.append(("HctlNetworkEditor", name))

            for name, obj in inspect.getmembers(hcu.HctlPane, inspect.isfunction):
                if hasattr(obj, "interactive") and obj.interactive:
                    items.append(("HctlPane", name))

            for name, obj in inspect.getmembers(hcu.HctlPaneTab, inspect.isfunction):
                if hasattr(obj, "interactive") and obj.interactive:
                    items.append(("HctlPaneTab", name))

            if self.owner.hctlPaneTab.type() == hou.paneTabType.SceneViewer:
                for name, obj in inspect.getmembers(hcu.HctlSceneViewer, inspect.isfunction):
                    if hasattr(obj, "interactive") and obj.interactive:
                        items.append(("HctlSceneViewer", name))

            for name, obj in inspect.getmembers(hcu.HctlSession, inspect.isfunction):
                if hasattr(obj, "interactive") and obj.interactive:
                    items.append(("HctlSession", name))

            for item in items:
                self.addItem(item[0] + "." + item[1])


        def setIndex(self, index):
            items = self.items()
            counter = 0
            for item in items:
                if not item.isHidden():
                    if counter == index:
                        self.setCurrentItem(item)
                    counter += 1
