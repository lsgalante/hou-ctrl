import hou
import types


class HCTab():
    def __init__(self, tab):
        self.tab = tab
        if self.type() == hou.paneTabType.NetworkEditor:
            from .hcnetworkeditor import addFunctions
            addFunctions(self)
        elif self.type() == hou.paneTabType.SceneViewer:
            from .hcsceneviewer import addFunctions
            addFunctions(self)

    ## CONTEXT ##

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

    ## CONTROLS ##

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

    ## TAB ##

    def close(self):
        self.tab.close()

    def closeOtherTabs(self):
        from .hcsglobal import tabs
        for tab in tabs():
            if tab != self.tab:
                tab.close()

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
