import hou
import types


class HCTab():
    def __init__(self, tab):
        self.tab = tab
        if self.type() == hou.paneTabType.NetworkEditor:
            import .hcnetworkeditor
            hcnetworkeditor.addFunctions(self)
        elif self.type() == hou.paneTabType.SceneViewer:
            import .hcsceneviewer
            hcsceneviewer.addFunctions(self)

    ## CONTEXT ##

    def currentNode(self):
        return self.paneTab.currentNode()

    def path(self):
        if self.hasNetworkControls():
            return self.pwd().path()
        else:
            return "None"

    def pwd(self):
        if self.paneTab.hasNetworkControls:
            return self.paneTab.pwd()
        else:
            return "No path"

    ## CONTROLS ##

    def hasNetworkControls(self):
        return self.paneTab.hasNetworkControls()

    def isPin(self):
        return self.paneTab.isPin()

    def isShowingNetworkControls(self):
        return self.paneTab.isShowingNetworkControls()

    def setCheckState(self, bool):
        if bool:
            self.tab.setCheckState()

    def setPin(self, bool):
        self.paneTab.setPin(bool)

    def showNetworkControls(self, bool):
        self.tab.showNetworkControls(bool)

    def toggleNetworkControls(self):
        if self.hasNetworkControls():
            self.showNetworkControls(not self.isShowingNetworkControls())

    def togglePin(self):
        self.setPin(not self.isPin())

    ## TAB ##

    def close(self):
        self.tab.close()

    def closeOtherTabs(self):
        from .hcsglobal import tabs
        for tab in tabs():
            if tab != self.tab:
                tab.close()

    # def setIsCurrentTab(self):
        # self.paneTab.setIsCurrentTab()

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
        return self.paneTab.pane()

    def type(self):
        return self.paneTab.type()
