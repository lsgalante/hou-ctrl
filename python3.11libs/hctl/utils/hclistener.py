import hou
# from importlib import reload
from hctl.core.hcpane           import HCPane
from hctl.core.hcsession        import HCSession
from hctl.core.hcpanetab            import HCPaneTab
# from hctl.core.hcviewport       import HCViewport


class HCListener():
    def __init__(self):
        self.report_tab = 1

        hou.session.tab = None
        hou.session.pane = None
        hou.session.hctlSession = None
        hou.session.hctlPane = None
        hou.session.hctlTab = None
        hou.session.hctlSceneViewer = None
        hou.session.hctlNetworkEditor = None
        hou.session.projectPath = hou.hipFile.path()
        hou.session.networkPath = None
        hou.session.tabType = None


        self.update_objects()
        return


    def start(self):
        hou.ui.addEventLoopCallback(self.listener)


    def stop(self):
        hou.ui.removeEventLoopCallback(self.listener)


    def update_objects(self):
        hou.session.tab = hou.ui.paneTabUnderCursor()
        hou.session.pane = hou.ui.paneUnderCursor()

        # Session
        hou.session.hctlSession = HctlSession()

        # Pane
        hou.session.hctlPane = HctlPane(hou.ui.paneUnderCursor())

        # Tab
        hou.session.hctlTab = HctlTab(hou.session.tab)

        if hou.session.hctlTab != None:

            if hou.session.hctlTab.hasNetworkControls():
                hou.session.networkPath = hou.session.hctlTab.path()
            hou.session.tabType = hou.session.hctlTab.type()

            if hou.session.tab.type() == hou.paneTabType.SceneViewer:
                hou.session.sceneViewer = HctlSceneViewer(hou.session.tab)
            else: hou.session.sceneViewer = None

            if hou.session.tab.type() == hou.paneTabType.NetworkEditor:
                hou.session.networkEditor = HctlNetworkEditor(hou.session.tab)
            else: hou.session.networkEditor = None

        # Labels
        # self.projectPathLabel.setText("Project path: " + self.projectPath())
        # if hou.session.tab.hasNetworkControls():
            # self.networkPathLabel.setText("Network Path: " + self.networkPath())
        # else: self.networkPathLabel.setText("No Network Path")
        # self.tabTypeLabel.setText("Tab type: " + str(hou.session.hctlTab.type()))


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

        self.tab_names = [tab.name() for tab in hou.session.hctlSession.tabs()]

        # Populate pane tab labels array
        self.tab_labels = []
        for tab in self.hctlSession.tabs():
            index = self.tab_types.index(tab.type())
            label = self.tab_type_names[index]
            self.tab_labels.append(label)


    def networkPath(self):
        return str(hou.session.tab.pwd())


    def projectPath(self):
        return hou.hipFile.name()
        # ct = self.project_path.count("/")
        # self.project_path = self.project_path.split("/", ct - 2)[-1]
