import hou, inspect, platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from fuzzyfinder import fuzzyfinder
import hctl_utils as hcu
from importlib import reload


class Dialog(QtWidgets.QDialog):

    def __init__(self):
        super(Dialog, self).__init__( hou.qt.mainWindow() )
        # Update class attributes
        self.update()
        # Window appearance
        self.resize(900, 400)
        self.setWindowTitle("hctl")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        # Finally, focus the input line AFTER setting window flags
        self.functionPanel.inputLine.setFocus()


    def closeEvent(self, event):
        # Unparent from main houdini window when closing
        self.setParent(None)


    def contexts(self):
        # hctl session
        self.hctlSession = hcu.HctlSession()
        # hctl pane
        pane = hou.ui.paneUnderCursor()
        self.hctlPane = hcu.HctlPane(pane)
        # hctl pane tab
        paneTab = hou.ui.paneTabUnderCursor()
        self.hctlPaneTab = hcu.HctlPaneTab(paneTab)
        # Additional contexts by pane tab type
        if self.hctlPaneTab.type() == hou.paneTabType.SceneViewer:
            self.hctlSceneViewer = hcu.HctlSceneViewer(paneTab)
        if self.hctlPaneTab.type() == hou.paneTabType.NetworkEditor:
            self.hctlNetworkEditor = hcu.HctlNetworkEditor(paneTab)
        # Viewport (needs work)
        # self.viewport = self.sceneViewer.viewport


    def layout(self):
        # Top-level layout
        self.mainLayout = QtWidgets.QHBoxLayout()
        # Controls column
        self.controlPanel = ControlPanel(self)
        self.mainLayout.addWidget(self.controlPanel)
        # Functions column
        self.functionPanel = FunctionPanel(self)
        self.mainLayout.addWidget(self.functionPanel)
        # Apply layout
        self.setLayout(self.mainLayout)


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


    def paths(self):
        # Project path
        self.project_path = hou.hipFile.name()
        ct = self.project_path.count("/")
        self.project_path = self.project_path.split("/", ct - 2)[-1]
        # Network path
        self.network_path = self.paneTab.pwd()


    def update(self):
        reload(hcu)
        self.contexts()
        self.lists()
        self.layout()



# Panel with the buttons
class ControlPanel(QtWidgets.QFrame):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

        # SESSION CONTROLS
        sessionColumn = QtWidgets.QVBoxLayout()
        sessionColumn.addWidget(QtWidgets.QLabel("Session"))
        # Autosave
        sessionColumn.addWidget(self.AutoSaveCheckBox(owner))
        # Toggle all menus
        sessionMenusButton = QtWidgets.QPushButton("Menus")
        sessionMenusButton.clicked.connect(owner.hctlSession.toggleMenus)
        sessionColumn.addWidget(sessionMenusButton)
        # Toggle all panetabs
        sessionPaneTabsButton = QtWidgets.QPushButton("Pane Tabs")
        sessionPaneTabsButton.clicked.connect(owner.hctlSession.togglePaneTabs)
        sessionColumn.addWidget(sessionPaneTabsButton)
        # Toggle all network controls
        sessionNetworkControlsButton = QtWidgets.QPushButton("Network Controls")
        sessionNetworkControlsButton.clicked.connect(owner.hctlSession.toggleNetworkControls)
        sessionColumn.addWidget(sessionNetworkControlsButton)
        # Toggle all stowbars
        stowbarsButton = QtWidgets.QPushButton("Stowbars")
        stowbarsButton.clicked.connect(owner.hctlSession.toggleStowbars)
        sessionColumn.addWidget(stowbarsButton)
        # Reload color schems
        reloadColorsButton = QtWidgets.QPushButton("Reload colors")
        reloadColorsButton.clicked.connect(owner.hctlSession.reloadColorSchemes)
        sessionColumn.addWidget(reloadColorsButton)
        # Fill empty space
        sessionColumn.addStretch()

        # PANE CONTROLS
        paneColumn = QtWidgets.QVBoxLayout()
        paneColumn.addWidget(QtWidgets.QLabel("Pane"))
        # Tab switcher
        paneColumn.addWidget(self.PaneTabMenu(owner))
        # Toggle pane tabs
        panePaneTabsButton = QtWidgets.QPushButton("Pane Tabs")
        panePaneTabsButton.clicked.connect(owner.hctlPane.toggleTabs)
        paneColumn.addWidget(panePaneTabsButton)
        # Toggle network controls
        paneNetworkControlsButton = QtWidgets.QPushButton("Network Controls")
        paneNetworkControlsButton.clicked.connect(owner.hctlPaneTab.toggleNetworkControls)
        paneColumn.addWidget(paneNetworkControlsButton)
        # Pane expand
        paneExpandButton = QtWidgets.QPushButton("Expand")
        paneExpandButton.clicked.connect(owner.hctlPane.expand)
        paneColumn.addWidget(paneExpandButton)
        # Pane contract
        paneContractButton = QtWidgets.QPushButton("Contract")
        paneContractButton.clicked.connect(owner.hctlPane.contract)
        paneColumn.addWidget(paneContractButton)
        # Toggle maximized
        paneMaximizedButton = QtWidgets.QPushButton("Maximized")
        paneMaximizedButton.clicked.connect(owner.hctlPane.toggleMaximized)
        paneColumn.addWidget(paneMaximizedButton)
        # Fill empty space
        paneColumn.addStretch()

        # PANE TAB CONTROLS
        paneTabColumn = QtWidgets.QVBoxLayout()
        paneTabColumn.addWidget(QtWidgets.QLabel("Pane Tab"))
        # Pin tab
        paneTabColumn.addWidget(self.PinCheckBox(owner))
        # Tab type
        paneTabColumn.addWidget(self.PaneTabTypeMenu(owner))

        # NETWORK EDITOR
        if self.owner.hctlPaneTab.type() == hou.paneTabType.NetworkEditor:
            networkEditorMenuButton = QtWidgets.QPushButton("NE Menu")
            networkEditorMenuButton.clicked.connect(owner.hctlNetworkEditor.toggleMenu)
            paneTabColumn.addWidget(networkEditorMenuButton)

        # SCENE VIEWER
        if self.owner.hctlPaneTab.type() == hou.paneTabType.SceneViewer:
            keycamButton = QtWidgets.QPushButton("Keycam")
            keycamButton.clicked.connect(owner.hctlSceneViewer.keycam)
            paneTabColumn.addWidget(keycamButton)

        # Fill empty space
        paneTabColumn.addStretch()

        # Finish control columns
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(sessionColumn)
        layout.addLayout(paneColumn)
        layout.addLayout(paneTabColumn)

        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(1)
        self.setLayout(layout)
        self.setFixedWidth(600)



    class AutoSaveCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner):
            super().__init__("Autosave")
            state = owner.hctlSession.autosaveState()
            if state == "1":
                self.setCheckState(Qt.Checked)
            elif state == "0":
                self.setCheckState(Qt.Unchecked)
            self.clicked.connect(owner.hctlSession.toggleAutoSave)


    class PinCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner):
            super().__init__("Pin tab")
            self.owner = owner
            self.clicked.connect(self.togglePin)
            if owner.hctlPaneTab.isPin():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)

        def togglePin(self):
            self.owner.hctlPaneTab.togglePin()


    class PaneTabMenu(QtWidgets.QComboBox):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            self.addItems(owner.paneTab_labels)
            self.activated.connect(self.change)

        def change(self):
            index = self.tabMenu.currentIndex()
            paneTab = self.owner.hctlSession.tabs()[index]
            paneTab.setIsCurrentTab()


    class PaneTabTypeMenu(QtWidgets.QComboBox):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            self.addItems(owner.paneTab_type_names)
            # Get current context
            key = str(owner.hctlPaneTab.type())
            key = key.lstrip("paneTabType")
            key = key.lstrip(".")
            self.setCurrentIndex(owner.paneTab_type_names.index(key))
            self.activated.connect(self.change)

        def change(self):
            index = self.paneTabTypeMenu.currentIndex()
            self.paneTab = self.paneTab.setType(self.owner.paneTab_types[index])


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
                        self.setItemSelected(item, 1)
                    counter += 1



class MiddleColumn(QtWidgets.QVBoxLayout):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.topPanel = self.TopPanel(self)
        self.bottomPanel = self.BottomPanel(self)
        self.addWidget(self.topPanel)
        self.addWidget(self.bottomPanel)


    class TopPanel(QtWidgets.QFrame):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            # Main layout
            layout = QtWidgets.QGridLayout()
            # Project path label
            layout.addWidget(QtWidgets.QLabel("Project path:"), 0, 0)
            layout.addWidget(QtWidgets.QLabel(owner.owner.project_path), 0, 1)
            layout.setRowMinimumHeight(0, 20)
            # Network path label
            layout.addWidget(QtWidgets.QLabel("Network path:"), 1, 0)
            layout.addWidget(QtWidgets.QLabel(str(owner.owner.network_path) + "/" + str(owner.owner.node)), 1, 1)
            layout.setRowMinimumHeight(1, 20)
            # Formatting
            self.setFrameShape(QtWidgets.QFrame.Panel)
            self.setLineWidth(1)
            self.setLayout(layout)
            # self.setFixedHeight(180)
            self.setFixedWidth(300)



class RightPanel(QtWidgets.QFrame):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(1)
        # self.setLayout
        # self.setFixedHeight(180)
        self.setFixedWidth(300)
        desktop = self.owner.session.layout()
