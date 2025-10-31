import hou
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QSlider, QDialog, QLabel, QMenu, QHBoxLayout, QVBoxLayout
from .hcwidgets import HCButton
from ..core.hcsession import HCSession
from ..core.hcpane import HCPane


class HCPanel(QDialog):

    def __init__(self, hcPaneTab):
        super(HCPanel, self).__init__(hou.qt.mainWindow())

        ## OBJECTS
        self.hcSession = HCSession()
        self.hcPaneTab = hcPaneTab
        self.hcPane = HCPane(hcPaneTab.pane())

        ## WINDOW PARAMETERS
        pane_geo = self.hcPane.qtScreenGeometry()
        pane_center = pane_geo.center()
        x = pane_center.x() - 200
        y = pane_center.y() - 75
        self.resize(400, 200)
        self.move(x, y)
        self.setWindowTitle("hctl panel")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint )

        ## UTILITY LISTS
        self.pane_tab_types = (hou.paneTabType.ApexEditor, hou.paneTabType.CompositorViewer, hou.paneTabType.DetailsView, hou.paneTabType.NetworkEditor, hou.paneTabType.Parm, hou.paneTabType.PythonPanel, hou.paneTabType.PythonShell, hou.paneTabType.SceneViewer, hou.paneTabType.Textport)
        self.pane_tab_names = [paneTab.name() for paneTab in self.hcSession.paneTabs()]
        self.pane_tab_type_names = ("ApexEditor", "CompositorViewer", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport")
        self.pane_tab_labels = []
        for paneTab in self.hcSession.paneTabs():
            index = self.pane_tab_types.index(paneTab.type())
            label = self.pane_tab_type_names[index]
            self.pane_tab_labels.append(label)

        ## PATHS
        self.projectpath = hou.hipFile.name()
        ct = self.projectpath.count("/")
        self.projectpath = self.projectpath.split("/", ct - 2)[-1]
        self.networkpath = self.hcPaneTab.pwd()

        ## SESSION COLUMN
        sessionCol = QVBoxLayout()
        # Label
        sessionLabel = QLabel("Session")
        sessionLabel.setStyleSheet("color: #909090")
        sessionCol.addWidget(sessionLabel)
        # Toggle autosave
        sessionCol.addWidget(self.SessionAutosaveCheckBox(self))
        # Toggle menus
        sessionMenusBtn = HCButton("Menus")
        sessionMenusBtn.clicked.connect(self.hcSession.toggleMenus)
        sessionCol.addWidget(sessionMenusBtn)
        # Toggle tabs
        sessionTabsBtn = HCButton("Tabs")
        sessionTabsBtn.clicked.connect(self.hcSession.toggleTabs)
        sessionCol.addWidget(sessionTabsBtn)
        # Toggle network controls
        sessionNetworkControlsBtn = HCButton("Network Controls")
        sessionNetworkControlsBtn.clicked.connect(self.hcSession.toggleNetworkControls)
        sessionCol.addWidget(sessionNetworkControlsBtn)
        # Toggle stowbars
        sessionStowbarsBtn = HCButton("Stowbars")
        sessionStowbarsBtn.clicked.connect(self.hcSession.toggleStowbars)
        sessionCol.addWidget(sessionStowbarsBtn)
        # Fill empty space
        sessionCol.addStretch()

        ## PANE COLUMN
        paneCol = QVBoxLayout()
        # Label
        paneLabel = QLabel("Pane")
        paneLabel.setStyleSheet("color: #909090")
        paneCol.addWidget(paneLabel)
        # Toggle maximize
        paneMaximizeBtn = HCButton("Maximize")
        paneMaximizeBtn.clicked.connect(self.hcPane.toggleMaximized)
        paneCol.addWidget(paneMaximizeBtn)
        # Expand
        # paneExpandBtn = HCButton("Expand")
        # paneExpandBtn.clicked.connect(self.hcPane.expand)
        # paneCol.addWidget(paneExpandBtn)
        # Contract
        # paneContractBtn = HCButton("Contract")
        # paneContractBtn.clicked.connect(self.hcPane.contract)
        # paneCol.addWidget(paneContractBtn)
        # Toggle tabs
        panePaneTabsBtn = HCButton("Tabs")
        panePaneTabsBtn.clicked.connect(self.hcPane.togglePaneTabs)
        paneCol.addWidget(panePaneTabsBtn)
        # Size slider
        sizeSlider= QSlider(Qt.Horizontal)
        sizeSlider.setFixedWidth(400/3)
        sizeSlider.setValue(self.hcPane.splitFraction()*100)
        sizeSlider.valueChanged.connect(self.sliderChange)
        paneCol.addWidget(sizeSlider)
        # Fill empty space
        paneCol.addStretch()

        ## PANE TAB COLUMN
        paneTabCol = QVBoxLayout()
        # Label
        paneTabLabel = QLabel("Tab")
        paneTabLabel.setStyleSheet("color: #909090")
        paneTabCol.addWidget(paneTabLabel)
        # Toggle pin
        paneTabCol.addWidget(self.PaneTabPinCheckBox(self))
        # Switch
        paneTabCol.addWidget(self.PaneTabMenu(self))
        # Change type
        # paneTabCol.addWidget(self.PaneTabTypeMenu(self))
        # Toggle network controls
        paneTabNetworkControlsBtn = HCButton("Network Controls")
        paneTabNetworkControlsBtn.clicked.connect(self.hcPaneTab.toggleNetworkControls)
        paneTabCol.addWidget(paneTabNetworkControlsBtn)
        # Scene viewer controls
        if self.hcPaneTab.type() == hou.paneTabType.SceneViewer:
            # Toggle keycam
            paneTabKeycamBtn = HCButton("Keycam")
            paneTabKeycamBtn.clicked.connect(self.hcSession.keycam)
            paneTabCol.addWidget(paneTabKeycamBtn)
            # Home all viewports
            paneTabHomeBtn = HCButton("Home")
            paneTabHomeBtn.clicked.connect(self.hcPaneTab.homeAllViewports)
            paneTabCol.addWidget(paneTabHomeBtn)
        # Fill empty space
        paneTabCol.addStretch()

        ## LAYOUT
        self.layout = QHBoxLayout()
        self.layout.addLayout(sessionCol)
        self.layout.addLayout(paneCol)
        self.layout.addLayout(paneTabCol)
        self.setLayout(self.layout)


    def sliderChange(self, value):
        self.hcPane.setSplitFraction(value/100)


    def closeEvent(self, event):
        self.setParent(None)



    class SessionAutosaveCheckBox(QCheckBox):

        def __init__(self, owner):
            super().__init__("Autosave")
            state = owner.hcSession.autosave()
            if state == "1":
                self.setCheckState(Qt.Checked)
            elif state == "0":
                self.setCheckState(Qt.Unchecked)
            self.clicked.connect(owner.hcSession.toggleAutoSave)



    class PaneTabPinCheckBox(QCheckBox):

        def __init__(self, owner):
            super().__init__("Pin")
            self.owner = owner
            self.clicked.connect(self.owner.hcPaneTab.togglePin)
            if self.owner.hcPaneTab.isPin():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)



    class PaneTabMenu(HCButton):

        def __init__(self, owner):
            super().__init__(str(owner.hcPane.currentTab().type()).split(".")[-1])
            self.owner = owner
            self.tabs = self.owner.hcPane.tabs()
            self.tabNames = [str(tab.type()).split(".")[-1] for tab in self.tabs]
            self.menu = QMenu(self)
            idx = 0
            for tabName in self.tabNames:
                action = self.menu.addAction(tabName)
                action.triggered.connect(lambda checked=False, index=idx: self.changeTab(index))
                idx += 1
            self.setMenu(self.menu)

        def changeTab(self, index):
            newTab = self.tabs[index]
            newTab.setIsCurrentTab()
            self.owner.close()



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
