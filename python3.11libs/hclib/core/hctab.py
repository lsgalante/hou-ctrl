import hou
import types


class HCTab():
    def __init__(self, tab):
        self.tab = tab

    """
    Controls
    """

    def toggleNetworkControls(self):
        if self.tab.hasNetworkControls():
            self.tab.showNetworkControls(not self.tab.isShowingNetworkControls())

    def togglePin(self):
        self.tab.setPin(not self.tab.isPin())

    """
    Tab
    """

    def close(self):
        self.tab.close()

    def closeOtherTabs(self):
        for tab in self.pane().tabs():
            if tab != self.tab:
                tab.close()

    def hcPane(self):
        from .hcpane import HCPane
        return HCPane(self.pane())

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
