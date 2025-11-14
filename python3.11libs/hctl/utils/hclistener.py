import hou
# from importlib import reload
from ..core.hcglobal import HCGlobal
from ..core.hcpane import HCPane
from ..core.hctab import HCTab
# from .core.hcviewport import HCViewport


class HCListener():
    def __init__(self):
        self.report_tab = 1
        hou.session.tab = None
        hou.session.pane = None
        hou.session.hc_global = None
        hou.session.hc_pane = None
        hou.session.hc_tab = None
        hou.session.hc_sceneviewer = None
        hou.session.hc_networkeditor = None
        hou.session.project_path = hou.hipFile.path()
        hou.session.network_path = None
        hou.session.tab_type = None
        self.update_objects()
        return

    def start(self):
        hou.ui.addEventLoopCallback(self.listener)

    def stop(self):
        hou.ui.removeEventLoopCallback(self.listener)

    def update_objects(self):
        hou.session.tab = hou.ui.paneTabUnderCursor()
        hou.session.pane = hou.ui.paneUnderCursor()

        hou.session.hc_global = HCGlobal()
        hou.session.hc_pane = HCPane(hou.ui.paneUnderCursor())
        hou.session.hc_tab = HCTab(hou.session.tab)

        if hou.session.hc_tab != None:

            if hou.session.hc_tab.hasNetworkControls():
                hou.session.network_path = hou.session.hc_tab.path()
            hou.session.tab_type = hou.session.hc_tab.type()

            if hou.session.tab.type() == hou.paneTabType.SceneViewer:
                hou.session.sceneviewer = HCSceneViewer(hou.session.tab)
            else: hou.session.sceneviewer = None

            if hou.session.tab.type() == hou.paneTabType.NetworkEditor:
                hou.session.networkeditor = HctlNetworkEditor(hou.session.tab)
            else: hou.session.networkeditor = None

        # Labels
        # self.project_path_label.setText("Project path: " + self.projectPath())
        # if hou.session.tab.hasNetworkControls():
            # self.network_path_label.setText("Network Path: " + self.networkPath())
        # else: self.network_path_label.setText("No Network Path")
        # self.tab_type_label.setText("Tab type: " + str(hou.session.hc_tab.type()))

    def listener(self):
        tab = hou.ui.paneTabUnderCursor()
        if tab == None:
            hou.session.tab = None
        elif tab != hou.session.tab:
            print(tab)
            self.update_objects()

    def lists(self):
        # Arrays for navigating pane tabs
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
        self.tab_names = [tab.name() for tab in hou.session.hc_global.tabs()]

        # Populate pane tab labels array
        self.tab_labels = []
        for tab in self.hc_global.tabs():
            index = self.tab_types.index(tab.type())
            label = self.tab_type_names[index]
            self.tab_labels.append(label)

    def networkPath(self):
        return str(hou.session.tab.pwd())

    def projectPath(self):
        return hou.hipFile.name()
        # ct = self.project_path.count("/")
        # self.project_path = self.project_path.split("/", ct - 2)[-1]
