import hou
import types


class HCTab():
    def __init__(self, tab):
        self.tab = tab

    """
    Context
    """

    def currentNode(self):
        return self.tab.currentNode()

    def path(self):
        if self.hasNetworkControls():
            return self.pwd().path()
        else:
            return "None"

    def pwd(self):
        if self.tab.hasNetworkControls:
            return self.tab.pwd()
        else:
            return "No path"

    """
    Controls
    """

    def hasNetworkControls(self):
        return self.tab.hasNetworkControls()

    def isPin(self):
        return self.tab.isPin()

    def isShowingNetworkControls(self):
        return self.tab.isShowingNetworkControls()

    def setCheckState(self, bool):
        if bool:
            self.tab.setCheckState()

    def setPin(self, bool):
        self.tab.setPin(bool)

    def showNetworkControls(self, bool):
        self.tab.showNetworkControls(bool)

    def toggleNetworkControls(self):
        if self.hasNetworkControls():
            self.showNetworkControls(not self.isShowingNetworkControls())

    def togglePin(self):
        self.setPin(not self.isPin())

    """
    Tab
    """

    def close(self):
        self.tab.close()

    def closeOtherTabs(self):
        from .hcglobal import tabs
        for tab in tabs():
            if tab != self.tab:
                tab.close()

    def hcPane(self):
        from .hcpane import HCPane
        return HCPane(self.pane())

    # def setIsCurrentTab(self):
        # self.tab.setIsCurrentTab()

    def setTypeDetailsView(self):
        self.setType(hou.paneTabType.DetailsView)

    def setTypeNetworkEditor(self):
        self.setType(hou.paneTabType.NetworkEditor)

    def setTypeParm(self):
        self.setType(hou.paneTabType.Parm)

    def setTypePythonShell(self):
        self.setType(hou.paneTabType.PythonShell)

    def setTypeSceneViewer(self):
        self.setType(hou.paneTabType.SceneViewer)

    def setType(self, type):
        tab = self.tab.setType(type)
        return tab

    def pane(self):
        return self.tab.pane()

    def type(self):
        return self.tab.type()
