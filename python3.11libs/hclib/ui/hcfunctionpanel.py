import hou, inspect, platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from fuzzyfinder import fuzzyfinder
from .core.hcglobal import HCGlobal
from .core.hcpane import HCPane
from .core.tab import HCTab
from importlib import reload


class HCFunctionPanel(QtWidgets.QDialog):
    def __init__(self):
        super(HCFunctionPanel, self).__init__(hou.qt.mainWindow())

        ## WINDOW PARAMETERS
        self.resize(900, 400)
        self.setWindowTitle("hcfunctionpanel")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        # Focus the input line AFTER setting window flags
        self.functionPanel.inputLine.setFocus()

        ## OBJECTS
        self.hc_global = HCGlobal()
        self.hc_pane = self.hc_global.hcPane()
        self.hc_tab = self.hc_global.hcTab()
        # self.hc_viewport = self.hc_tab.viewport()

        ## PATHS
        self.project_path = self.hc_global.projectPath()
        ct = self.project_path.count('/')
        self.project_path = self.project_path.split('/', ct - 2)[-1]
        self.network_path = self.hc_tab.pwd()

        ## LAYOUT
        self.main_layout = QtWidgets.QHBoxLayout()
        self.function_panel = FunctionPanel(self)
        self.main_layout.addWidget(self.function_panel)
        self.setLayout(self.main_layout)

    def closeEvent(self, event):
        self.setParent(None)

    def lists(self):
        # Define various arrays for navigating tabs
        self.tab_names = [tab.name() for tab in self.hc_global.tabs()]
        self.tab_types = (
            hou.paneTabType.ApexEditor,
            hou.paneTabType.CompositorViewer,
            hou.paneTabType.DetailsView,
            hou.paneTabType.NetworkEditor,
            hou.paneTabType.Parm,
            hou.paneTabType.PythonPanel,
            hou.paneTabType.PythonShell,
            hou.paneTabType.SceneViewer,
            hou.paneTabType.Textport
        )
        self.tab_type_names = (
            "ApexEditor",
            "CompositorViewer",
            "DetailsView",
            "NetworkEditor",
            "Parm",
            "PythonPanel",
            "PythonShell",
            "SceneViewer",
            "Textport"
        )
        self.tab_labels = []
        for tab in self.hc_global.tabs():
            index = self.tab_types.index(tab.type())
            label = self.tab_type_names[index]
            self.tab_labels.append(label)

    def nodes(self):
        self.node = self.hc_tab.currentNode()


class FunctionPanel(QtWidgets.QFrame):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.function_list = self.FunctionList(owner)
        self.input_line = self.InputLine(owner)
        self.input_line.function_list = self.function_list
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.input_line)
        layout.addWidget(self.function_list)
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(1)
        self.setLayout(layout)
        self.setFixedWidth(300)


    class InputLine(QtWidgets.QLineEdit):
        def __init__(self, owner, parent=None):
            super().__init__(parent)
            self.owner = owner
            # self.returnPressed.connect(self.function_list.exec)
            self.key_ctl_n = QtCore.Signal()
            self.key_ctl_p = QtCore.Signal()
            self.key_down = QtCore.Signal()
            self.key_up = QtCore.Signal()
            # Enable fuzzy search
            self.textEdited.connect(self.filter)

        def event(self, event):
            if event.type() == QtCore.QEvent.Type.KeyPress:
                key = event.key()
                mods = event.modifiers()
                # Choose modifiers based on platform
                sys = platform.system()
                modifier = None

                # Macos or linux
                if sys == 'Darwin':
                    modifier = Qt.MetaModifier
                elif sys == 'linux':
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
            items = self.function_list.items()
            item_names = [item.text() for item in items]
            matches = list(fuzzyfinder(query, item_names))
            for item in items:
                if item.text() in matches:
                    item.setHidden(0)
                else:
                    item.setHidden(1)
            self.function_list.setIndex(0)

        def visibleItems(self):
            item_count = self.function_list.count()
            items = []
            for i in range(item_count):
                item = self.function_list.item(i)
                if not item.isHidden():
                    items.append(item)
            return(items)

        def next(self):
            items = self.visibleItems()
            current_item = self.function_list.selectedItems()[0]
            index = items.index(current_item)
            index = (index + 1) % len(items)
            self.function_list.setIndex(index)

        def prev(self):
            items = self.visibleItems()
            current_item = self.function_list.selectedItems()[0]
            index = items.index(current_item)
            index = (index - 1) % len(items)
            self.function_list.setIndex(index)


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
            current_item = self.selectedItems()[0]
            index = items.index(current_item)
            item = items[index]
            label = item.text()
            obj_name, method_name = label.split('.')
            # Populate functions based on context
            if obj_name == 'HCNetworkEditor':
                method = getattr(self.owner.hcNetworkEditor, method_name)
                method()
            elif obj_name == 'HCPane':
                method = getattr(self.owner.hcPane, method_name)
                method()
            elif obj_name == 'HCTab':
                method = getattr(self.owner.hcTab, method_name)
                method()
            elif obj_name == 'HCSceneViewer':
                method = getattr(self.owner.hcSceneViewer, method_name)
                method()
            elif obj_name == 'HCGlobal':
                method = getattr(self.owner.hcGlobal, method_name)
                method()
            # Close window on function execution
            # self.accept()

        def items(self):
            item_count = self.count()
            items = [self.item(i) for i in range(item_count)]
            return(items)

        def populate(self):
            items = []

            for name, obj in inspect.getmembers(HCNetworkEditor, inspect.isfunction):
                if hasattr(obj, 'interactive') and obj.interactive:
                    items.append(('HCNetworkEditor', name))

            for name, obj in inspect.getmembers(hcu.HCPane, inspect.isfunction):
                if hasattr(obj, 'interactive') and obj.interactive:
                    items.append(('HCPane', name))

            for name, obj in inspect.getmembers(hcu.HCTab, inspect.isfunction):
                if hasattr(obj, 'nteractive') and obj.interactive:
                    items.append(('HCTab', name))

            if self.owner.hc_tab.type() == hou.paneTabType.SceneViewer:
                for name, obj in inspect.getmembers(HCSceneViewer, inspect.isfunction):
                    if hasattr(obj, 'interactive') and obj.interactive:
                        items.append(('HCSceneViewer', name))

            for name, obj in inspect.getmembers(HCGlobal, inspect.isfunction):
                if hasattr(obj, 'interactive') and obj.interactive:
                    items.append(('HCGlobal', name))

            for item in items:
                self.addItem(item[0] + '.' + item[1])

        def setIndex(self, index):
            items = self.items()
            counter = 0
            for item in items:
                if not item.isHidden():
                    if counter == index:
                        self.setCurrentItem(item)
                    counter += 1
