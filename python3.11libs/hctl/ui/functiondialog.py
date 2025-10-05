import hou, inspect, platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from fuzzyfinder import fuzzyfinder
import hctl_utils as hcu
from importlib import reload


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__( hou.qt.mainWindow() )
        self.resize(900, 400)
        self.setWindowTitle("hctl")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        self.update()

        # Focus the input line AFTER setting window flags
        self.functionPanel.inputLine.setFocus()


    def closeEvent(self, event):
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
        # Control columns
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
        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(1)
        self.setLayout(layout)
        self.setFixedWidth(600)
        self.owner = owner

        # Control columns
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self.SessionControls(self))
        layout.addLayout(self.PaneControls(self))
        layout.addLayout(self.TabControls(self))



class SessionControls(QtWidgets.QVBoxLayout):
    def __init__(self, owner):
        super().__init__()

        # Label
        self.addWidget(QtWidgets.QLabel("Session"))

        # Separator
        sep0 = QtWidgets.QFrame()
        sep0.setFrameShape(QtWidgets.QFrame.HLine)
        self.addWidget(sep0)

        # Autosave
        self.addWidget(self.AutoSaveCheckBox(owner))

        # Toggle all menus
        menusButton = QtWidgets.QPushButton("Menus")
        menusButton.clicked.connect(owner.hctlSession.toggleMenus)
        menusButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        menusButton.setFlat(1)
        self.addWidget(menusButton)

        # Panetab visibility
        paneTabsButton = QtWidgets.QPushButton("Pane Tabs")
        paneTabsButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        paneTabsButton.clicked.connect(owner.hctlSession.togglePaneTabs)
        paneTabsButton.setFlat(1)
        self.addWidget(paneTabsButton)

        # Toggle all network controls
        networkControlsButton = QtWidgets.QPushButton("Network Controls")
        networkControlsButton.clicked.connect(owner.hctlSession.toggleNetworkControls)
        networkControlsButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        networkControlsButton.setFlat(1)
        self.addWidget(networkControlsButton)

        # Stowbar visibility
        stowbarsButton = QtWidgets.QPushButton("Stowbars")
        stowbarsButton.clicked.connect(owner.hctlSession.toggleStowbars)
        stowbarsButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        stowbarsButton.setFlat(1)
        self.addWidget(stowbarsButton)

        # Reload color schems
        reloadColorsButton = QtWidgets.QPushButton("Reload colors")
        reloadColorsButton.clicked.connect(owner.hctlSession.reloadColorSchemes)
        reloadColorsButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        reloadColorsButton.setFlat(1)
        self.addWidget(reloadColorsButton)

        # Fill empty space
        self.addStretch()


    class AutoSaveCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner):
            super().__init__("Autosave")

            state = owner.hctlSession.autosaveState()
            if state == "1":
                self.setCheckState(Qt.Checked)
            elif state == "0":
                self.setCheckState(Qt.Unchecked)

            self.clicked.connect(owner.hctlSession.toggleAutoSave)



class PaneControls(QtWidgets.QVBoxLayout):
    def __init__(self, owner):
        super().__init__()

        # Label
        self.addWidget(QtWidgets.QLabel("Pane"))

        # Separator
        sep0 = QtWidgets.QFrame()
        sep0.setFrameShape(QtWidgets.QFrame.HLine)
        self.addWidget(sep0)

        # Tab switcher
        self.addWidget(self.PaneTabMenu(owner))

        # Maximize
        maximizeButton = QtWidgets.QPushButton("Maximize")
        maximizeButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        maximizeButton.clicked.connect(owner.hctlPane.toggleMaximized)
        maximizeButton.setFlat(1)
        self.addWidget(maximizeButton)

        # Expand
        expandButton = QtWidgets.QPushButton("Expand")
        expandButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        expandButton.clicked.connect(owner.hctlPane.expand)
        expandButton.setFlat(1)
        self.addWidget(expandButton)

        # Contract
        contractButton = QtWidgets.QPushButton("Contract")
        contractButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        contractButton.clicked.connect(owner.hctlPane.contract)
        contractButton.setFlat(1)
        self.addWidget(contractButton)

        # Toggle pane tabs
        paneTabsButton = QtWidgets.QPushButton("Pane Tabs")
        paneTabsButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        paneTabsButton.clicked.connect(owner.hctlPane.toggleTabs)
        paneTabsButton.setFlat(1)
        self.addWidget(paneTabsButton)

        # Fill empty space
        self.addStretch()

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


class TabControls(QtWidgets.QVBoxLayout):
    def __init__(self, owner):
        super().__init__()
        self.owner = owner

        self.addWidget(QtWidgets.QLabel("Tab"))

        # Separator
        sep0 = QtWidgets.QFrame()
        sep0.setFrameShape(QtWidgets.QFrame.HLine)
        self.addWidget(sep0)

        # Pin
        self.addWidget(self.PinCheckBox(owner))

        # Tab type menu
        self.addWidget(self.TabTypeMenu(owner))

        # Network controls
        networkControlsButton = QtWidgets.QPushButton("Network Controls")
        networkControlsButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
        networkControlsButton.clicked.connect(owner.hctlPaneTab.toggleNetworkControls)
        networkControlsButton.setFlat(1)
        self.addWidget(networkControlsButton)

        # Conditionals
        if self.owner.hctlPaneTab.type() == hou.paneTabType.SceneViewer:
            keycamButton = QtWidgets.QPushButton("Keycam")
            keycamButton.setStyleSheet("text-align: left; padding: 2 2 2 10")
            keycamButton.clicked.connect(owner.hctlSceneViewer.keycam)
            self.addWidget(keycamButton)

        # Fill empty space
        self.addStretch()


    class PinCheckBox(QtWidgets.QCheckBox):
        def __init__(self, owner):
            super().__init__("Pin")
            self.owner = owner
            self.clicked.connect(self.togglePin)

            if owner.hctlPaneTab.isPin():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)

        def togglePin(self):
            self.owner.hctlPaneTab.togglePin()


    class TabTypeMenu(QtWidgets.QComboBox):
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
                        self.setCurrentItem(item)
                    counter += 1
