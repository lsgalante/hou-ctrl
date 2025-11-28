import hou, types
from .hctab import HCTab
# Layout/viewport IDs
#
# DoubleSide:        2 3
#
# DoubleStack:       3
#                    0
#
# Quad:              2 3
#                    1 0
#
# QuadBottomSplit:     3
#                    2 1 0
#
# QuadLeftSplit:     2
#                    1 3
#                    0
#
# TripleBottomSplit:   3
#                    1   0
#
# TripleLeftSplit:   2
#                    0 3
#                    1
#
# Single:
# setViewportLayout(layout, single=-1)
# -1: current viewport (viewportmouse is/was over)
# 0: top-left quad viewport (default: Top)
# 1: top-right quad viewport (default: Perspective)
# 2: bottom-left quad viewport (default: Front)
# 3: bottom-right quad viewport (default: Right)

class HCSceneViewer(HCTab):
    def __init__(self, tab):
        print(tab)
        self.viewer = tab
        hctab = HCTab(tab)

    """
    Context
    """

    def pwd(self):
        return self.viewer.pwd()

    """
    Geometry
    """

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

    """
    Grids
    """

    def toggleGrid(self):
        refplane = self.referencePlane()
        refplane.setIsVisible(not refplane.isVisible())

    """
    Layout
    """

    def layout(self):
        return self.viewer.viewportLayout()

    def layouts(self):
        return (
            hou.geometryViewportLayout.DoubleSide,
            hou.geometryViewportLayout.DoubleStack,
            hou.geometryViewportLayout.Quad,
            hou.geometryViewportLayout.QuadBottomSplit,
            hou.geometryViewportLayout.QuadLeftSplit,
            hou.geometryViewportLayout.TripleBottomSplit,
            hou.geometryViewportLayout.TripleLeftSplit,
            hou.geometryViewportLayout.Single,
        )

    def layoutIndices(self):
        return (
            (2, 3),
            (3, 0),
            (2, 3, 1, 0),
            (3, 2, 1, 0),
            (2, 1, 0, 3),
            (3, 1, 0),
            (2, 3, 1),
            (3),
        )

    def nextLayout(self):
        index = self.layouts().index(self.layout())
        new_index = (index + 1) % len(self.layouts())
        self.setLayout(self.layouts()[new_index])
        return

    def setLayout(self, layout):
        layoutmap = {
            "DoubleSide": hou.geometryViewportLayout.DoubleSide,
            "DoubleStack": hou.geometryViewportLayout.DoubleStack,
            "Quad": hou.geometryViewportLayout.Quad,
            "QuadBottomSplit": hou.geometryViewportLayout.QuadBottomSplit,
            "QuadLeftSplit": hou.geometryViewportLayout.QuadLeftSplit,
            "Single": hou.geometryViewportLayout.Single,
            "TripleBottomSplit": hou.geometryViewportLayout.TripleBottomSplit,
            "TripleLeftSplit": hou.geometryViewportLayout.TripleLeftSplit
        }
        self.viewer.setViewportLayout(layoutmap[layout])

    """
    UI
    """

    def isShowingDisplayOptionsBar(self):
        return self.viewer.isShowingDisplayOptionsBar()

    def isShowingOperationBar(self):
        return self.viewer.isShowingOperationBar()

    def isShowingSelectionBar(self):
        return self.viewer.isShowingSelectionBar()

    def showDisplayOptionsBar(self, bool):
        self.viewer.showDisplayOptionsBar(bool)

    def showOperationBar(self, bool):
        self.viewer.showOperationBar(bool)

    def showSelectionBar(self, bool):
        self.viewer.showSelectionBar(bool)

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

    """
    Utils
    """

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
        contextmap = {
            "Object": "Entered keycam in an obj context",
            "Sop": "Entered keycam in a sop context",
            "Lop": "Entered keycam in a lop context",
        }
        context = self.pwd().childTypeCategory().name()
        if context in contextmap:
            self.viewer.setCurrentState("keycam")
            hou.ui.setStatusMessage(contextmap[context])
        else:
            hou.ui.setStatusMessage("No obj, sop or lop context", hou.severityType.Error)

    """
    Viewports
    """

    def homeAllViewports(self):
        for viewport in self.viewports():
            viewport.home()

    def viewport(self):
        return self.viewer.curViewport()

    def viewports(self):
        return self.viewer.viewports()

    def frame(self):
        for viewport in self.viewports():
            cam = viewport.camera()
            # Is camera node or default.
            if not cam:
                viewport.frameAll()
            else:
                viewport.frameAll()
