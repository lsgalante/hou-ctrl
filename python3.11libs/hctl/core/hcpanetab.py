import hou
import types


class HCPaneTab():
    def __init__(self, paneTab):
        self.paneTab = paneTab
        if self.type() == hou.paneTabType.NetworkEditor:
            addNetworkEditorFunctions(self)
        elif self.type() == hou.paneTabType.SceneViewer:
            addSceneViewerFunctions(self)


    def close(self):
        self.paneTab.close()


    def closeOtherPaneTabs(self):
        from .core.hcsession import paneTabs
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


    # def setIsCurrentTab(self):
        # self.paneTab.setIsCurrentTab()


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



# Network editor functions

def addNetworkEditorFunctions(hcPaneTab):
    hcPaneTab.addNetworkBox        = types.MethodType(addNetworkBox, hcPaneTab)
    hcPaneTab.addStickyNote        = types.MethodType(addStickyNote, hcPaneTab)
    hcPaneTab.nextGrid             = types.MethodType(nextGrid, hcPaneTab)
    hcPaneTab.deselectAll          = types.MethodType(nextGrid, hcPaneTab)
    hcPaneTab.renameNode           = types.MethodType(renameNode, hcPaneTab)
    hcPaneTab.selectDisplayNode    = types.MethodType(selectDisplayNode, hcPaneTab)
    hcPaneTab.toggleDimUnusedNodes = types.MethodType(toggleDimUnusedNodes, hcPaneTab)
    hcPaneTab.toggleLocating       = types.MethodType(toggleLocating, hcPaneTab)
    hcPaneTab.toggleMenu           = types.MethodType(toggleMenu, hcPaneTab)
    hcPaneTab.toggleGridPoints     = types.MethodType(toggleGridPoints, hcPaneTab)


def addNetworkBox(self):
    networkBox = self.pwd().createNetworkBox()
    networkBox.setPosition(self.currentNode().position())


def addStickyNote(self):
    stickyNote = self.pwd().createStickyNote()
    cursor_pos = self.cursorPosition()
    stickyNote.setPosition(cursor_pos)
    stickyNote.setColor(hou.Color(0.71, 0.78, 1.0))


# def connectNode(self):
# return
# choices = ("a", "b", "c")
# popup = hou.ui.selectFromList(choices)


def nextGrid(self):
    mode = int(self.getPref("gridmode"))
    mode = (mode + 1) % 3
    self.setPref("gridmode", mode)


def deselectAll(self):
    self.currentNode().setSelected(False)


def renameNode(self):
    node = self.currentNode()
    name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
    if name[0] == 0:
        node.setName(name[1])


# def rotateNodeInputs(self):
# return
# node = self.currentNode()
# connectors = node.inputConnectors()


def selectDisplayNode(self):
    self.pwd().setCurrent(True, True)


def toggleDimUnusedNodes(self):
    dim = int(self.getPref("dimunusednodes"))
    self.setPref("dimunusednodes", str(not dim))


def toggleLocating(self):
    self.setLocatingEnabled(not self.locatingEnabled())


def toggleMenu(self):
    visible = int(self.getPref("showmenu"))
    self.setPref("showmenu", str(not visible))


def toggleGridPoints(self):
    visible = int(self.getPref("gridmode"))
    self.setPref("gridmode", str(not visible))



# Scene viewer functions

def addSceneViewerFunctions(hcPaneTab):
    hcPaneTab.displaySets = types.MethodType(displaySets, hcPaneTab)
    hcPaneTab.homeAllViewports = types.MethodType(homeAllViewports, hcPaneTab)
    print("a")
    hcPaneTab.isShowingDisplayOptionsBar = types.MethodType(isShowingDisplayOptionsBar, hcPaneTab)
    hcPaneTab.isShowingOperationBar = types.MethodType(isShowingOperationBar, hcPaneTab)
    hcPaneTab.isShowingSelectionBar = types.MethodType(isShowingSelectionBar, hcPaneTab)
    hcPaneTab.keycam = types.MethodType(keycam, hcPaneTab)
    hcPaneTab.setLayoutDoubleSide = types.MethodType(setLayoutDoubleSide, hcPaneTab)
    hcPaneTab.setLayoutDoubleStack = types.MethodType(setLayoutDoubleStack, hcPaneTab)
    hcPaneTab.setLayoutQuad = types.MethodType(setLayoutQuad, hcPaneTab)
    hcPaneTab.setLayoutQuadBottomSplit = types.MethodType(setLayoutQuadBottomSplit, hcPaneTab)
    hcPaneTab.setLayoutQuadLeftSplit = types.MethodType(setLayoutQuadLeftSplit, hcPaneTab)
    hcPaneTab.setLayoutSingle = types.MethodType(setLayoutSingle, hcPaneTab)
    hcPaneTab.setLayoutTripleBottomSplit = types.MethodType(setLayoutTripleBottomSplit, hcPaneTab)
    hcPaneTab.setLayoutTripleLeftSplit = types.MethodType(setLayoutTripleLeftSplit, hcPaneTab)
    hcPaneTab.showDisplayOptionsBar = types.MethodType(showDisplayOptionsBar, hcPaneTab)
    hcPaneTab.showOperationBar = types.MethodType(showOperationBar, hcPaneTab)
    hcPaneTab.showSelectionBar = types.MethodType(showSelectionBar, hcPaneTab)
    hcPaneTab.toggleLightGeo = types.MethodType(toggleLightGeo, hcPaneTab)
    hcPaneTab.toggleBackface = types.MethodType(toggleBackface, hcPaneTab)
    hcPaneTab.toggleDisplayOptionsToolbar = types.MethodType(toggleDisplayOptionsToolbar, hcPaneTab)
    hcPaneTab.toggleOperationBar = types.MethodType(toggleOperationBar, hcPaneTab)
    hcPaneTab.toggleSelectionBar = types.MethodType(toggleSelectionBar, hcPaneTab)
    hcPaneTab.toggleGrid = types.MethodType(toggleGrid, hcPaneTab)
    hcPaneTab.toggleGroupList = types.MethodType(toggleGroupList, hcPaneTab)
    hcPaneTab.togglePointMarkers = types.MethodType(togglePointMarkers, hcPaneTab)
    hcPaneTab.togglePointNormals = types.MethodType(togglePointNormals, hcPaneTab)
    hcPaneTab.togglePointNumbers = types.MethodType(togglePointNumbers, hcPaneTab)
    hcPaneTab.togglePrimNormals = types.MethodType(togglePrimNormals, hcPaneTab)
    hcPaneTab.togglePrimNumbers = types.MethodType(togglePrimNumbers, hcPaneTab)
    hcPaneTab.toggleToolbars = types.MethodType(toggleToolbars, hcPaneTab)
    hcPaneTab.toggleVectors = types.MethodType(toggleVectors, hcPaneTab)
    hcPaneTab.viewport = types.MethodType(viewport, hcPaneTab)
    hcPaneTab.viewports = types.MethodType(viewports, hcPaneTab)
    hcPaneTab.visualizerPanel = types.MethodType(visualizerPanel, hcPaneTab)


def displaySets(self):
    displaySets = []
    for viewport in self.viewports():
        settings = viewport.settings()
        displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
        displaySets.append(displaySet)
    return(displaySets)


def homeAllViewports(self):
    print("b")
    for viewport in self.viewports():
        viewport.home()


def isShowingDisplayOptionsBar(self):
    return self.paneTab.isShowingDisplayOptionsBar()


def isShowingOperationBar(self):
    return self.paneTab.isShowingOperationBar()


def isShowingSelectionBar(self):
    return self.paneTab.isShowingSelectionBar()


def keycam(self):
    # Contexts:
    # Chop, ChopNet, Cop, Cop2, CopNet, Data, Director, Dop, Driver, Lop, Manager, Object, Shop, Sop, Top, TopNet, Vop, VopNet
    context = self.pwd().childTypeCategory().name()
    if context == "Object":
        self.paneTab.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam viewer state in Obj context.")
    elif context == "Sop":
        self.paneTab.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam viewer state in Sop context.")
    elif context == "Lop":
        self.paneTab.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam viewer state in Lop context.")
    else:
        hou.ui.setStatusMessage("No Obj, Sop or Lop context.", hou.severityType.Error)


def setLayoutDoubleSide(self):
    self.setViewportLayout(hou.geometryViewportLayout.DoubleSide)


def setLayoutDoubleStack(self):
    self.setViewportLayout(hou.geometryViewportLayout.DoubleStack)


def setLayoutQuad(self):
    self.setViewportLayout(hou.geometryViewportLayout.Quad)


def setLayoutQuadBottomSplit(self):
    self.setViewportLayout(hou.geometryViewportLayout.QuadBottomSplit)


def setLayoutQuadLeftSplit(self):
    self.setViewportLayout(hou.geometryViewportLayout.QuadLeftSplit)


def setLayoutSingle(self):
    self.setViewportLayout(hou.geometryViewportLayout.Single)


def setLayoutTripleBottomSplit(self):
    self.setViewportLayout(hou.geometryViewportLayout.TripleBottomSplit)


def setLayoutTripleLeftSplit(self):
    self.setViewportLayout(hou.geometryViewportLayout.TripleLeftSplit)


def showDisplayOptionsBar(self, bool):
    self.paneTab.showDisplayOptionsBar(bool)


def showOperationBar(self, bool):
    self.paneTab.showOperationBar(bool)


def showSelectionBar(self, bool):
    self.paneTab.showSelectionBar(bool)


def toggleLightGeo(self):
    self.setShowLights(not self.showLights())


def toggleBackface(self):
    visible = 0
    displaySets = self.displaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPrimBackfaces():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPrimBackfaces(not visible)


def toggleDisplayOptionsToolbar(self):
    self.showDisplayOptionsBar(not self.isShowingDisplayOptionsBar())


def toggleOperationBar(self):
    self.showOperationBar(not self.isShowingOperationBar())


def toggleSelectionBar(self):
    self.showSelectionBar(not self.isShowingSelectionBar())


def toggleGrid(self):
    refplane = self.referencePlane()
    refplane.setIsVisible(not refplane.isVisible())


def toggleGroupList(self):
    self.setGroupListVisible(not self.isGroupListVisible())


def togglePointMarkers(self):
    visible = 0
    displaySets = self.displaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointMarkers():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPointMarkers(not visible)


def togglePointNormals(self):
    visible = 0
    displaySets = self.displaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointNormals():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPointNormals(not visible)


def togglePointNumbers(self):
    visible = 0
    displaySets = self.displaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointNumbers():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPointNumbers(not visible)


def togglePrimNormals(self):
    visible = 0
    displaySets = self.displaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPrimNormals():
            visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNormals(not visible)


def togglePrimNumbers(self):
    visible = 0
    displaySets = self.displaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPrimNumbers():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPrimNumbers(not visible)


def toggleToolbars(self):
    state1 = self.isShowingOperationBar()
    state2 = self.isShowingDisplayOptionsBar()
    state3 = self.isShowingSelectionBar()
    if state1 + state2 + state3 > 0:
        self.showOperationBar(0)
        self.showDisplayOptionsBar(0)
        self.showSelectionBar(0)
    else:
        self.showOperationBar(1)
        self.showDisplayOptionsBar(1)
        self.showSelectionBar(1)


def toggleVectors(self):
    for viewport in self.viewports():
        viewportSettings = viewport.settings()
        vector_scale = viewportSettings.vectorScale()
        if vector_scale == 1:
            viewportSettings.setVectorScale(0)
        elif vector_scale == 0:
            viewportSettings.setVectorScale(1)
        else:
            viewportSettings.setVectorScale(1)


def viewport(self):
    return self.paneTab.curViewport()


def viewports(self):
    return self.paneTab.viewports()


def visualizerPanel(self):
    from .ui.hcvisualizerpanel import HCVisualizerPanel
    panel = HCVisualizerPanel()
    panel.show()
