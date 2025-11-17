import hou
import types


def addFunctions(hc_tab):
    hc_tab.displaySets = types.MethodType(displaySets, hc_tab)
    hc_tab.homeAllViewports = types.MethodType(homeAllViewports, hc_tab)
    hc_tab.isShowingDisplayOptionsBar = types.MethodType(isShowingDisplayOptionsBar, hc_tab)
    hc_tab.isShowingOperationBar = types.MethodType(isShowingOperationBar, hc_tab)
    hc_tab.isShowingSelectionBar = types.MethodType(isShowingSelectionBar, hc_tab)
    hc_tab.keycam = types.MethodType(keycam, hc_tab)
    hc_tab.setLayoutDoubleSide = types.MethodType(setLayoutDoubleSide, hc_tab)
    hc_tab.setLayoutDoubleStack = types.MethodType(setLayoutDoubleStack, hc_tab)
    hc_tab.setLayoutQuad = types.MethodType(setLayoutQuad, hc_tab)
    hc_tab.setLayoutQuadBottomSplit = types.MethodType(setLayoutQuadBottomSplit, hc_tab)
    hc_tab.setLayoutQuadLeftSplit = types.MethodType(setLayoutQuadLeftSplit, hc_tab)
    hc_tab.setLayoutSingle = types.MethodType(setLayoutSingle, hc_tab)
    hc_tab.setLayoutTripleBottomSplit = types.MethodType(setLayoutTripleBottomSplit, hc_tab)
    hc_tab.setLayoutTripleLeftSplit = types.MethodType(setLayoutTripleLeftSplit, hc_tab)
    hc_tab.showDisplayOptionsBar = types.MethodType(showDisplayOptionsBar, hc_tab)
    hc_tab.showOperationBar = types.MethodType(showOperationBar, hc_tab)
    hc_tab.showSelectionBar = types.MethodType(showSelectionBar, hc_tab)
    hc_tab.toggleLightGeo = types.MethodType(toggleLightGeo, hc_tab)
    hc_tab.toggleBackface = types.MethodType(toggleBackface, hc_tab)
    hc_tab.toggleDisplayOptionsToolbar = types.MethodType(toggleDisplayOptionsToolbar, hc_tab)
    hc_tab.toggleOperationBar = types.MethodType(toggleOperationBar, hc_tab)
    hc_tab.toggleSelectionBar = types.MethodType(toggleSelectionBar, hc_tab)
    hc_tab.toggleGrid = types.MethodType(toggleGrid, hc_tab)
    hc_tab.toggleGroupList = types.MethodType(toggleGroupList, hc_tab)
    hc_tab.togglePointMarkers = types.MethodType(togglePointMarkers, hc_tab)
    hc_tab.togglePointNormals = types.MethodType(togglePointNormals, hc_tab)
    hc_tab.togglePointNumbers = types.MethodType(togglePointNumbers, hc_tab)
    hc_tab.togglePrimNormals = types.MethodType(togglePrimNormals, hc_tab)
    hc_tab.togglePrimNumbers = types.MethodType(togglePrimNumbers, hc_tab)
    hc_tab.toggleToolbars = types.MethodType(toggleToolbars, hc_tab)
    hc_tab.toggleVectors = types.MethodType(toggleVectors, hc_tab)
    hc_tab.viewport = types.MethodType(viewport, hc_tab)
    hc_tab.viewports = types.MethodType(viewports, hc_tab)
    hc_tab.visualizerPanel = types.MethodType(visualizerPanel, hc_tab)

## CONTROLS ##

def isShowingDisplayOptionsBar(self):
    return self.tab.isShowingDisplayOptionsBar()

def isShowingOperationBar(self):
    return self.tab.isShowingOperationBar()

def isShowingSelectionBar(self):
    return self.tab.isShowingSelectionBar()

def showDisplayOptionsBar(self, bool):
    self.tab.showDisplayOptionsBar(bool)

def showOperationBar(self, bool):
    self.tab.showOperationBar(bool)

def showSelectionBar(self, bool):
    self.tab.showSelectionBar(bool)

def toggleDisplayOptionsToolbar(self):
    self.showDisplayOptionsBar(not self.isShowingDisplayOptionsBar())

def toggleGroupList(self):
    self.setGroupListVisible(not self.isGroupListVisible())

def toggleOperationBar(self):
    self.showOperationBar(not self.isShowingOperationBar())

def toggleSelectionBar(self):
    self.showSelectionBar(not self.isShowingSelectionBar())

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

## DISPLAY OPTIONS ##

def displaySets(self):
    displaySets = []
    for viewport in self.viewports():
        settings = viewport.settings()
        displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
        displaySets.append(displaySet)
    return(displaySets)

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

def toggleGrid(self):
    refplane = self.referencePlane()
    refplane.setIsVisible(not refplane.isVisible())

def togglePointMarkers(self):
    visible = 0
    displaySets = self.displaySets()
    print(displaySets)
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

## LAYOUT ##

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

def viewport(self):
    return self.tab.curViewport()

def viewports(self):
    return self.tab.viewports()

## UTILS ##

def keycam(self):
    # Contexts:
    # Chop
    # ChopNet
    # Cop
    # Cop2
    # CopNet
    # Data
    # Director
    # Dop
    # Driver
    # Lop
    # Manager
    # Object
    # Shop
    # Sop
    # Top
    # TopNet
    # Vop
    # VopNet
    context = self.pwd().childTypeCategory().name()
    if context == "Object":
        self.tab.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam in an obj context")
    elif context == "Sop":
        self.tab.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam in a sop context")
    elif context == "Lop":
        self.tab.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam in a lop context")
    else:
        hou.ui.setStatusMessage("No obj, sop or lop context", hou.severityType.Error)

def visualizerPanel(self):
    from .ui.hcvisualizerpanel import HCVisualizerPanel
    panel = HCVisualizerPanel()
    panel.show()

## VIEW ##

def homeAllViewports(self):
    for viewport in self.viewports():
        viewport.home()
