import hou


class HCSceneViewer():

    def __init__(self, paneTab):
        self.paneTab = paneTab


    def displaySets(self):
        displaySets = []
        for viewport in self.viewports():
            settings = viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
        return(displaySets)


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


    def pwd(self):
        return self.paneTab.pwd()


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
        from hctl.ui.visualizerdialog import visualizerMenu
        panel = visualizerMenu()
        panel.show()
