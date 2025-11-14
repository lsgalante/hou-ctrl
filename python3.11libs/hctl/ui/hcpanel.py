import hou
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMenu,
    QSlider,
    QVBoxLayout,
)

from ..core.hcglobal import HCGlobal
from ..core.hcpane import HCPane
from .hcwidgets import HCButton


class HCPanel(QDialog):
    def __init__(self, hc_tab):
        super(HCPanel, self).__init__(hou.qt.mainWindow())

        # Objects
        self.hc_global= HCSession()
        self.hc_tab = hc_tab
        self.hc_pane = HCPane(hc_pane.pane())

        # Window parameters
        pane_geo = self.hcPane.qtScreenGeometry()
        pane_center = pane_geo.center()
        x = pane_center.x() - 200
        y = pane_center.y() - 75
        self.resize(200, 100)
        self.move(x, y)
        self.setWindowTitle("hctl panel")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        # Utility lists
        self.tab_types = (
            hou.paneTabType.ApexEditor,
            hou.paneTabType.ChannelEditor,
            hou.paneTabType.ChannelViewer,
            hou.paneTabType.CompositorViewer,
            hou.paneTabType.DetailsView,
            hou.paneTabType.IPRViewer,
            hou.paneTabType.NetworkEditor,
            hou.paneTabType.Parm,
            hou.paneTabType.PythonPanel,
            hou.paneTabType.PythonShell,
            hou.paneTabType.SceneViewer,
            hou.paneTabType.Textport,
            hou.paneTabType.TreeView,
        )
        self.tab_names = [tab.name() for tab in self.hc_global.tabs()]
        self.tab_type_names = (
            "ApexEditor",
            "Channel Editor",
            "Channel Viewer",
            "CompositorViewer",
            "DetailsView",
            "IPR Viewer",
            "NetworkEditor",
            "Parm",
            "PythonPanel",
            "PythonShell",
            "SceneViewer",
            "Textport",
            "Tree View",
        )
        self.tab_labels = []
        for tab in self.hc_global.tabs():
            index = self.tab_types.index(tab.type())
            label = self.tab_type_names[index]
            self.tab_labels.append(label)

        # Paths
        self.project_path = hou.hipFile.name()
        ct = self.project_path.count("/")
        self.project_path = self.project_path.split("/", ct - 2)[-1]
        self.network_path = self.hc_tab.pwd()

        # Global column
        global_col = QVBoxLayout()
        # Label
        global_label = QLabel("Global")
        global_label.setStyleSheet("color: #909090")
        global_col.addWidget(global_label)
        # Toggle tabs
        global_tabs_btn = HCButton("Tabs")
        global_tabs_btn.clicked.connect(self.hc_global.toggleTabs)
        global_col.addWidget(global_tabs_btn)
        # Toggle network controls
        global_network_controls_btn = HCButton("Network Controls")
        global_network_controls_btn.clicked.connect(self.hc_global.toggleNetworkControls)
        global_col.addWidget(global_network_controls_btn)
        # Toggle autosave
        global_col.addWidget(self.SessionAutosaveCheckBox(self))
        # Toggle menus
        global_menus_btn = HCButton("Menus")
        global_menus_btn.clicked.connect(self.hc_global.toggleMenus)
        global_col.addWidget(global_menus_btn)
        # Toggle stowbars
        global_stowbars_btn = HCButton("Stowbars")
        global_stowbars_btn.clicked.connect(self.hc_global.toggleStowbars)
        global_col.addWidget(global_stowbars_btn)
        # Fill empty space
        global_col.addStretch()

        # Context column
        context_col = QVBoxLayout()
        # Label
        context_label = QLabel("Context")
        context_label.setStyleSheet("color: #909090")
        context_col.addWidget(context_label)
        # Toggle tabs
        context_tabs_btn = HCButton("Tabs")
        context_tabs_btn.clicked.connect(self.hc_pane.toggleTabs)
        context_col.addWidget(context_tabs_btn)
        # Toggle network controls
        context_network_controls_btn = HCButton("Network Controls")
        context_network_controls_btn.clicked.connect(self.hc_tab.toggleNetworkControls)
        context_col.addWidget(context_network_controls_btn)
        # Toggle pin
        context_col.addWidget(self.TabPinCheckBox(self))
        # Tab switcher
        context_col.addWidget(self.TabMenu(self))
        # Tab type switcher
        # context_col.addWidget(self.TabTypeMenu(self))
        # Toggle maximize
        context_maximize_btn = HCButton("Maximize")
        context_maximize_btn.clicked.connect(self.hc_pane.toggleMaximized)
        context_col.addWidget(context_maximize_btn)
        # Size slider
        context_size_slider = QSlider(Qt.Horizontal)
        context_size_slider.setFixedWidth(300 / 2)
        context_size_slider.setValue(self.hc_pane.splitFraction() * 100)
        context_size_slider.valueChanged.connect(self.sliderChange)
        context_col.addWidget(context_size_slider)

        # Scene viewer controls
        if self.hc_tab.type() == hou.paneTabType.SceneViewer:
            # Toggle keycam
            context_keycam_btn = HCButton("Keycam")
            context_keycam_btn.clicked.connect(self.hc_tab.keycam)
            context_col.addWidget(context_keycam_btn)
            # Home all viewports
            context_home_btn = HCButton("Home")
            context_home_btn.clicked.connect(self.hc_tab.homeAllViewports)
            context_col.addWidget(context_home_btn)

        # Fill empty space
        context_col.addStretch()

        # LAYOUT
        self.layout = QHBoxLayout()
        self.layout.addLayout(global_col)
        self.layout.addLayout(global_col)
        self.setLayout(self.layout)

    def sliderChange(self, value):
        self.hc_pane.setSplitFraction(value / 100)

    def closeEvent(self, event):
        self.setParent(None)

    class GlobalAutosaveCheckBox(QCheckBox):
        def __init__(self, owner):
            super().__init__("Autosave")
            state = owner.hc_global.autosave()
            if state == "1":
                self.setCheckState(Qt.Checked)
            elif state == "0":
                self.setCheckState(Qt.Unchecked)
            self.clicked.connect(owner.hc_global.toggleAutoSave)

    class TabPinCheckBox(QCheckBox):
        def __init__(self, owner):
            super().__init__("Pin")
            self.owner = owner
            self.clicked.connect(self.owner.hc_tab.togglePin)
            if self.owner.hc_tab.isPin():
                self.setCheckState(Qt.Checked)
            else:
                self.setCheckState(Qt.Unchecked)

    class TabMenu(HCButton):
        def __init__(self, owner):
            super().__init__(str(owner.hc_pane.currentTab().type()).split(".")[-1])
            self.owner = owner
            self.tabs = self.owner.hc_pane.tabs()
            self.tab_names = [str(tab.type()).split(".")[-1] for tab in self.tabs]
            self.menu = QMenu(self)
            idx = 0
            for tab_name in self.tab_names:
                action = self.menu.addAction(tab_name)
                action.triggered.connect(
                    lambda checked=False, index=idx: self.changeTab(index)
                )
                idx += 1
            self.setMenu(self.menu)

        def changeTab(self, index):
            new_tab = self.tabs[index]
            new_tab.setIsCurrentTab()
            self.owner.close()

    class TabTypeMenu(HCButton):
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
