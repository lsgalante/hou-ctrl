import hou
from hou import Desktop, Pane, PaneTab, SceneViewer, GeometryViewport
from importlib import reload
import hctl_panel
import hctl_vis_panel
# import hctl_new_tab_panel
import hctl_resize_panel
import hctl_bindings


class HctlNetworkEditor(PaneTab):
    def __init__(self):
        pass

    def update(self):
        self.context = self.pwd()
        self.node = self.currentNode()


    def addNetworkBox(self):
        self.update()
        networkBox = self.pwd().createNetworkBox()
        networkBox.setPosition(self.currentNode().position())
    addNetworkBox.interactive_contexts = ["paneTabType.NetworkEditor"]


    def addStickyNote(self):
        stickyNote = self.pwd().createStickyNote()
        cursor_pos = self.cursorPosition()
        stickyNote.setPosition(cursor_pos)
        color = hou.Color(0.71, 0.784, 1.0)
        stickyNote.setColor(color)
    addStickyNote.interactive_contexts = ["paneTabType.NetworkEditor"]


    def connectNode(self):
        return
        # choices = ("a", "b", "c")
        # popup = hou.ui.selectFromList(choices)
    connectNode.interactive_contexts = ["paneTabType.NetworkEditor"]


    def cycleGrid(self):
        mode = int(self.getPref("gridmode"))
        mode = (mode + 1) % 3
        self.setPref("gridmode", mode)
    cycleGrid.interactive_contexts = ["all"]


    def deselectAll(self):
        self.currentNode().setSelected(False)
    deselectAll.interactive_contexts = ["paneTabType.NetworkEditor"]


    def renameNode(self):
        node = self.currentNode()
        name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
        if name[0] == 0:
            node.setName(name[1])
    renameNode.interactive_contexts = ["paneTabType.NetworkEditor", "paneTabType.Parm"]


    def rotateNodeInputs(self):
        return
        # node = self.currentNode()
        # connectors = node.inputConnectors()
    rotateNodeInputs.interactive_contexts = ["paneTabType.NetworkEditor"]


    def selectDisplayNode(self):
        self.pwd().setCurrent(True, True)
    selectDisplayNode.interactive_contexts = ["paneTabType.NetworkEditor"]


    def toggleDimUnusedNodes(self):
        dim = int(self.getPref("dimunusednodes"))
        self.setPref("dimunusednodes", str(not dim))
    toggleDimUnusedNodes.interactive_contexts = ["all"]


    def toggleLocating(self):
        self.setLocatingEnabled(not self.locatingEnabled())
    toggleLocating.interactive_contexts = ["all"]


    def toggleMenu(self):
        visible = int(self.getPref("showmenu"))
        self.setPref("showmenu", str(not visible))
    toggleMenu.interactive_contexts = ["all"]


    def toggleGridPoints(self):
        visible = int(self.getPref("gridmode"))
        self.setPref("gridmode", str(not visible))
    toggleGridPoints.interactive_contexts = ["all"]



class HctlPane(hou.Pane):
    def __init__(self, pane):
        self.pane = pane


    def contract(self):
        fraction = self.getSplitFraction()
        fraction = round(fraction, 3) + 0.1
        hou.ui.setStatusMessage("Pane fraction: " + str(fraction))
        self.setSplitFraction(fraction)
    contract.interactive_contexts = ["all"]


    def expand(self):
        fraction = self.getSplitFraction()
        fraction = round(fraction, 3) - 0.1
        message = "Pane fraction: " + str(fraction)
        hou.ui.setStatusMessage(message)
        self.setSplitFraction(fraction)
    expand.interactive_contexts = ["all"]


    def newPaneTab(self):
        reload(hctl_new_tab_menu)
        newPaneTabMenu = hctl_new_tab_menu.newPaneTabMenu()
        newPaneTabMenu.show()
    newPaneTab.interactive_contexts = ["all"]


    def only(self):
        panes = hou.ui.curDesktop().panes()
        for pane in panes:
            if pane != self:
                for paneTab in pane.tabs():
                    paneTab.close()
    only.interactive_contexts = ["all"]


    def resize(self):
        reload(hctl_resize_panel)
        panel = hctl_resize_panel.resizeWidget(self)
        panel.show()
    resize.interactive_contexts = ["all"]


    def setRatioHalf(self):
        self.setSplitFraction(0.5)
    setRatioHalf.interactive_contexts = ["all"]


    def setRatioQuarter(self):
        self.setSplitFraction(0.25)
    setRatioQuarter.interactive_contexts = ["all"]


    def setRatioThird(self):
        self.setSplitFraction(0.333)
    setRatioThird.interactive_contexts = ["all"]


    def toggleMaximized(self):
        self.setIsMaximized(not self.isMaximized())
    toggleMaximized.interactive_contexts = ["all"]


    def togglePaneTabs(self):
        self.showPaneTabs(not self.isShowingPaneTabs())
    togglePaneTabs.interactive_contexts = ["all"]


    def toggleSplitMaximized(self):
        self.setIsSplitMaximized(not self.isSplitMaximized())
    toggleSplitMaximized.interactive_contexts = ["all"]

    # Wrapped functions

    def getSplitFraction(self):
        return self.pane.getSplitFraction()
    getSplitFraction.interactive_contexts = ["none"]


    def setIsMaximized(self, bool):
        self.pane.setIsMaximized(bool)
    setIsMaximized.interactive_contexts = ["all"]


    def setSplitFraction(self, fraction):
        self.pane.setSplitFraction(fraction)
    setSplitFraction.interactive_contexts = ["none"]


    def splitHorizontally(self):
        self.pane.splitHorizontally()
    splitHorizontally.interactive_contexts = ["all"]


    def splitRotate(self):
        self.pane.splitRotate()
    splitRotate.interactive_contexts = ["all"]


    def splitSwap(self):
        self.pane.splitSwap()
    splitSwap.interactive_contexts = ["all"]


    def splitVertically(self):
        self.pane.splitVertically()
    splitVertically.interactive_contexts = ["all"]


    def tabs(self):
        return self.pane.tabs()
    tabs.interactive_contexts = ["none"]



class HctlPaneTab():
    def __init__(self, paneTab):
        self.paneTab = paneTab


    def currentNode(self):
        return self.paneTab.currentNode()


    def path(self):
        if self.hasNetworkControls():
            return self.pwd().path()
        else:
            return "No path"
    path.interactive_contexts = ["none"]


    def pwd(self):
        return self.paneTab.pwd()


    def only(self):
        for paneTab in hou.ui.paneTabs():
            if paneTab != self:
                paneTab.close()
    only.interactive_contexts = ["all"]


    def setPin(self, enable):
        if enable:
            self.paneTab.setCheckState(Qt.Checked)
        else:
            self.paneTab.setCheckState(Qt.Unchecked)
    setPin.interactive_contexts = ["all"]


    def setTypeDetailsView(self):
        self.setType(hou.paneTabType.DetailsView)
    setTypeDetailsView.interactive_contexts = ["all"]


    def setTypeNetworkEditor(self):
        self.setType(hou.paneTabType.NetworkEditor)
    setTypeNetworkEditor.interactive_contexts = ["all"]


    def setTypeParm(self):
        self.setType(hou.paneTabType.Parm)
    setTypeParm.interactive_contexts = ["all"]


    def setTypePythonShell(self):
        self.setType(hou.paneTabType.PythonShell)
    setTypePythonShell.interactive_contexts = ["all"]


    def setTypeSceneViewer(self):
        self.setType(hou.paneTabType.SceneViewer)
    setTypeSceneViewer.interactive_contexts = ["all"]


    def toggleNetworkControls(self):
        if self.hasNetworkControls():
            self.showNetworkControls(not self.isShowingNetworkControls())
    toggleNetworkControls.interactive_contexts = ["all"]


    def togglePin(self):
        self.setPin(not self.isPin())
    togglePin.interactive_contexts = ["all"]

    # Wrapped functions

    def isPin(self):
        return self.paneTab.isPin()
    isPin.interactive_contexts = ["none"]


    def setCheckState(self, bool):
        if bool: self.paneTab.setCheckState()


    def setPin(self, bool):
        self.paneTab.setPin(bool)
    setPin.interactive_contexts = ["none"]


    def type(self):
        return self.paneTab.type()
    type.interactive_contexts = ["none"]



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



class HctlSceneViewer(SceneViewer):
    def __init__(self):
        self.update()

    def update(self):
        self.viewports = self.viewports()
        self.viewport = self.curViewport()
        self.displaySets = self.getDisplaySets()


    def displaySets(self):
        displaySets = []
        for viewport in self.viewports():
            settings = viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
        return(displaySets)
    displaySets.interactive_contexts = ["none"]


    def keycam(self):
        context = self.pwd()
        context_type = context.childTypeCategory().name()
        if context_type == "Object":
            self.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam viewer state in Obj context.")
        elif context_type == "Sop":
            self.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam viewer state in Sop context.")
        elif context_type == "Lop":
            self.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam viewer state in Lop context.")
        else:
            hou.ui.setStatusMessage("No Obj, Sop or Lop context.", hou.severityType.Error)
    keycam.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutDoubleSide(self):
        self.setViewportLayout(hou.geometryViewportLayout.DoubleSide)
    setLayoutDoubleSide.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutDoubleStack(self):
        self.setViewportLayout(hou.geometryViewportLayout.DoubleStack)
    setLayoutDoubleStack.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutQuad(self):
        self.setViewportLayout(hou.geometryViewportLayout.Quad)
    setLayoutQuad.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutQuadBottomSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.QuadBottomSplit)
    setLayoutQuadBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutQuadLeftSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.QuadLeftSplit)
    setLayoutQuadLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutSingle(self):
        self.setViewportLayout(hou.geometryViewportLayout.Single)
    setLayoutSingle.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutTripleBottomSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.TripleBottomSplit)
    setLayoutTripleBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]


    def setLayoutTripleLeftSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.TripleLeftSplit)
    setLayoutTripleLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]


    def toggleLightGeo(self):
        self.setShowLights(not self.showLights())
    toggleLightGeo.interactive_contexts = ["paneTabType.SceneViewer"]


    def toggleBackface(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimBackfaces():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimBackfaces(not visible)
    toggleBackface.interactive_contexts = ["paneTabType.SceneViewer"]


    def toggleDisplayOptionsToolbar(self):
        self.showDisplayOptionsBar(not self.isShowingDisplayOptionsBar())
    toggleDisplayOptionsToolbar.interactive_contexts = ["paneTabType.SceneViewer"]


    def toggleGrid(self):
        refplane = self.referencePlane()
        refplane.setIsVisible(not refplane.isVisible())
    toggleGrid.interactive_contexts = ["paneTabType.SceneViewer"]


    def toggleGroupList(self):
        self.setGroupListVisible(not self.isGroupListVisible())
    toggleGroupList.interactive_contexts = ["paneTabType.SceneViewer"]


    def togglePointMarkers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointMarkers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointMarkers(not visible)
    togglePointMarkers.interactive_contexts = ["paneTabType.SceneViewer"]


    def togglePointNormals(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNormals():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNormals(not visible)
    togglePointNormals.interactive_contexts = ["paneTabType.SceneViewer"]


    def togglePointNumbers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNumbers(not visible)
    togglePointNumbers.interactive_contexts = ["paneTabType.SceneViewer"]


    def togglePrimNormals(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNormals():
                visible = 1
            for displaySet in displaySets:
                displaySet.showPrimNormals(not visible)
    togglePrimNormals.interactive_contexts = ["paneTabType.SceneViewer"]

    def togglePrimNumbers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNumbers(not visible)
    togglePrimNumbers.interactive_contexts = ["paneTabType.SceneViewer"]

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
    toggleToolbars.interactive_contexts = ["paneTabType.SceneViewer"]

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
    toggleVectors.interactive_contexts = ["paneTabType.SceneViewer"]


    def visualizerPanel(self):
        reload(hctl_vis_panel)
        panel = hctl_vis_panel.visualizerMenu()
        panel.show()
    visualizerPanel.interactive_contexts = ["paneTabType.SceneViewer"]


class HctlSession(Desktop):
    def __init__(self):
        self.update()

    def update(self):
        self.desktop = hou.ui.curDesktop()
        self.pane = hou.ui.paneUnderCursor()
        self.panes = self.desktop.panes()
        self.paneTab = hou.ui.paneTabUnderCursor()
        self.paneTabs = self.desktop.paneTabs()
        self.autosave_state = hou.getPreference("autoSave")


    def clearLayout(self, paneTab):
        self.paneOnly(paneTab.pane())
        self.paneTabOnly(paneTab)
        self.update()
    clearLayout.interactive_contexts = ["all"]


    def colorEditor(self):
        hou.ui.selectColor()
    colorEditor.interactive_contexts = ["all"]


    def floatingParameterEditor(self, paneTab):
        if paneTab.type() == hou.paneTabType.NetworkEditor:
            node = paneTab.currentNode()
            hou.ui.showFloatingParameterEditor(node)
        else:
            hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)
    floatingParameterEditor.interactive_contexts = ["all"]


    def hctlPanel(self):
        reload(hctl_panel)
        hctl_panel.Dialog().show()
    hctlPanel.interactive_contexts = ["all"]


    def hideShelf(self, desktop):
        desktop.shelfDock().show(0)
        hou.ui.reloadViewportColorSchemes()
    hideShelf.interactive_contexts = ["none"]


    def layoutA(self, paneTab):
        self.clearLayout(paneTab)
        # pin network editor(?) pane
        # self.panes[0].tabs()[0].setPin(False)
        # Main center split
        self.panes()[0].splitHorizontally()
        self.panes()[0].setSplitFraction(0.6)
        # Left vertical split
        self.panes()[0].splitVertically()
        self.panes()[0].setSplitFraction(0.2)
        # Right vertical split
        self.panes()[1].splitVertically()
        self.panes()[1].setSplitFraction(0.666)
        # Assign
        self.paneTabs()[0].setType(hou.paneTabType.SceneViewer) # Top left
        self.paneTabs()[1].setType(hou.paneTabType.DetailsView) # Bas left
        self.paneTabs()[2].setType(hou.paneTabType.Parm) # Top right
        self.paneTabs()[3].setType(hou.paneTabType.NetworkEditor) # Bas right
        # Hide etc
        # paneTabs[3].setPin(True)
        # desktopToggleMenus()
        self.toggleStowbars()
        self.toggleStowbars()
    layoutA.interactive_contexts = ["all"]


    def layoutB(self, paneTab):
        self.clearLayout(paneTab)
        self.panes()[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[0].splitVertically()
        self.panes()[1].splitVertically()
        # Assign top left
        self.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
    layoutB.interactive_contexts = ["all"]


    def layoutQuad(self, paneTab):
        self.clearLayout(paneTab)
        self.panes()[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[0].splitVertically()
        self.panes()[1].splitVertically()
    layoutQuad.interactive_contexts = ["all"]


    def layoutTriH(self, paneTab):
        self.session.removeEventLoopCallbacks()
        self.clearLayout(paneTab)
        # Make panes
        self.panes()[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[1].splitHorizontally()
        # Make paneTabs
        self.panes()[1].createTab(hou.paneTabType.PythonShell)
        self.panes()[1].tabs()[0].setIsCurrentTab()
        # Set types
        self.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
        self.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
        self.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
        # Ratios
        self.panes()[0].setSplitFraction(0.5)
        hou.session.lastPane = hou.ui.paneUnderCursor()
        hou.ui.addEventLoopCallback(self.layoutTriHCallback)
    layoutTriH.interactive_contexts = ["all"]


    def layoutTriHCallback():
        panes = hou.ui.panes()
        pane = hou.ui.paneUnderCursor()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[1]):
                pane.setSplitFraction(0.6)
            elif str(pane) == str(panes[2]):
                pane.setSplitFraction(0.3)
        return True


    def layoutTriV(self, paneTab):
        self.session.removeEventLoopCallbacks()
        self.clearLayout(paneTab)
        # Make panes
        self.panes()[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[1].splitVertically()
        # Make pane tabs
        self.panes()[1].createTab(hou.paneTabType.PythonShell)
        self.panes()[1].tabs()[0].setIsCurrentTab()
        # Set types
        self.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
        self.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
        self.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
        # Set ratios
        self.panes()[0].setSplitFraction(0.66)
        # Ok
        hou.session.lastPane = hou.ui.paneUnderCursor()
        hou.ui.addEventLoopCallback(self.layoutTriVCallback)
    layoutTriV.interactive_contexts = ["all"]


    def layoutTriVCallback():
        panes = hou.ui.panes()
        pane = hou.ui.paneUnderCursor()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[1]):
                pane.setSplitFraction(0.33)
            elif str(pane) == str(panes[2]):
                pane.setSplitFraction(0.66)
        return True


    def networkEditors(self):
        editors = []
        for paneTab in self.paneTabs:
            if paneTab.type() == hou.paneTabType.NetworkEditor:
                editors.append(paneTab)
        return editors
    networkEditors.interactive_contexts = ["none"]


    def openFile(self):
        hou.ui.selectFile()
    openFile.interactive_contexts = ["all"]


    def paneTabs(self):
        paneTabs = []
        for pane in self.panes():
            for paneTab in pane.tabs():
                paneTabs.append(paneTab)
        return paneTabs
    paneTabs.interactive_contexts = ["none"]


    def reloadColorSchemes(self):
        hou.ui.reloadColorScheme()
    reloadColorSchemes.interactive_contexts = ["all"]


    def reloadKeyBindings(self):
        reload(hctl_bindings)
        hctl_bindings.updateBindings()
    reloadKeyBindings.interactive_contexts = ["all"]


    def reloadKeycam(self):
        hou.ui.reloadViewerState("keycam")
    reloadKeycam.interactive_contexts = ["all"]


    def removeEventLoopCallbacks(self):
        callbacks = hou.ui.eventLoopCallbacks()
        for callback in callbacks:
            hou.ui.removeEventLoopCallback(callback)
    removeEventLoopCallbacks.interactive_contexts = ["all"]


    def restart(self):
        print("This function does nothing")
    restart.interactive_contexts = ["none"]


    def sceneViewers(self):
        paneTabs = self.paneTabs()
        sceneViewers = [paneTab for paneTab in paneTabs if paneTab.type() == hou.paneTabType.SceneViewer]
        return sceneViewers
    sceneViewers.interactive_contexts = ["none"]


    def showShelf(self):
        self.shelfDock().show(1)
    showShelf.interactive_contexts = ["none"]


    def toggleMainMenuBar(self):
        if hou.getPreference("showmenu.val") == "1":
            hou.setPreference("showmenu.val", "0")
        else:
            hou.setPreference("showmenu.val", "1")
    toggleMainMenuBar.interactive_contexts = ["all"]


    def toggleMenus(self):
        visible = 0
        panes = self.panes()
        paneTabs = self.paneTabs()
        editors = self.networkEditors()
        sceneViewers = self.sceneViewers()
        # Main menu
        if hou.getPreference("showmenu.val") == "1":
            visible = 1
        # Network editor menu
        elif any(editor.getPref("showmenu") == "1" for editor in editors):
            visible = 1
        # Network controls
        elif any(paneTab.isShowingNetworkControls() for paneTab in paneTabs):
            visible = 1
        # Scene viewer toolbars (top, right, left)
        elif any(sceneViewer.isShowingOperationBar() for sceneViewer in sceneViewers):
            visible = 1
        elif any(sceneViewer.isShowingDisplayOptionsBar() for sceneViewer in sceneViewers):
            visible = 1
        elif any(sceneViewer.isShowingSelectionBar() for sceneViewer in sceneViewers):
            visible = 1
        # Panetabs
        elif any(pane.isShowingPaneTabs() for pane in panes):
            visible = 1
        #
        # Set state
        hou.setPreference("showmenu.val", str(not visible))
        for editor in editors:
            editor.setPref("showmenu", str(not visible))
        for paneTab in paneTabs:
            paneTab.showNetworkControls(not visible)
        for pane in panes:
            pane.showPaneTabs(not visible)
        for viewer in sceneViewers:
            viewer.showOperationBar(not visible)
            viewer.showDisplayOptionsBar(not visible)
            viewer.showSelectionBar(not visible)
        hou.ui.setHideAllMinimizedStowbars(visible)
    toggleMenus.interactive_contexts = ["all"]


    def toggleNetworkControls(self):
        visible = 0
        paneTabs = self.paneTabs()
        for paneTab in paneTabs:
            if paneTab.isShowingNetworkControls():
                visible = 1
        for paneTab in paneTabs:
            paneTab.showNetworkControls(not visible)
    toggleNetworkControls.interactive_contexts = ["all"]


    def togglePaneTabs(self):
        visible = 0
        panes = self.panes()
        for pane in panes:
            if pane.isShowingPaneTabs():
                visible = 1
        for pane in panes:
            pane.showPaneTabs(not visible)
    togglePaneTabs.interactive_contexts = ["all"]


    def toggleStowbars(self):
        hidden = hou.ui.hideAllMinimizedStowbars()
        hou.ui.setHideAllMinimizedStowbars(not hidden)
    toggleStowbars.interactive_contexts = ["all"]


    def triggerUpdate(self):
        hou.ui.triggerUpdate()
    triggerUpdate.interactive_contexts = ["all"]


    def toggleAutoSave(self):
        if hou.getPreference("autoSave"):
            hou.setPreference("autoSave", "0")
        else:
            hou.setPreference("autoSave", "1")
    toggleAutoSave.interactive_contexts = ["none"]


    def updateMainMenuBar(self):
        hou.ui.updateMainMenuBar()
    updateMainMenuBar.interactive_contexts = ["all"]


    def updateModeAuto(self):
        hou.setUpdateMode(hou.updateMode.AutoUpdate)
    updateModeAuto.interactive_contexts = ["all"]


    def updateModeManual(self):
        hou.setUpdateMode(hou.updateMode.Manual)
    updateModeManual.interactive_contexts = ["all"]


    def viewports(self):
        viewports = []
        sceneViewers = self.sceneViewers
        for sceneViewer in sceneViewers:
            for viewport in sceneViewer.viewports():
                viewports.append(viewport)
        return(viewports)
    viewports.interactive_contexts = ["none"]



class HctlViewport(GeometryViewport):
    def __init__(self):
        pass
        # self.viewport = viewport

    def update():
        pass


    def visualizers(self):
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr
