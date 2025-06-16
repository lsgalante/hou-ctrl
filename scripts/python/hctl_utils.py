import hou
from importlib import reload
import hctl
import hctl_vis_menu
import hctl_new_tab_menu
import hctl_resize
import hctl_bindings
import time


class Desktop():
    def __init__(self, paneTab):
        self.update()
        return

    def clearLayout(self):
        self.paneOnly(self.pane)
        self.paneTabOnly(self.paneTab)
        self.update()
    clearLayout.interactive_contexts = ["all"]

    def getNetworkEditors(self):
        editors = []
        for paneTab in self.paneTabs():
            if paneTab.type() == hou.paneTabType.NetworkEditor:
                editors.append(paneTab)
        return editors
    getNetworkEditors.interactive_contexts = ["none"]

    def getPanes(self):
        panes = hou.ui.curDesktop().panes()
        return panes
    getPanes.interactive_contexts = ["none"]

    def getPaneTabs(self):
        paneTabs = []
        for pane in hou.desktopPanes():
            for paneTab in pane.tabs():
                paneTabs.append(paneTab)
        return paneTabs
    getPaneTabs.interactive_contexts = ["none"]

    def getSceneViewers(self):
        paneTabs = hou.ui.paneTabs()
        sceneViewers = [paneTab for paneTab in paneTabs if paneTab.type() == hou.paneTabType.SceneViewer]
        return sceneViewers
    getSceneViewers.interactive_contexts = ["none"]

    def getViewports(self):
        viewports = []
        sceneViewers = self.getSceneViewers()
        for sceneViewer in sceneViewers:
            for viewport in sceneViewer.viewports():
                viewports.append(viewport)
        return(viewports)
    getViewports.interactive_contexts = ["none"]

    def hideShelf(self):
        desktop = hou.ui.curDesktop()
        desktop.shelfDock().show(0)
        hou.ui.reloadViewportColorSchemes()
    hideShelf.interactive_contexts = ["none"]

    def layoutA(self):
        self.clearLayout()
        # pin network editor(?) pane
        # self.panes[0].tabs()[0].setPin(False)
        # Main center split
        self.panes[0].splitHorizontally()
        self.update()
        self.panes[0].setSplitFraction(0.6)
        # Left vertical split
        self.panes[0].splitVertically()
        self.panes[0].setSplitFraction(0.2)
        # Right vertical split
        self.panes[1].splitVertically()
        self.panes[1].setSplitFraction(0.666)
        # Assign
        self.update()
        self.paneTabs[0].setType(hou.paneTabType.SceneViewer) # Top left
        self.paneTabs[1].setType(hou.paneTabType.DetailsView) # Bas left
        self.paneTabs[2].setType(hou.paneTabType.Parm) # Top right
        self.paneTabs[3].setType(hou.paneTabType.NetworkEditor) # Bas right
        # Hide etc
        # paneTabs[3].setPin(True)
        # desktopToggleMenus()
        self.toggleStowbars()
        self.toggleStowbars()
    layoutA.interactive_contexts = ["all"]

    def layoutB(self):
        self.clearLayout()
        self.panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes[0].splitHorizontally()
        self.panes[0].splitVertically()
        self.panes[1].splitVertically()
        self.update()
        # Assign top left
        self.panes[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes[1].tabs()[0].setType(hou.paneTabType.Parm)
    layoutB.interactive_contexts = ["all"]

    def layoutQuad(self):
        self.clearLayout()
        self.panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes[0].splitHorizontally()
        self.update()
        self.panes[0].splitVertically()
        self.panes[1].splitVertically()
        self.update()
    layoutQuad.interactive_contexts = ["all"]

    def layoutTriH(self):
        self.parent.session.removeEventLoopCallbacks()
        self.clearLayout()
        # Make panes
        self.panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes[0].splitHorizontally()
        self.update()
        self.panes[1].splitHorizontally()
        self.update()
        # Make paneTabs
        self.panes[1].createTab(hou.paneTabType.PythonShell)
        self.panes[1].tabs()[0].setIsCurrentTab()
        # Set types
        self.panes[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes[1].tabs()[0].setType(hou.paneTabType.Parm)
        self.panes[1].tabs()[1].setType(hou.paneTabType.DetailsView)
        self.panes[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
        # Ratios
        self.panes[0].setSplitFraction(0.5)
        self.update()
        hou.session.lastPane = hou.ui.paneUnderCursor()
        hou.ui.addEventLoopCallback(self.triHCallback)
    layoutTriH.interactive_contexts = ["all"]

    def triHCallback():
        panes = hou.ui.panes()
        pane = hou.ui.paneUnderCursor()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[1]): pane.setSplitFraction(0.6)
            elif str(pane) == str(panes[2]): pane.setSplitFraction(0.3)
        return True

    def layoutTriV(self):
        self.parent.session.removeEventLoopCallbacks()
        self.clearLayout()
        # Make panes
        self.panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes[0].splitHorizontally()
        self.update()
        self.panes[1].splitVertically()
        self.update()
        # Make pane tabs
        self.panes[1].createTab(hou.paneTabType.PythonShell)
        self.panes[1].tabs()[0].setIsCurrentTab()
        # Set types
        self.panes[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes[1].tabs()[0].setType(hou.paneTabType.Parm)
        self.panes[1].tabs()[1].setType(hou.paneTabType.DetailsView)
        self.panes[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
        # Set ratios
        self.panes[0].setSplitFraction(0.66)
        # Ok
        hou.session.lastPane = hou.ui.paneUnderCursor()
        hou.ui.addEventLoopCallback(self.triVCallback)
    layoutTriV.interactive_contexts = ["all"]

    def triVCallback():
        panes = hou.ui.panes()
        pane = hou.ui.paneUnderCursor()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[1]):
                pane.setSplitFraction(0.33)
            elif str(pane) == str(panes[2]):
                pane.setSplitFraction(0.66)
        return True

    def openColorEditor(self):
        hou.ui.selectColor()
    openColorEditor.interactive_contexts = ["all"]

    def openFloatingParameterEditor(self):
        if self.paneTab.type() == hou.paneTabType.NetworkEditor:
            node = self.paneTab.currentNode()
            hou.ui.showFloatingParameterEditor(node)
        else:
            hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)
    openFloatingParameterEditor.interactive_contexts = ["all"]

    def openHotkeyEditor(self):
        print("This function does nothing")
    openHotkeyEditor.interactive_contexts = ["none"]

    def showShelf(self):
        self.desktop.shelfDock().show(1)
    showShelf.interactive_contexts = ["none"]

    def toggleMainMenuBar(*args):
        if hou.getPreference("showmenu.val") == "1":
            hou.setPreference("showmenu.val", "0")
        else:
            hou.setPreference("showmenu.val", "1")
    toggleMainMenuBar.interactive_contexts = ["all"]

    def toggleMenus(self):
        visible = 0
        # main menu
        if hou.getPreference("showmenu.val") == "1":
            visible = 1
        # network editor menu
        elif any(editor.getPref("showmenu") == "1" for editor in self.editors):
            visible = 1
        # network controls
        elif any(paneTab.isShowingNetworkControls() for paneTab in self.paneTabs):
            visible = 1
        # scene viewer toolbars (top, right, left)
        elif any(viewer.isShowingOperationBar() for viewer in self.sceneViewers):
            visible = 1
        elif any(viewer.isShowingDisplayOptionsBar() for viewer in self.sceneViewers):
            visible = 1
        elif any(viewer.isShowingSelectionBar() for sceneViewer in self.sceneViewers):
            visible = 1
        # paneTabs
        elif any(pane.isShowingPaneTabs() for pane in self.panes):
            visible = 1
        # hide all
        if visible:
            hou.setPreference("showmenu.val", "0")
            for editor in self.editors:
                editor.setPref("showmenu", "0")
            for paneTab in self.paneTabs:
                paneTab.showNetworkControls(0)
            for pane in self.panes:
                pane.showPaneTabs(0)
            for viewer in self.sceneViewers:
                viewer.showOperationBar(0)
                viewer.showDisplayOptionsBar(0)
                viewer.showSelectionBar(0)
            hou.ui.setHideAllMinimizedStowbars(1)
        # show all
        else:
            hou.setPreference("showmenu.val", "1")
            for editor in self.editors:
                editor.setPref("showment", "1")
            for paneTab in self.paneTabs:
                paneTab.showNetworkControls(1)
            for pane in self.panes:
                pane.showPaneTabs(1)
            for viewer in self.sceneViewers:
                viewer.showOperationBar(1)
                viewer.showDisplayOptionsBar(1)
                viewer.showSelectionBar(1)
            hou.ui.setHideAllMinimizedStowbars(0)
    toggleMenus.interactive_contexts = ["all"]

    def toggleHctl(self):
        reload(hctl)
        hctl.dialog().show()
    toggleHctl.interactive_contexts = ["all"]

    def toggleNetworkControls(self):
        visible = 0
        for paneTab in self.paneTabs:
            if paneTab.isShowingNetworkControls():
                visible = 1
        for paneTab in self.paneTabs:
            paneTab.showNetworkControls((visible + 1) % 2)
    toggleNetworkControls.interactive_contexts = ["all"]

    def togglePaneTabs(self):
        visible = 0
        for pane in self.panes:
            if pane.isShowingPaneTabs():
                visible = 1
        for pane in self.panes:
            pane.showPaneTabs(not visible)
    togglePaneTabs.interactive_contexts = ["all"]

    def toggleStowbars(self):
        hidden = hou.ui.hideAllMinimizedStowbars()
        hou.ui.setHideAllMinimizedStowbars(not hidden)
    toggleStowbars.interactive_contexts = ["all"]

    def update(self):
        self.desktop = hou.ui.curDesktop()
        self.editors = self.getNetworkEditors()
        self.pane = self.paneTab.pane()
        self.panes = self.getPanes()
        self.paneTab = self.hou.ui.paneTabUnderCursor()
        self.paneTabs = self.getPaneTabs()
        self.viewers = self.getSceneViewers()

    def updateMainMenuBar(*args):
        hou.ui.updateMainMenuBar()
    updateMainMenuBar.interactive_contexts = ["all"]



class NetworkEditor():
    def __init__(self, editor):
        self.editor = editor
        self.networkBox = None
        self.stickyNote = None

    def addNetworkBox(self):
        context = self.editor.pwd()
        node = self.editor.currentNode()
        networkBox = context.createNetworkBox()
        networkBox.setPosition(node.position())
    addNetworkBox.interactive_contexts = ["paneTabType.NetworkEditor"]

    def addStickyNote(self):
        context = self.editor.pwd()
        stickyNote = context.createStickyNote()
        cursor_pos = self.editor.cursorPosition()
        stickyNote.setPosition(cursor_pos)
        color = hou.Color(0.71, 0.784, 1.0)
        stickyNote.setColor(color)
    addStickyNote.interactive_contexts = ["paneTabType.NetworkEditor"]

    def connectNodeTo(self):
        node = self.currentNode(self.editor)
        choices = ("a", "b", "c")
        popup = hou.ui.selectFromList(choices)
    connectNodeTo.interactive_contexts = ["paneTabType.NetworkEditor"]

    def currentNode(self):
        return self.editor.currentNode()
    currentNode.interactive_contexts = ["none"]

    def deselectAllNodes(self):
        node = self.CurrentNode(self.editor)
        node.setSelected(False)
    deselectAllNodes.interactive_contexts = ["paneTabType.NetworkEditor"]

    def displayNode(self):
        context = self.editor.pwd()
        return  context.displayNode()
    displayNode.interactive_contexts = ["none"]

    def renameNode(self):
        node = self.currentNode(self.editor)
        name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
        if name[0] == 0:
            node.setName(name[1])
    renameNode.interactive_contexts = ["paneTabType.NetworkEditor", "paneTabType.Parm"]

    def rotateNodeInputs(self):
        node = self.currentNode(self)
        connectors = node.inputConnectors()
    rotateNodeInputs.interactive_contexts = ["paneTabType.NetworkEditor"]

    def selectDisplayNode(self):
        displayNode = self.displayNode(self.editor)
        displayNode.setCurrent(True, True)
    selectDisplayNode.interactive_contexts = ["paneTabType.NetworkEditor"]

    def toggleDimUnusedNodes(self):
        dim = "0"
        if self.editor.getPref("dimunusednodes") == "1":
            dim = "1"
        if dim == "0":
            self.editor.setPref("dimunusednodes", "1")
        else:
            self.editor.setPref("dimunusednodes", "0")
    toggleDimUnusedNodes.interactive_contexts = ["all"]

    def toggleGridLines(self):
        visible = "0"
        if self.editor.getPref("gridmode") == "1":
            visible = "1"
        if self.editor.getPref("gridmode") == "0":
            self.editor.setPref("gridmode", "1")
        else:
            self.editor.setPref("gridmode", "0")
    toggleGridLines.interactive_contexts = ["all"]

    def toggleLocating(self):
        locating = 0
        if self.editor.locatingEnabled():
            locating = 1
        self.editor.setLocatingEnabled(not locating)
    toggleLocating.interactive_contexts = ["all"]

    def toggleMenu(self):
        visible = 0
        if self.editor.getPref("showmenu") == "1":
            visible = 1
        if visible:
            self.editor.setPref("showmenu", str(not visible))
    toggleMenu.interactive_contexts = ["all"]

    def toggleGridPoints(self):
        visible = int(self.editor.getPref("gridmode"))
        self.editor.setPref("gridmode", str(not visible))
    toggleGridPoints.interactive_contexts = ["all"]

    def update(self):
        context = self.editor.pwd()
        node = self.editor.currentNode()
        pass



class Pane():
    def __init__(self, pane):
        self.pane = pane

    def contract(self):
        fraction = self.pane.getSplitFraction()
        fraction = round(fraction, 3) + 0.1
        message = "Pane fraction: " + str(fraction)
        hou.ui.setStatusMessage(message)
        pane = pane.setSplitFraction(fraction)
    contract.interactive_contexts = ["all"]

    def expand(self):
        fraction = self.pane.getSplitFraction()
        fraction = round(fraction, 3) - 0.1
        message = "Pane fraction: " + str(fraction)
        hou.ui.setStatusMessage(message)
        pane = pane.setSplitFraction(fraction)
    expand.interactive_contexts = ["all"]

    def getRatio(self):
        return self.pane.getSplitFraction()
    getRatio.interactive_contexts = ["none"]

    def newPaneTab(self):
        reload(hctl_new_pane_tab_menu)
        newPaneTabMenu = hctl_new_pane_tab_menu.newPaneTabMenu()
        newPaneTabMenu.show()
    newPaneTab.interactive_contexts = ["all"]

    def only(self):
        for pane in hou.ui.curDesktop().panes():
            if pane != self.pane:
                for paneTab in pane.tabs():
                    paneTab.close()
    only.interactive_contexts = ["all"]

    def resize(self):
        reload(hctl_resize)
        resizeWidget = hctl_resize.resizeWidget(self.pane)
        resizeWidget.show()
    resize.interactive_contexts = ["all"]

    def setRatio(self, ratio):
        self.pane.setSplitFraction(ratio)
    setRatio.interactive_contexts = ["none"]

    def setRatioHalf(self):
        self.pane.setSplitFraction(0.5)
    setRatioHalf.interactive_contexts = ["all"]

    def setRatioQuarter(self):
        self.pane.setSplitFraction(0.25)
    setRatioQuarter.interactive_contexts = ["all"]

    def setRatioThird(self):
        self.pane.setSplitFraction(0.333)
    setRatioThird.interactive_contexts = ["all"]

    def splitHorizontal(self):
        newPane = self.pane.splitHorizontally()
    splitHorizontal.interactive_contexts = ["all"]

    def splitVertical(self):
        newPane = self.pane.splitVertically()
    splitVertical.interactive_contexts = ["all"]

    def splitRotate(self):
        self.pane.splitRotate()
    splitRotate.interactive_contexts = ["all"]

    def splitSwap(self):
        self.pane.splitSwap()
    splitSwap.interactive_contexts = ["all"]

    def toggleMaximized(self):
        self.pane.setIsMaximized(not self.pane.isMaximized())
    toggleMaximized.interactive_contexts = ["all"]

    def togglePaneTabs(self):
        self.pane.showPaneTabs(not self.pane.isShowingPaneTabs())
    togglePaneTabs.interactive_contexts = ["all"]

    def toggleSplitMaximized(self):
        self.pane.setIsSplitMaximized(not self.pane.isSplitMaximized())
    toggleSplitMaximized.interactive_contexts = ["all"]



class PaneTab(object):
    def __init__(self, paneTab):
        self.paneTab = paneTab

    def close(self):
        self.paneTab.close()
    close.interactive_contexts = ["all"]

    def currentNode(self):
        if self.paneTab.hasNetworkControls():
            return self.paneTab.currentNode()
    currentNode.interactive_contexts = ["none"]

    def path(self):
        if self.paneTab.hasNetworkControls():
            return self.paneTab.pwd().path()
        else:
            return "No path"
    path.interactive_contexts = ["none"]

    def only(self):
        for paneTab in self.parent.desktop.paneTabs:
            if paneTab != self.paneTab:
                paneTab.close()
    only.interactive_contexts = ["all"]

    def setTypeDetailsView(self):
        self.paneTab.setType(hou.paneTabType.DetailsView)
    setTypeDetailsView.interactive_contexts = ["all"]

    def setTypeNetworkEditor(self):
        self.paneTab.setType(hou.paneTabType.NetworkEditor)
    setTypeNetworkEditor.interactive_contexts = ["all"]

    def setTypeParm(self):
        self.paneTab.setType(hou.paneTabType.Parm)
    setTypeParm.interactive_contexts = ["all"]

    def setTypePythonShell(self):
        self.paneTab.setType(hou.paneTabType.PythonShell)
    setTypePythonShell.interactive_contexts = ["all"]

    def setTypeSceneViewer(self):
        self.paneTab.setType(hou.paneTabType.SceneViewer)
    setTypeSceneViewer.interactive_contexts = ["all"]

    def toggleNetworkControls(self):
        if self.paneTab.hasNetworkControls():
            self.paneTab.showNetworkControls(not self.paneTab.isShowingNetworkControls())
    toggleNetworkControls.interactive_contexts = ["all"]

    def togglePin(self):
        self.paneTab.setPin(not self.paneTab.isPin())
    togglePin.interactive_contexts = ["all"]



class Printer():
    def __init__(self):
        self.message = ""

    def layout(self):
        message = "Layout:"
        desktop = hou.ui.curDesktop()
        panes = desktop.panes()
        ct = 0
        for pane in panes:
            message += " Pane" + str(ct) + " -"
            if pane.isSplit():
                message += " split"
            else:
                message += " whole"
                message += "    "
            ct += 1
        message = message[0:-1]
        hou.ui.setStatusMessage(message)
    layout.interactive_contexts = ["all"]



class SceneViewer():
    def __init__(self, sceneViewer):
        self.sceneViewer = self.sceneViewer
        self.update()

    def getDisplaySets(self):
        displaySets = []
        for viewport in self.viewports:
            settings = viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
        return(displaySets)
    getDisplaySets.interactive_contexts = ["none"]

    def layoutDoubleSide(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleSide)
    layoutDoubleSide.interactive_contexts = ["paneTabType.SceneViewer"]

    def layoutDoubleStack(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleStack)
    layoutDoubleStack.interactive_contexts = ["paneTabType.SceneViewer"]

    def layoutQuad(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.Quad)
    layoutQuad.interactive_contexts = ["paneTabType.SceneViewer"]

    def layoutQuadBottomSplit(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadBottomSplit)
    layoutQuadBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]

    def layoutQuadLeftSplit(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadLeftSplit)
    layoutQuadLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]

    def layoutSingle(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.Single)
    layoutSingle.interactive_contexts = ["paneTabType.SceneViewer"]

    def layoutTripleBottomSplit(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleBottomSplit)
    layoutTripleBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]

    def layoutTripleLeftSplit(self):
        self.sceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleLeftSplit)
    layoutTripleLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]

    def lopToggleLightGeo(self):
        visible = self.sceneViewer.showLights()
        self.sceneViewer.setShowLights(not visible)
    lopToggleLightGeo.interactive_contexts = ["paneTabType.SceneViewer"]

    def visualizerMenu(self):
        reload(hctl_vis_menu)
        visualizerMenu = hctl_vis_menu.visualizerMenu()
        visualizerMenu.show()
    visualizerMenu.interactive_contexts = ["paneTabType.SceneViewer"]

    def toggleBackface(self):
        visible = 0
        for displaySet in self.displaySets:
            if displaySet.isShowingPrimBackfaces():
                visible = 1
        for displaySet in self.displaySets:
            displaySet.showPrimBackfaces(not visible)
    toggleBackface.interactive_contexts = ["paneTabType.SceneViewer"]

    def toggleDisplayOptionsToolbar():
        visible = 0
        if self.sceneViewer.isShowingDisplayOptionsBar():
            visible = 1
        self.sceneViewer.showDisplayOptionsBar(not visible)
    toggleDisplayOptionsToolbar.interactive_contexts = ["paneTabType.SceneViewer"]

    def toggleGrid(self):
        visible = self.sceneViewer.referencePlane().isVisible()
        self.sceneViewer.referencePlane().setIsVisible(not visible)
    toggleGrid.interactive_contexts = ["paneTabType.SceneViewer"]

    def toggleGroupList(self):
        visible = 0
        if self.sceneViewer.isGroupListVisible():
            visible = 1
        self.sceneViewer.setGroupListVisible(not visible)
    toggleGroupList.interactive_contexts = ["paneTabType.SceneViewer"]

    def toggleKeycam(self):
        context = self.sceneViewer.pwd()
        context_type = context.childTypeCategory().name()
        if context_type == "Object":
            self.sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam viewer state in Obj context.")
        elif context_type == "Sop":
            self.sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam viewer state in Sop context.")
        elif context_type == "Lop":
            self.sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam viewer state in Lop context.")
        else:
            hou.ui.setStatusMessage("No Obj, Sop or Lop context.", hou.severityType.Error)
    toggleKeycam.interactive_contexts = ["paneTabType.SceneViewer"]

    def togglePointMarkers(self):
        visible = 0
        for displaySet in self.displaySets:
            if displaySet.isShowingPointMarkers():
                visible = 1
        for displaySet in self.displaySets:
            displaySet.showPointMarkers(not visible)
    togglePointMarkers.interactive_contexts = ["paneTabType.SceneViewer"]

    def togglePointNormals(self):
        visible = 0
        for displaySet in self.displaySets:
            if displaySet.isShowingPointNormals():
                visible = 1
        for displaySet in self.displaySets:
            displaySet.showPointNormals(not visible)
    togglePointNormals.interactive_contexts = ["paneTabType.SceneViewer"]

    def togglePointNumbers(self):
        visible = 0
        for displaySet in self.displaySets:
            if displaySet.isShowingPointNumbers():
                visible = 1
        for displaySet in self.displaySets:
            displaySet.showPointNumbers(not visible)
    togglePointNumbers.interactive_contexts = ["paneTabType.SceneViewer"]

    def togglePrimNormals(self):
        visible = 0
        for displaySet in self.displaySets:
            if displaySet.isShowingPrimNormals():
                visible = 1
            for displaySet in displaySets:
                displaySet.showPrimNormals(not_visible)
    togglePrimNormals.interactive_contexts = ["paneTabType.SceneViewer"]

    def togglePrimNumbers(self):
        visible = 0
        for displaySet in self.displaySets:
            if displaySet.isShowingPrimNumbers():
                visible = 1
        for displaySet in self.displaySets:
            displaySet.showPrimNumbers(not visible)
    togglePrimNumbers.interactive_contexts = ["paneTabType.SceneViewer"]

    def toggleToolbars(self):
        state1 = self.sceneViewer.isShowingOperationBar()
        state2 = self.sceneViewer.isShowingDisplayOptionsBar()
        state3 = self.sceneViewer.isShowingSelectionBar()
        if state1 + state2 + state3 > 0:
            self.sceneViewer.showOperationBar(0)
            self.sceneViewer.showDisplayOptionsBar(0)
            self.sceneViewer.showSelectionBar(0)
        else:
            self.sceneViewer.showOperationBar(1)
            self.sceneViewer.showDisplayOptionsBar(1)
            self.sceneViewer.showSelectionBar(1)
    toggleToolbars.interactive_contexts = ["paneTabType.SceneViewer"]

    def toggleVectors(self):
        for viewport in self.viewports:
            viewportSettings = viewport.settings()
            vector_scale = viewportSettings.vectorScale()
            if vector_scale == 1:
                viewportSettings.setVectorScale(0)
            elif vector_scale == 0:
                viewportSettings.setVectorScale(1)
            else:
                viewportSettings.setVectorScale(1)
    toggleVectors.interactive_contexts = ["paneTabType.SceneViewer"]

    def update(self):
        self.displaySets = self.getDisplaySets()
        self.viewport = self.sceneViewer.curViewport()
        self.viewports = self.sceneViewer.viewports()


class Session():
    def __init__(self):
        self.update()
        return

    def reloadKeyBindings(self):
        reload(hctl_bindings)
        hctl_bindings.updateBindings()
    reloadKeyBindings.interactive_contexts = ["all"]

    def reloadColorSchemes(self):
        hou.ui.reloadColorScheme()
    reloadColorSchemes.interactive_contexts = ["all"]

    def openFile(self):
        hou.ui.selectFile()
    openFile.interactive_contexts = ["all"]

    def removeEventLoopCallbacks(self):
        callbacks = hou.ui.eventLoopCallbacks()
        for callback in callbacks:
            hou.ui.removeEventLoopCallback(callback)
    removeEventLoopCallbacks.interactive_contexts = ["all"]

    def reloadKeycam(self):
        hou.ui.reloadViewerState("keycam")
    reloadKeycam.interactive_contexts = ["all"]

    def restart(self):
        print("This function does nothing")
    restart.interactive_contexts = ["none"]

    def triggerUpdate(self):
        hou.ui.triggerUpdate()
    triggerUpdate.interactive_contexts = ["all"]

    def updateModeAuto(self):
        hou.setUpdateMode(hou.updateMode.AutoUpdate)
    updateModeAuto.interactive_contexts = ["all"]

    def updateModeManual(self):
        hou.setUpdateMode(hou.updateMode.Manual)
    updateModeManual.interactive_contexts = ["all"]

    def toggleAutoSave(self):
        if self.autosave_state == "0":
            self.autosave_state = "1"
        else:
            self.autosave_state = "0"
        hou.setPreference("autoSave", self.autosave_state)
    toggleAutoSave.interactive_contexts = ["none"]

    def update(self):
        self.autosave_state = hou.getPreference("autoSave")



class Viewport():
    def __init__(self, viewport):
        self.viewport = viewport

    def update():
        pass

    def visualizers(self):
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr
