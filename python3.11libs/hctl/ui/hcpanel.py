import hou
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QCheckBox, QVBoxLayout, QLabel, QMenu, QDialog, QHBoxLayout
from .hcwidgets import HCButton
from hctl.core.hcsession import HCSession
from hctl.core.hcpane import HCPane


class HCPanel(QDialog):

    def __init__(self, hCPaneTab):
        super(HCPanel, self).__init__(hou.qt.mainWindow())

        ## OBJECTS
        self.hCSession = HCSession()
        self.hCPaneTab = hCPaneTab
        self.hCPane = HCPane(hCPaneTab.pane())

        ## WINDOW PARAMETERS
        pane_geo = self.hCPane.qtScreenGeometry()
        pane_center = pane_geo.center()
        x = pane_center.x() - 200
        y = pane_center.y() - 75
        self.resize(400, 150)
        self.move(x, y)
        # self.moveCenter(pane_geo.center)
        self.setWindowTitle("hctl panel")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint )

        ## UTILITY LISTS
        self.pane_tab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
        self.pane_tab_names = [paneTab.name() for paneTab in self.hCSession.paneTabs()]
        self.pane_tab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
        self.pane_tab_labels = []
        for paneTab in self.hCSession.paneTabs():
            index = self.pane_tab_types.index(paneTab.type())
            label = self.pane_tab_type_names[index]
            self.pane_tab_labels.append(label)

        ## PATHS
        self.projectpath = hou.hipFile.name()
        ct = self.projectpath.count("/")
        self.projectpath = self.projectpath.split("/", ct - 2)[-1]
        self.networkpath = self.hCPaneTab.pwd()

        ## SESSION COLUMN
        sessionCol = QVBoxLayout()
        # Session label
        sessionLabel = QLabel("Session")
        sessionLabel.setStyleSheet("color: #909090")
        sessionCol.addWidget(sessionLabel)
        # Session autosave widget
        sessionCol.addWidget(self.SessionAutosaveCheckBox(self))
        # Session toggle menus
        sessionMenusBtn = HCButton("Menus")
        sessionMenusBtn.clicked.connect(self.hCSession.toggleMenus)
        sessionCol.addWidget(sessionMenusBtn)
        # Session tab visibility
        sessionTabsBtn = HCButton("Tabs")
        sessionTabsBtn.clicked.connect(self.hCSession.toggleTabs)
        sessionCol.addWidget(sessionTabsBtn)
        # Session toggle network controls
        sessionNetworkControlsBtn = HCButton("Network Controls")
        sessionNetworkControlsBtn.clicked.connect(self.hCSession.toggleNetworkControls)
        sessionCol.addWidget(sessionNetworkControlsBtn)
        # Session stowbars
        sessionStowbarsBtn = HCButton("Stowbars")
        sessionStowbarsBtn.clicked.connect(self.hCSession.toggleStowbars)
        sessionCol.addWidget(sessionStowbarsBtn)
        # Fill empty space
        sessionCol.addStretch()

        ## PANE COLUMN
        paneCol = QVBoxLayout()
        # Pane label
        paneLabel = QLabel("Pane")
        paneLabel.setStyleSheet("color: #909090")
        paneCol.addWidget(paneLabel)
        # Pane maximize
        paneMaximizeBtn = HCButton("Maximize")
        paneMaximizeBtn.clicked.connect(self.hCPane.toggleMaximized)
        paneCol.addWidget(paneMaximizeBtn)
        # Pane expand
        paneExpandBtn = HCButton("Expand")
        paneExpandBtn.clicked.connect(self.hCPane.expand)
        paneCol.addWidget(paneExpandBtn)
        # Pane contract
        paneContractBtn = HCButton("Contract")
        paneContractBtn.clicked.connect(self.hCPane.contract)
        paneCol.addWidget(paneContractBtn)
        # Pane toggle tabs
        panePaneTabsBtn = HCButton("Tabs")
        panePaneTabsBtn.clicked.connect(self.hCPane.togglePaneTabs)
        paneCol.addWidget(panePaneTabsBtn)
        # Fill empty space
        paneCol.addStretch()

        ## PANE TAB COLUMN
        paneTabCol = QVBoxLayout()
        # Pane tab label
        paneTabLabel = QLabel("Tab")
        paneTabLabel.setStyleSheet("color: #909090")
        paneTabCol.addWidget(paneTabLabel)
        # Pane tab pin
        paneTabCol.addWidget(self.PaneTabPinCheckBox(self))
        # Pane tab menu
        paneTabCol.addWidget(self.PaneTabMenu(self))
        # Pane tab type menu
        paneTabCol.addWidget(self.PaneTabTypeMenu(self))
        # Pane tab network controls
        paneTabNetworkControlsBtn = HCButton("Network Controls")
        paneTabNetworkControlsBtn.clicked.connect(self.hCPaneTab.toggleNetworkControls)
        paneTabCol.addWidget(paneTabNetworkControlsBtn)
        # Pane tab scene viewer controls
        if self.hCPaneTab.type() == hou.paneTabType.SceneViewer:
            paneTabKeycamBtn = HCButton("Keycam")
            paneTabKeycamBtn.clicked.connect(self.hCSession.keycam)
            paneTabCol.addWidget(paneTabKeycamBtn)
        # Fill empty space
        paneTabCol.addStretch()

        ## LAYOUT
        self.layout = QHBoxLayout()
        self.layout.addLayout(sessionCol)
        self.layout.addLayout(paneCol)
        self.layout.addLayout(paneTabCol)
        self.setLayout(self.layout)


    def closeEvent(self, event):
        self.setParent(None)



    class SessionAutosaveCheckBox(QCheckBox):

        def __init__(self, owner):
            super().__init__("Autosave")
            state = owner.hCSession.autosave()
            if state == "1":
                self.setCheckState(Qt.Checked)
            elif state == "0":
                self.setCheckState(Qt.Unchecked)
            self.clicked.connect(owner.hCSession.toggleAutoSave)



    class PaneTabPinCheckBox(QCheckBox):

        def __init__(self, owner):
            super().__init__("Pin")
            self.owner = owner
            self.clicked.connect(self.owner.hCPaneTab.togglePin)
            if self.owner.hCPaneTab.isPin():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)



    class PaneTabMenu(HCButton):

        def __init__(self, owner):
            super().__init__("k")
            self.owner = owner
            self.paneTabs = self.owner.hCPane.paneTabs()
            self.paneTabNames = [str(paneTab) for paneTab in self.paneTabs]
            self.actions = []
            self.menu = QMenu(self)
            for paneTabName in self.paneTabNames:
                action = self.menu.addAction(paneTabName)
                action.triggered.connect(self.changeTab)
                self.actions.append(action)
            self.setMenu(self.menu)


        def changeTab(self):
            print(action)
            return
            # self.setText(self.sender().text())
            # index = self.actions.index(QAction)
            # print(index)
            # print(self.paneTabNames)
            # print(self.menu.activeAction())
            # return
            # index = self.paneTabNames.index(self.menu.activeAction())
            # newPaneTab = self.paneTab[index]
            # newPaneTab.setIsCurrentTab()



    class PaneTabTypeMenu(HCButton):

        def __init__(self, owner):
            super().__init__("menu")
            self.owner = owner
            menu = QMenu(self)
            for label in owner.pane_tab_type_names:
                menu.addAction(label)
            menu.triggered.connect(self.on_action_triggered)
            self.setMenu(menu)


        def on_action_triggered(self, action):
            self.setText(action.text())
            # index = self.owner.tab_type_names.index(action.text())
            # tab_type = self.owner.tab_types[index]
            # tab = self.owner.hctlTab.setType(tab_type)
            # self.owner.hctlTab = hcu.HctlTab(tab)
