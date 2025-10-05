import hou
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QVBoxLayout, QLabel, QMenu, QDialog, QHBoxLayout
from .widgets import HctlButton
from .core.hcsession import HctlSession


class Dialog(QDialog):
    def __init__(self, hctlPaneTab):
        super(Dialog, self).__init__(hou.qt.mainWindow())
        self.resize(400, 150)
        self.setWindowTitle("hctl")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint )
        self.hctlPaneTab = hctlPaneTab
        self.hctlSession = HctlSession()
        self.update()


    def change(self):
        self.setText(self.sender().text())
        index = self.tabMenu.currentIndex()
        tab = self.session.tabs()[index]
        tab.setIsCurrentTab()


    def closeEvent(self, event):
        self.setParent(None)


    def lists(self):
        # TYPE/NAME ARRAYS
        self.paneTab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
        self.paneTab_names = [paneTab.name() for paneTab in self.hctlSession.paneTabs()]
        self.paneTab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
        # Populate pane tab labels array
        self.paneTab_labels = []
        for paneTab in self.hctlSession.tabs():
            index = self.paneTab_types.index(paneTab.type())
            label = self.paneTab_type_names[index]
            self.paneTab_labels.append(label)


    def paths(self):
        # Project path
        self.project_path = hou.hipFile.name()
        ct = self.project_path.count("/")
        self.project_path = self.project_path.split("/", ct - 2)[-1]
        # Network path
        self.network_path = self.hctlPaneTab.pwd()


    def update(self):
        self.lists()
        # Layout
        self.layout = QHBoxLayout()
        self.controls = self.Controls(self)
        self.layout.addLayout(self.controls)
        self.paneControls = PaneControls(self)
        self.layout.addLayout(self.paneControls)
        self.tabControls = TabControls(self)
        self.layout.addLayout(self.tabControls)
        self.setLayout(self.layout)


    def sessionToggleAutosave():
        hou.session.hctlSession.toggleAutoSave()
    def sessionToggleMenus():
        hou.session.hctlSession.toggleMenus()


    def paneToggleMaximized():
        hou.session.hctlPane.toggleMaximized()
    def paneExpand():
        hou.session.hctlPane.expand()
    def paneContract():
        hou.session.hctlPane.contract()
    def paneToggleTabs():
        hou.session.hctlPane.toggleTabs()


    # CONTROL COLUMNS

    class SessionControls(QVBoxLayout):
        def __init__(self, owner):
            super().__init__()
            # LABEL
            sessionLabel = QLabel("Session")
            sessionLabel.setStyleSheet("color: #909090")
            self.addWidget(sessionLabel)
            # AUTOSAVE
            self.addWidget(self.AutosaveCheckBox(owner))
            # TOGGLE ALL MENUS
            sessionMenusButton = HctlButton("Menus")
            sessionMenusButton.clicked.connect(owner.session.toggleMenus)
            self.addWidget(sessionMenusButton)
            # TAB VISIBILITY
            sessionTabsButton = HctlButton("Tabs")
            sessionTabsButton.clicked.connect(owner.session.toggleTabs)
            self.addWidget(sessionTabsButton)
            # TOGGLE ALL NETWORK CONTROLS
            sessionNetworkControlsButton = HctlButton("Network Controls")
            sessionNetworkControlsButton.clicked.connect(owner.session.toggleNetworkControls)
            self.addWidget(sessionNetworkControlsButton)
            # STOWBAR VISIBILITY
            sessionStowbarsButton = HctlButton("Stowbars")
            sessionStowbarsButton.clicked.connect(owner.session.toggleStowbars)
            self.addWidget(sessionStowbarsButton)
            # Fill empty space
            self.addStretch()


    class PaneControls(QVBoxLayout):
        def __init__(self, owner):
            super().__init__()

            # LABEL
            paneLabel = QLabel("Pane")
            paneLabel.setStyleSheet("color: #909090")
            self.addWidget(paneLabel)
            # TAB SWITCHER
            # tabMenu = self.TabMenu(owner, "menu")
            # self.addWidget(tabMenu)
            # MAXIMIZE TOGGLE
            paneMaximizeBtn = HctlButton("Maximize")
            paneMaximizeBtn.clicked.connect(owner.hctlPane.toggleMaximize)
            self.addWidget(paneMaximizeBtn)
            # EXPAND
            paneExpandBtn = HctlButton("Expand")
            paneExpandBtn.clicked.connect(owner.hctlPane.expand)
            self.addWidget(paneExpandBtn)
            # CONTRACT
            paneContractBtn = HctlButton("Contract")
            paneContractBtn.clicked.connect(owner.hctlPane.contract)
            self.addWidget(paneContractBtn)
            # TOGGLE TABS
            panePaneTabsBtn = HctlButton("Tabs")
            panePaneTabsBtn.clicked.connect(owner.hctlPane.togglePaneTabs)
            self.addWidget(panePaneTabsBtn)
            # FILL EMPTY SPACE
            self.addStretch()


    class AutosaveCheckBox(QCheckBox):
        def __init__(self, owner):
            super().__init__("Autosave")
            state = owner.hctlSession.autosave()
            if state == "1":
                self.setCheckState(Qt.Checked)
            elif state == "0":
                self.setCheckState(Qt.Unchecked)
            self.clicked.connect(owner.session.toggleAutosave)


    class PinCheckBox(QCheckBox):
        def __init__(self, owner):
            super().__init__("Pin")
            self.owner = owner
            self.clicked.connect(self.owner.tab.togglePin)
            if self.owner.tab.isPin():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)



    class TabControls(QVBoxLayout):
        def __init__(self, owner):
            super().__init__()
            self.owner = owner
            # LABEL
            label = QLabel("Tab")
            label.setStyleSheet("color: #909090")
            self.addWidget(label)
            # PIN
            self.addWidget(self.PinCheckBox(owner))
            # TAB TYPE MENU
            self.addWidget(self.TabTypeMenu(owner))
            # NETWORK CONTROLS
            tabNetworkControlsButton = HctlButton("Network Controls")
            tabNetworkControlsButton.clicked.connect(owner.hcTab.toggleNetworkControls)
            self.addWidget(tabNetworkControlsButton)
            # SCENE VIEWER CONTROLS
            if owner.paneTab.type() == hou.paneTabType.SceneViewer:
                paneTabKeycamButton = HctlButton("Keycam")
                paneTabKeycamButton.clicked.connect(owner.hctlSession.keycam)
                self.addWidget(paneTabKeycamButton)
            # FILL EMPTY SPACE
            self.addStretch()



    class PaneTabMenu(HctlButton):
        def __init__(self, owner, text):
            super().__init__(text)
            menu = QMenu(self)
            for label in owner.tab_labels:
                action = menu.addAction(label)
                action.triggered.connect(self.change)
            self.setMenu(menu)



    class TabTypeMenu(HctlButton):
        def __init__(self, owner):
            super().__init__("menu")
            self.owner = owner
            menu = QMenu(self)
            for label in owner.tab_type_names:
                menu.addAction(label)
            menu.triggered.connect(self.on_action_triggered)
            self.setMenu(menu)


        def on_action_triggered(self, action):
            self.setText(action.text())
            # index = self.owner.tab_type_names.index(action.text())
            # tab_type = self.owner.tab_types[index]
            # tab = self.owner.hctlTab.setType(tab_type)
            # self.owner.hctlTab = hcu.HctlTab(tab)
