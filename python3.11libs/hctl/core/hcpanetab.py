import hou


class HCPaneTab():
    def __init__(self, paneTab):
        self.paneTab = paneTab


    def close(self):
        self.paneTab.close()


    def closeOtherPaneTabs(self):
        from hctl.core.hcsession import paneTabs
        for paneTab in paneTabs():
            if paneTab != self.paneTab:
                paneTab.close()


    def currentNode(self):
        return self.paneTab.currentNode()


    def hasNetworkControls(self):
        return self.paneTab.hasNetworkControls()


    def isPin(self):
        return self.paneTab.isPin()


    def isShowingNetworkControls(self):
        return self.paneTab.isShowingNetworkControls()


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


    def setCheckState(self, bool):
        if bool:
            self.paneTab.setCheckState()


    def setPin(self, bool):
        self.paneTab.setPin(bool)


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
        paneTab = self.paneTab.setType(type)
        return paneTab


    def showNetworkControls(self, bool):
        self.paneTab.showNetworkControls(bool)


    def pane(self):
        return self.paneTab.pane()


    def paneTabs(self):
        return self.pane().tabs()


    def toggleNetworkControls(self):
        if self.hasNetworkControls():
            self.showNetworkControls(not self.isShowingNetworkControls())


    def togglePin(self):
        self.setPin(not self.isPin())


    def type(self):
        return self.paneTab.type()
