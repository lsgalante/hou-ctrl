import hou
from hou import Desktop, Pane, PaneTab, SceneViewer, GeometryViewport
from importlib import reload
import hctl_panel
import hctl_vis_panel
# import hctl_new_tab_panel
import hctl_resize_panel
import hctl_bindings


## Always available functions



## Classes

class HctlNetworkEditor(PaneTab):
    def __init__(self):
        pass
    __init__.interactive: False

    def update(self):
        self.context = self.pwd()
        self.node = self.currentNode()
    update.interactive: False


    def addNetworkBox(self):
        self.update()
        networkBox = self.pwd().createNetworkBox()
        networkBox.setPosition(self.currentNode().position())
    addNetworkBox.interactive = True


    def addStickyNote(self):
        stickyNote = self.pwd().createStickyNote()
        cursor_pos = self.cursorPosition()
        stickyNote.setPosition(cursor_pos)
        color = hou.Color(0.71, 0.784, 1.0)
        stickyNote.setColor(color)
    addStickyNote.interactive = True


    def connectNode(self):
        return
        # choices = ("a", "b", "c")
        # popup = hou.ui.selectFromList(choices)
    connectNode.interactive = True


    def cycleGrid(self):
        mode = int(self.getPref("gridmode"))
        mode = (mode + 1) % 3
        self.setPref("gridmode", mode)
    cycleGrid.interactive = True


    def deselectAll(self):
        self.currentNode().setSelected(False)
    deselectAll.interactive = True


    def renameNode(self):
        node = self.currentNode()
        name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
        if name[0] == 0:
            node.setName(name[1])
    renameNode.interactive = True


    def rotateNodeInputs(self):
        return
        # node = self.currentNode()
        # connectors = node.inputConnectors()
    rotateNodeInputs.interactive = True


    def selectDisplayNode(self):
        self.pwd().setCurrent(True, True)
    selectDisplayNode.interactive = True


    def toggleDimUnusedNodes(self):
        dim = int(self.getPref("dimunusednodes"))
        self.setPref("dimunusednodes", str(not dim))
    toggleDimUnusedNodes.interactive = True


    def toggleLocating(self):
        self.setLocatingEnabled(not self.locatingEnabled())
    toggleLocating.interactive = True


    def toggleMenu(self):
        visible = int(self.getPref("showmenu"))
        self.setPref("showmenu", str(not visible))
    toggleMenu.interactive = True


    def toggleGridPoints(self):
        visible = int(self.getPref("gridmode"))
        self.setPref("gridmode", str(not visible))
    toggleGridPoints.interactive = True



class HctlPane(hou.Pane):
    def __init__(self, pane):
        self.pane = pane
    __init__.interactive = False


    def close(self):
        for tab in self.tabs():
            tab.close()
    close.interactive = True


    def contract(self):
        fraction = self.getSplitFraction()
        fraction = round(fraction, 3) + 0.1
        hou.ui.setStatusMessage("Pane fraction: " + str(fraction))
        self.setSplitFraction(fraction)
    contract.interactive = True


    def expand(self):
        fraction = self.getSplitFraction()
        fraction = round(fraction, 3) - 0.1
        message = "Pane fraction: " + str(fraction)
        hou.ui.setStatusMessage(message)
        self.setSplitFraction(fraction)
    expand.interactive = True


    def getSplitFraction(self):
        return self.pane.getSplitFraction()
    getSplitFraction.interactive = False


    def isShowingTabs(self):
        return self.pane.isShowingPaneTabs()
    isShowingTabs.interactive = 0


    def newTab(self):
        reload(hctl_new_tab_menu)
        newPaneTabMenu = hctl_new_tab_menu.newPaneTabMenu()
        newPaneTabMenu.show()
    newTab.interactive = True


    def only(self):
        panes = hou.ui.curDesktop().panes()
        for pane in panes:
            if pane != self:
                for paneTab in pane.tabs():
                    paneTab.close()
    only.interactive = True


    def resize(self):
        reload(hctl_resize_panel)
        panel = hctl_resize_panel.resizeWidget(self)
        panel.show()
    resize.interactive = True


    def setIsMaximized(self, bool):
        self.pane.setIsMaximized(bool)
    setIsMaximized.interactive = False


    def setRatioHalf(self):
        self.setSplitFraction(0.5)
    setRatioHalf.interactive = True


    def setRatioQuarter(self):
        self.setSplitFraction(0.25)
    setRatioQuarter.interactive = True


    def setRatioThird(self):
        self.setSplitFraction(0.333)
    setRatioThird.interactive = True


    def setSplitFraction(self, fraction):
        self.pane.setSplitFraction(fraction)
    setSplitFraction.interactive = False


    def showTabs(self, bool):
        self.pane.showPaneTabs(bool)


    def splitHorizontally(self):
        self.pane.splitHorizontally()
    splitHorizontally.interactive = True


    def splitRotate(self):
        self.pane.splitRotate()
    splitRotate.interactive = True


    def splitSwap(self):
        self.pane.splitSwap()
    splitSwap.interactive = True


    def splitVertically(self):
        self.pane.splitVertically()
    splitVertically.interactive = True


    def tabs(self):
        return self.pane.tabs()
    tabs.interactive = False


    def toggleMaximized(self):
        self.setIsMaximized(not self.isMaximized())
    toggleMaximized.interactive = True


    def toggleTabs(self):
        self.showTabs(not self.isShowingTabs())
    toggleTabs.interactive = True


    def toggleSplitMaximized(self):
        self.setIsSplitMaximized(not self.isSplitMaximized())
    toggleSplitMaximized.interactive = True



class HctlPaneTab():
    def __init__(self, paneTab):
        self.paneTab = paneTab


    def close(self):
        self.paneTab.close()
    close.interactive = True


    def currentNode(self):
        return self.paneTab.currentNode()
    currentNode.interactive = False


    def hasNetworkControls(self):
        return self.paneTab.hasNetworkControls()
    hasNetworkControls.interactive = False


    def isPin(self):
        return self.paneTab.isPin()
    isPin.interactive = False


    def isShowingNetworkControls(self):
        return self.paneTab.isShowingNetworkControls()
    isShowingNetworkControls.interactive = False


    def only(self):
        for paneTab in hou.ui.paneTabs():
            if paneTab != self:
                paneTab.close()
    only.interactive = True


    def path(self):
        if self.hasNetworkControls():
            return self.pwd().path()
        else:
            return "No path"
    path.interactive = False


    def pwd(self):
        if self.paneTab.hasNetworkControls:
            return self.paneTab.pwd()
        else:
            return "No path"
    pwd.interactive = False


    def setCheckState(self, bool):
        if bool: self.paneTab.setCheckState()
    setCheckState.interactive = False


    def setPin(self, bool):
        self.paneTab.setPin(bool)
    setPin.interactive = False


    def setTypeDetailsView(self):
        self.setType(hou.paneTabType.DetailsView)
    setTypeDetailsView.interactive = True


    def setTypeNetworkEditor(self):
        self.setType(hou.paneTabType.NetworkEditor)
    setTypeNetworkEditor.interactive = True


    def setTypeParm(self):
        self.setType(hou.paneTabType.Parm)
    setTypeParm.interactive = True


    def setTypePythonShell(self):
        self.setType(hou.paneTabType.PythonShell)
    setTypePythonShell.interactive = True


    def setTypeSceneViewer(self):
        self.setType(hou.paneTabType.SceneViewer)
    setTypeSceneViewer.interactive = True


    def showNetworkControls(self, bool):
        self.paneTab.showNetworkControls(bool)
    showNetworkControls.interactive = False


    def tabs(self):
        return self.paneTab.tabs()
    tabs.interactive = False


    def toggleNetworkControls(self):
        if self.hasNetworkControls():
            self.showNetworkControls(not self.isShowingNetworkControls())
    toggleNetworkControls.interactive = True


    def togglePin(self):
        self.setPin(not self.isPin())
    togglePin.interactive = True


    def type(self):
        return self.paneTab.type()
    type.interactive = False



class Printer():
    def __init__(self):
        self.message = ""
    __init__.interactive = False


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
    layout.interactive = True



class HctlSceneViewer():
    def __init__(self, sceneViewer):
        self.sceneViewer = sceneViewer
        self.update()
    __init__.interactive = False


    def update(self):
        self.viewports = self.sceneViewer.viewports()
        self.viewport = self.sceneViewer.curViewport()
    update.interactive = False


    def displaySets(self):
        displaySets = []
        for viewport in self.viewports():
            settings = viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
        return(displaySets)
    displaySets.interactive = False


    def isShowingDisplayOptionsBar(self):
        return self.sceneViewer.isShowingDisplayOptionsBar()
    isShowingDisplayOptionsBar.interactive = False


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
    keycam.interactive = True


    def setLayoutDoubleSide(self):
        self.setViewportLayout(hou.geometryViewportLayout.DoubleSide)
    setLayoutDoubleSide.interactive = True


    def setLayoutDoubleStack(self):
        self.setViewportLayout(hou.geometryViewportLayout.DoubleStack)
    setLayoutDoubleStack.interactive = True


    def setLayoutQuad(self):
        self.setViewportLayout(hou.geometryViewportLayout.Quad)
    setLayoutQuad.interactive = True


    def setLayoutQuadBottomSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.QuadBottomSplit)
    setLayoutQuadBottomSplit.interactive = True


    def setLayoutQuadLeftSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.QuadLeftSplit)
    setLayoutQuadLeftSplit.interactive = True


    def setLayoutSingle(self):
        self.setViewportLayout(hou.geometryViewportLayout.Single)
    setLayoutSingle.interactive = True


    def setLayoutTripleBottomSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.TripleBottomSplit)
    setLayoutTripleBottomSplit.interactive = True


    def setLayoutTripleLeftSplit(self):
        self.setViewportLayout(hou.geometryViewportLayout.TripleLeftSplit)
    setLayoutTripleLeftSplit.interactive = True


    def showDisplayOptionsBar(self, bool):
        self.sceneViewer.showDisplayOptionsBar(bool)
    showDisplayOptionsBar.interactive = False


    def toggleLightGeo(self):
        self.setShowLights(not self.showLights())
    toggleLightGeo.interactive = True


    def toggleBackface(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimBackfaces():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimBackfaces(not visible)
    toggleBackface.interactive = True


    def toggleDisplayOptionsToolbar(self):
        self.showDisplayOptionsBar(not self.isShowingDisplayOptionsBar())
    toggleDisplayOptionsToolbar.interactive = True


    def toggleGrid(self):
        refplane = self.referencePlane()
        refplane.setIsVisible(not refplane.isVisible())
    toggleGrid.interactive = True


    def toggleGroupList(self):
        self.setGroupListVisible(not self.isGroupListVisible())
    toggleGroupList.interactive = True


    def togglePointMarkers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointMarkers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointMarkers(not visible)
    togglePointMarkers.interactive = True


    def togglePointNormals(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNormals():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNormals(not visible)
    togglePointNormals.interactive = True


    def togglePointNumbers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPointNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPointNumbers(not visible)
    togglePointNumbers.interactive = True


    def togglePrimNormals(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNormals():
                visible = 1
            for displaySet in displaySets:
                displaySet.showPrimNormals(not visible)
    togglePrimNormals.interactive = True


    def togglePrimNumbers(self):
        visible = 0
        displaySets = self.displaySets()
        for displaySet in displaySets:
            if displaySet.isShowingPrimNumbers():
                visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNumbers(not visible)
    togglePrimNumbers.interactive = True


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
    toggleToolbars.interactive = True


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
    toggleVectors.interactive = True


    def visualizerPanel(self):
        reload(hctl_vis_panel)
        panel = hctl_vis_panel.visualizerMenu()
        panel.show()
    visualizerPanel.interactive = True



class HctlSession(Desktop):
    def __init__(self):
        pass
        # self.update()


    # def update(self):
        # self.desktop = hou.ui.curDesktop()
        # self.pane = hou.ui.paneUnderCursor()
        # self.panes = self.desktop.panes()
        # self.tab = hou.ui.paneTabUnderCursor()
        # self.tabs = self.desktop.paneTabs()
        # self.node = self.tab.currentNode()
        # self.autosave_state = hou.getPreference("autoSave")
    # update.interactive = False


    def autosaveState(self):
        return hou.getPreference("autoSave")
    autosaveState.interactive = False


    def clearLayout(self):
        tabs = self.tabs()
        for tab in tabs:
            if tab != tabs[0]:
                tab.close()
        # self.paneOnly(paneTab.pane())
        # self.paneTabOnly(paneTab)
        # self.update()
    clearLayout.interactive = True


    def colorEditor(self):
        hou.ui.selectColor()
    colorEditor.interactive = True


    def desktop(self):
        return hou.ui.curDesktop()
    desktop.interactive = False


    def floatingParameterEditor(self):
        tab = self.tab()
        if tab.type() == hou.paneTabType.NetworkEditor: hou.ui.showFloatingParameterEditor(self.node())
        else: hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)
    floatingParameterEditor.interactive = True


    def hctlPanel(self):
        reload(hctl_panel)
        hctl_panel.Dialog().show()
    hctlPanel.interactive = True


    def hideShelf(self):
        self.desktop().shelfDock().show(0)
    hideShelf.interactive = True


    def layout(self):
        desktop = self.desktop()
        panes = desktop.panes()
        lefts = []
        tops = []
        for pane in panes:
            geo = pane.qtScreenGeometry()
            lefts.append(geo.left())
            tops.append(geo.top())
        print(lefts)
        print(tops)
    layout.interactive = False


    def networkEditors(self):
        editors = []
        for tab in self.tabs():
            if tab.type() == hou.paneTabType.NetworkEditor:
                editors.append(tab)
        return editors
    networkEditors.interactive = False


    def node(self):
        return self.tab().currentNode()
    node.interactive = False


    def openFile(self):
        hou.ui.selectFile()
    openFile.interactive = True


    def pane(self):
        return hou.ui.paneUnderCursor()


    def panes(self):
        return self.desktop().panes()
    panes.interactive = False


    def reloadColorSchemes(self):
        hou.ui.reloadColorScheme()
        hou.ui.reloadViewportColorSchemes()
    reloadColorSchemes.interactive = True


    def reloadKeyBindings(self):
        reload(hctl_bindings)
        hctl_bindings.updateBindings()
    reloadKeyBindings.interactive = True


    def reloadKeycam(self):
        hou.ui.reloadViewerState("keycam")
    reloadKeycam.interactive = True


    def removeEventLoopCallbacks(self):
        callbacks = hou.ui.eventLoopCallbacks()
        for callback in callbacks:
            hou.ui.removeEventLoopCallback(callback)
    removeEventLoopCallbacks.interactive = True


    def restart(self):
        print("This function does nothing")
    restart.interactive = True


    def sceneViewers(self):
        sceneViewers = [tab for tab in self.tabs() if tab.type() == hou.paneTabType.SceneViewer]
        return sceneViewers
    sceneViewers.interactive = False


    def setLayoutQuad(self):
        self.clearLayout()
        self.tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[0].splitVertically()
        self.panes()[1].splitVertically()
    setLayoutQuad.interactive = True


    def setLayoutRamp(self):
        self.removeEventLoopCallbacks()
        self.clearLayout()
        self.panes()[0].splitVertically()
        self.tabs()[1].setType(hou.paneTabType.Parm)
        self.panes()[1].setSplitRatio(0.3)
        self.panes()[1].createTab()
    setLayoutRamp.interactive = True


    def setLayoutTriH(self):
        self.removeEventLoopCallbacks()
        self.clearLayout()
        # Make panes
        self.tabs()[0].setType(hou.paneTabType.PythonShell)
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
        hou.session.lastPane = self.pane()
        hou.ui.addEventLoopCallback(self.triHCallback)
    setLayoutTriH.interactive = True


    def triHCallback():
        panes = hou.ui.panes()
        pane = hou.ui.paneUnderCursor()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[1]):
                pane.setSplitFraction(0.6)
            elif str(pane) == str(panes[2]):
                pane.setSplitFraction(0.3)
        return True
    triHCallback.interactive = False


    def setLayoutTriV(self):
        # Remove other callbacks
        self.removeEventLoopCallbacks()
        # Reset pane layout
        self.clearLayout()
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
        hou.ui.addEventLoopCallback(self.triVCallback)
    setLayoutTriV.interactive = True


    def triVCallback(self):
        panes = hou.ui.panes()
        pane = hou.ui.paneUnderCursor()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[1]):
                pane.setSplitFraction(0.33)
            elif str(pane) == str(panes[2]):
                pane.setSplitFraction(0.66)
        return True
    triVCallback.interactive = False


    def setUpdateModeAuto(self):
        hou.setUpdateMode(hou.updateMode.AutoUpdate)
    setUpdateModeAuto.interactive = True


    def setUpdateModeManual(self):
        hou.setUpdateMode(hou.updateMode.Manual)
    setUpdateModeManual.interactive = True


    def showShelf(self):
        self.shelfDock().show(1)
    showShelf.interactive = True


    def tab(self):
        return hou.ui.paneTabUnderCursor()
    tab.interactive = False


    def tabs(self):
        return hou.ui.curDesktop().paneTabs()
    tabs.interactive = False


    def toggleMainMenuBar(self):
        if hou.getPreference("showmenu.val") == "1":
            hou.setPreference("showmenu.val", "0")
        else:
            hou.setPreference("showmenu.val", "1")
    toggleMainMenuBar.interactive = True


    def toggleMenus(self):
        visible = 0
        panes = self.panes()
        tabs = self.tabs()
        editors = self.networkEditors()
        sceneViewers = self.sceneViewers()
        # Main menu
        if hou.getPreference("showmenu.val") == "1":
            visible = 1
        # Network editor menu
        elif any(editor.getPref("showmenu") == "1" for editor in editors):
            visible = 1
        # Network controls
        elif any(tab.isShowingNetworkControls() for tab in tabs):
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

        # Set state
        hou.setPreference("showmenu.val", str(not visible))
        for editor in editors:
            editor.setPref("showmenu", str(not visible))
        for tab in tabs:
            tab.showNetworkControls(not visible)
        for pane in panes:
            pane.showPaneTabs(not visible)
        for viewer in sceneViewers:
            viewer.showOperationBar(not visible)
            viewer.showDisplayOptionsBar(not visible)
            viewer.showSelectionBar(not visible)
        hou.ui.setHideAllMinimizedStowbars(visible)
        hou.ui.setHideAllMinimizedStowbars(visible)
    toggleMenus.interactive = True


    def toggleNetworkControls(self):
        visible = 0
        paneTabs = self.paneTabs()
        for paneTab in paneTabs:
            if paneTab.isShowingNetworkControls():
                visible = 1
        for paneTab in paneTabs:
            paneTab.showNetworkControls(not visible)
    toggleNetworkControls.interactive = True


    def togglePaneTabs(self):
        visible = 0
        panes = self.panes()
        for pane in panes:
            if pane.isShowingPaneTabs():
                visible = 1
        for pane in panes:
            pane.showPaneTabs(not visible)
    togglePaneTabs.interactive = True


    def toggleStowbars(self):
        hidden = hou.ui.hideAllMinimizedStowbars()
        hou.ui.setHideAllMinimizedStowbars(not hidden)
    toggleStowbars.interactive = True


    def triggerUpdate(self):
        hou.ui.triggerUpdate()
    triggerUpdate.interactive = True


    def toggleAutoSave(self):
        if hou.getPreference("autoSave"):
            hou.setPreference("autoSave", "0")
        else:
            hou.setPreference("autoSave", "1")
    toggleAutoSave.interactive = True


    def updateMainMenuBar(self):
        hou.ui.updateMainMenuBar()
    updateMainMenuBar.interactive = True


    def viewports(self):
        viewports = []
        sceneViewers = self.sceneViewers
        for sceneViewer in sceneViewers:
            for viewport in sceneViewer.viewports():
                viewports.append(viewport)
        return(viewports)
    viewports.interactive = False



class HctlViewport(GeometryViewport):
    def __init__(self):
        pass
        # self.viewport = viewport
    __init__.interactive = False


    def update():
        pass
    update.interactive = False


    def visualizers(self):
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr
    visualizers.interactive = False
