import hou
from importlib import reload
import hctl
import hctl_vis_menu
import hctl_new_tab_menu
import hctl_resize
import hctl_bindings


#         #
# Desktop #

def desktopEvalColorSchemes():
    hou.ui.reloadColorScheme()
desktopEvalColorSchemes.interactive_contexts = ["all"]


def desktopGetNetworkEditors():
    tabs = hou.ui.paneTabs()
    networkEditors = [tab for tab in tabs if tab.type() == hou.paneTabType.NetworkEditor]
    return networkEditors
desktopGetNetworkEditors.interactive_contexts = ["none"]


def desktopGetSceneViewers():
    tabs  = hou.ui.paneTabs()
    sceneViewers = [tab for tab in tabs if tab.type() == hou.paneTabType.SceneViewer]
    return sceneViewers
desktopGetSceneViewers.interactive_contexts = ["none"]


def desktopGetViewports():
    viewports = []
    sceneViewers = getSceneViewers()
    for sceneViewer in sceneViewers:
        for viewport in sceneViewer.viewports():
            viewports.append(viewport)
desktopGetViewports.interactive_contexts = ["none"]


def desktopSceneSetA():
    paneOnly()
    paneTabOnly()
    panes = hou.ui.curDesktop().panes()
    # panes[0].tabs()[0].setPin(False)
    panes[0].splitHorizontally()
    panes = hou.ui.curDesktop().panes()
    panes[0].setSplitFraction(0.6)
    panes[0].splitVertically()
    panes[0].setSplitFraction(0.2)
    panes[1].splitVertically()
    panes[1].setSplitFraction(0.666)

    paneTabs = [pane.tabs()[0] for pane in hou.ui.curDesktop().panes()]
    paneTabs[0].setType(hou.paneTabType.SceneViewer)
    paneTabs[1].setType(hou.paneTabType.DetailsView)
    paneTabs[2].setType(hou.paneTabType.Parm)
    paneTabs[3].setType(hou.paneTabType.NetworkEditor)
    # paneTabs[3].setPin(True)
    desktopToggleMenus()
    desktopToggleStowbars()
    desktopToggleStowbars()
desktopSceneSetA.interactive_contexts = ["all"]


def desktopShelfHide():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(0)
    hou.ui.reloadViewportColorSchemes()
desktopShelfHide.interactive_contexts = ["none"]


def desktopShelfShow():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(1)
desktopShelfShow.interactive_contexts = ["none"]


def desktopToggleMainMenuBar():
    if hou.getPreference("showmenu.val") == "1":
        hou.setPreference("showmenu.val", "0")
    else:
        hou.setPreference("showmenu.val", "1")
desktopToggleMainMenuBar.interactive_contexts = ["all"]


def desktopToggleMenus():
    is_visible = 0
    # gather contexts
    networkEditors = desktopGetNetworkEditors()
    panes = hou.ui.curDesktop().panes()
    sceneViewers = desktopGetSceneViewers()
    tabs = hou.ui.paneTabs()
    # main menu
    if hou.getPreference("showmenu.val") == "1":
        is_visible = 1
    # network editor menu
    elif any(networkEditor.getPref("showmenu") == "1" for networkEditor in networkEditors):
        is_visible = 1
    # network controls
    elif any(tab.isShowingNetworkControls() for tab in tabs):
        is_visible = 1
    # scene viewer toolbars (top, right, left)
    elif any(sceneViewer.isShowingOperationBar() for sceneViewer in sceneViewers):
        is_visible = 1
    elif any(sceneViewer.isShowingDisplayOptionsBar() for sceneViewer in sceneViewers):
        is_visible = 1
    elif any(sceneViewer.isShowingSelectionBar() for sceneViewer in sceneViewers):
        is_visible = 1
    # tabs
    elif any(pane.isShowingPaneTabs() for pane in panes):
        is_visible = 1
    # hide all
    if is_visible:
        hou.setPreference("showmenu.val", "0")
        for networkEditor in networkEditors:
            networkEditor.setPref("showmenu", "0")
        for tab in tabs:
            tab.showNetworkControls(0)
        for pane in panes:
            pane.showPaneTabs(0)
        for sceneViewer in sceneViewers:
            sceneViewer.showOperationBar(0)
            sceneViewer.showDisplayOptionsBar(0)
            sceneViewer.showSelectionBar(0)
        hou.ui.setHideAllMinimizedStowbars(1)
    # show all
    else:
        hou.setPreference("showmenu.val", "1")
        for networkEditor in networkEditors:
            networkEditor.setPref("showment", "1")
        for tab in tabs:
            tab.showNetworkControls(1)
        for pane in panes:
            pane.showPaneTabs(1)
        for sceneViewer in sceneViewers:
            sceneViewer.showOperationBar(1)
            sceneViewer.showDisplayOptionsBar(1)
            sceneViewer.showSelectionBar(1)
        hou.ui.setHideAllMinimizedStowbars(0)
desktopToggleMenus.interactive_contexts = ["all"]


def desktopToggleHctl():
    reload(hctl)
    hctl.dialog().show()
desktopToggleHctl.interactive_contexts = ["all"]


def desktopToggleNetworkControls():
    is_visible = 0
    tabs = hou.ui.paneTabs()
    for tab in tabs:
        if tab.isShowingNetworkControls():
            is_visible = 1
    for tab in tabs:
        tab.showNetworkControls((is_visible + 1) % 2)
desktopToggleNetworkControls.interactive_contexts = ["all"]


def desktopTogglePaneTabs():
    panes = hou.ui.curDesktop().panes()
    is_visible = 0
    for pane in panes:
        if pane.isShowingPaneTabs():
            is_visible = 1
    for pane in panes:
        pane.showPaneTabs(not is_visible)
desktopTogglePaneTabs.interactive_contexts = ["all"]


def desktopToggleStowbars():
    is_hidden = hou.ui.hideAllMinimizedStowbars()
    hou.ui.setHideAllMinimizedStowbars(not is_hidden)
desktopToggleStowbars.interactive_contexts = ["all"]


def desktopUpdateMainMenuBar():
    hou.ui.updateMainMenuBar()
desktopUpdateMainMenuBar.interactive_contexts = ["all"]


## Network Editor


def networkEditorAddNetworkBox():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        context = tab.pwd()
        node = tab.currentNode()
        networkBox = context.createNetworkBox()
        networkBox.setPosition(node.position())
    else:
        hou.ui.setStatusMessage("Network editor not focused", hou.severityType.Error)
networkEditorAddNetworkBox.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorAddStickyNote():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        context = tab.pwd()
        stickyNote = context.createStickyNote()
        cursor_pos =  tab.cursorPosition()
        stickyNote.setPosition(cursor_pos)
        color = hou.Color(0.71, 0.784, 1.0)
        stickyNote.setColor(color)
    else:
        hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)
networkEditorAddStickyNote.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorConnectNodeTo():
    node = networkEditorGetCurrentNode()
    choices = ("a", "b", "c")
    popup = hou.ui.selectFromList(choices)
networkEditorConnectNodeTo.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorDeselectAllNodes():
    node = networkEditorGetCurrentNode()
    node.setSelected(False)
networkEditorDeselectAllNodes.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorGetCurrentNode():
    tabs = hou.ui.paneTabs()
    tabs = [tab for tab in tabs if tab.type() == hou.paneTabType.NetworkEditor]
    node = tabs[0].currentNode()    
    return node
networkEditorGetCurrentNode.interactive_contexts = ["none"]


def networkEditorGetDisplayNode():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        context = tab.pwd()
        displayNode = context.displayNode()
        return displayNode
    else:
        hou.ui.setStatusMessage("Not a network editor", hou.severityTyoe.Error)
networkEditorGetDisplayNode.interactive_contexts = ["none"]


def networkEditorRenameNode():
    node = networkEditorGetCurrentNode()
    name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
    if name[0] == 0:
        node.setName(name[1])
networkEditorRenameNode.interactive_contexts = ["paneTabType.NetworkEditor", "paneTabType.Parm"]


def networkEditorRotateNodeInputs():
    node = networkEditorGetCurrentNode()
    connectors = node.inputConnectors()
networkEditorRotateNodeInputs.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorSelectDisplayNode():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        displayNode = networkEditorGetDisplayNode()
        displayNode.setCurrent(True, True)
    else:
        hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)
networkEditorSelectDisplayNode.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorToggleDimUnusedNodes():
    is_dim = "0"
    networkEditors = getNetworkEditors()
    for networkEditor in networkEditors:
        if networkEditor.getPref("dimunusednodes") == "1":
            is_dim = "1"
    for networkEditor in networkEditors:
        if is_dim == "0":
            networkEditor.setPref("dimunusednodes", "1") 
        else:
            networkEditor.setPref("dimunusednodes", "0")
networkEditorToggleDimUnusedNodes.interactive_contexts = ["all"]


def networkEditorToggleGridLines():
    is_visible = "0"
    networkEditors = desktopGetNetworkEditors()
    for networkEditor in networkEditors:
        if networkEditor.getPref("gridmode") == "1":
            is_visible = "1"
    for networkEditor in networkEditors:
        if networkEditor.getPref("gridmode") == "0":
            networkEditor.setPref("gridmode", "1")
        else:
            networkEditor.setPref("gridmode", "0")
networkEditorToggleGridLines.interactive_contexts = ["all"]


def networkEditorToggleLocating():
    is_locating = 0
    networkEditors = getNetworkEditors()
    for networkEditor in networkEditors:
        if networkEditor.locatingEnabled():
            is_locating = 1
    for networkEditor in networkEditors:
        networkEditor.setLocatingEnabled((is_locating + 1) % 2)
networkEditorToggleLocating.interactive_contexts = ["all"]


def networkEditorToggleMenu():
    is_visible = 0
    networkEditors = desktopGetNetworkEditors()
    for networkEditor in networkEditors:
        if networkEditor.getPref("showmenu") == "1":
            is_visible = 1
    for networkEditor in networkEditors:
        if is_visible:
            networkEditor.setPref("showmenu", "0")
        else:
            networkEditor.setPref("showmenu", "1")
networkEditorToggleMenu.interactive_contexts = ["all"]


def networkEditorToggleGridPoints():
    is_visible = "0"
    networkEditors = getNetworkEditors()
    for networkEditor in networkEditors:
        if networkEditor.getPref("gridmode") == "1":
            is_visible = "1"
    for networkEditor in networkEditors:
        if is_visible == "0":
            networkEditor.setPref("gridmode", "1")
        else:
            networkEditor.setPref("gridmode", "0")
networkEditorToggleMenu.interactive_contexts = ["all"]

    
## Open

def openColorEditor():
    hou.ui.selectColor()
openColorEditor.interactive_contexts = ["all"]


def openFloatingParameterEditor():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        node = tab.currentNode()
        hou.ui.showFloatingParameterEditor(node)
    else:
        hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error) 
openFloatingParameterEditor.interactive_contexts = ["all"]


def openHotkeyEditor():
    print("open hotkey editor")
openHotkeyEditor.interactive_contexts = ["none"]
    
    
## Pane

def paneContract():
    pane = hou.ui.paneUnderCursor()
    fraction = pane.getSplitFraction()
    fraction = round(fraction, 3) + 0.1
    message = "Pane fraction: " + str(fraction)
    hou.ui.setStatusMessage(message)
    pane = pane.setSplitFraction(fraction)
paneContract.interactive_contexts = ["all"]


def paneExpand():
    pane = hou.ui.paneUnderCursor()
    fraction = pane.getSplitFraction()
    fraction = round(fraction, 3) - 0.1
    message = "Pane fraction: " + str(fraction)
    hou.ui.setStatusMessage(message)
    pane = pane.setSplitFraction(fraction)
paneExpand.interactive_contexts = ["all"]


def paneNewTab():
    reload(hctl_new_tab_menu)
    newTabMenu = hctl_new_tab_menu.newTabMenu()
    newTabMenu.show()
paneNewTab.interactive_contexts = ["all"]


def paneOnly():
    for pane in hou.ui.curDesktop().panes():
        if pane != hou.ui.paneUnderCursor():
            for paneTab in pane.tabs():
                paneTab.close()
paneOnly.interactive_contexts = ["all"]


def paneRatioHalf():
    pane = hou.ui.paneUnderCursor()
    pane.setSplitFraction(0.5)
paneRatioHalf.interactive_contexts = ["all"]


def paneRatioQuarter():
    pane = hou.ui.paneUnderCursor()
    pane.setSplitFraction(0.25)
paneRatioQuarter.interactive_contexts = ["all"]


def paneRatioThird():
    pane = hou.ui.paneUnderCursor()
    pane.setSplitFraction(0.333)
paneRatioThird.interactive_contexts = ["all"]


def paneResize():
    pane = hou.ui.paneUnderCursor()
    reload(hctl_resize)
    resizeWidget = hctl_resize.resizeWidget(pane)
    resizeWidget.show()
paneResize.interactive_contexts = ["all"]


def paneSplitHorizontal():
    pane = hou.ui.paneUnderCursor()
    newPane = pane.splitHorizontally()
paneSplitHorizontal.interactive_contexts = ["all"]


def paneSplitVertical():
    pane = hou.ui.paneUnderCursor()
    newPane = pane.splitVertically()
paneSplitVertical.interactive_contexts = ["all"]


def paneSplitRotate():
    pane = hou.ui.paneUnderCursor()
    pane.splitRotate()
paneSplitRotate.interactive_contexts = ["all"]


def paneSplitSwap():
    pane = hou.ui.paneUnderCursor()
    pane.splitSwap()
paneSplitSwap.interactive_contexts = ["all"]


def paneToggleMaximized():
    pane = hou.ui.paneUnderCursor()
    pane.setIsMaximized(not pane.isMaximized())
paneToggleMaximized.interactive_contexts = ["all"]


def paneToggleSplitMaximized():
    pane = hou.ui.paneUnderCursor()
    pane.setIsSplitMaximized(not pane.isSplitMaximized())
paneToggleSplitMaximized.interactive_contexts = ["all"]


## Panetab

def paneTabClose():
    paneTab = hou.ui.paneTabUnderCursor()
    paneTab.close()
paneTabClose.interactive_contexts = ["all"]


def paneTabGetCurrentNode():
    paneTab = hou.ui.paneTabUnderCursor()
    if paneTab.hasNetworkControls():
        return paneTab.currentNode()
    return None
paneTabGetCurrentNode.interactive_contexts = ["none"]


def paneTabGetCurrentViewport():
    paneTab = hou.ui.paneTabUnderCursor()
    if paneTab.type() == hou.paneTabType.SceneViewer:
        return paneTab.curViewport()
    else:
        return None
paneTabGetCurrentViewport.interactive_contexts = ["none"]


def paneTabGetPath():
    paneTab = hou.ui.paneTabUnderCursor()
    if paneTab.hasNetworkControls():
        return paneTab.pwd().path()
    else:
        return "No path"
paneTabGetPath.interactive_contexts = ["none"]


def paneTabGetSceneViewer():
    paneTab = hou.ui.paneTabUnderCursor()
    if paneTab.type() == hou.paneTabType.SceneViewer:
        return paneTab
    else:
        hou.ui.setStatusMessage("Not a scene viewer")
paneTabGetSceneViewer.interactive_contexts = ["none"]


def paneTabOnly():
    for paneTab in hou.ui.paneUnderCursor().tabs():
        if paneTab != hou.ui.paneTabUnderCursor():
            paneTab.close()
paneTabOnly.interactive_contexts = ["all"]


def paneTabSetTypeDetailsView():
    paneTab = hou.ui.paneTabUnderCursor()
    paneTab.setType(hou.paneTabType.DetailsView)
paneTabSetTypeDetailsView.interactive_contexts = ["all"]


def paneTabSetTypeNetworkEditor():
    paneTab = hou.ui.paneTabUnderCursor()
    paneTab.setType(hou.paneTabType.NetworkEditor)
paneTabSetTypeNetworkEditor.interactive_contexts = ["all"]


def paneTabSetTypeParm():
    paneTab = hou.ui.paneTabUnderCursor()
    paneTab.setType(hou.paneTabType.Parm)
paneTabSetTypeParm.interactive_contexts = ["all"]


def paneTabSetTypePythonShell():
    paneTab = hou.ui.paneTabUnderCursor()
    paneTab.setType(hou.paneTabType.PythonShell)
paneTabSetTypePythonShell.interactive_contexts = ["all"]


def paneTabSetTypeSceneViewer():
    paneTab = hou.ui.paneTabUnderCursor()
    paneTab.setType(hou.paneTabType.SceneViewer)
paneTabSetTypeSceneViewer.interactive_contexts = ["all"]


def paneTabToggleNetworkControls():
    paneTab = hou.ui.paneTabUnderCursor()
    if paneTab.hasNetworkControls():
        paneTab.showNetworkControls(not paneTab.isShowingNetworkControls())
paneTabToggleNetworkControls.interactive_contexts = ["all"]


def paneTabTogglePin():
    paneTab = hou.ui.paneTabUnderCursor()
    paneTab.setPin(not paneTab.isPin())
paneTabTogglePin.interactive_contexts = ["all"]

        
## Print
    
def printLayout():
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
printLayout.interactive_contexts = ["all"]


## Scene Viewer

def sceneViewerGetDisplaySets():
    displaySets = []
    for sceneViewer in desktopGetSceneViewers():
        viewports = sceneViewer.viewports()
        for viewport in viewports:
            settings = viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
    return(displaySets)
sceneViewerGetDisplaySets.interactive_contexts = ["none"]


def sceneViewerLayoutDoubleSide():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleSide)
sceneViewerLayoutDoubleSide.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutDoubleStack():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleStack)
sceneViewerLayoutDoubleStack.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutQuad():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.Quad)
sceneViewerLayoutQuad.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutQuadBottomSplit():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadBottomSplit)
sceneViewerLayoutQuadBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutQuadLeftSplit():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadLeftSplit)
sceneViewerLayoutQuadLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutSingle():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.Single)
sceneViewerLayoutSingle.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutTripleBottomSplit():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleBottomSplit)
sceneViewerLayoutTripleBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutTripleLeftSplit():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        sceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleLeftSplit)
sceneViewerLayoutTripleLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLopToggleLightGeo():
    sceneViewer = paneTabGetSceneViewer()
    if sceneViewer:
        is_visible = sceneViewer.showLights()
        sceneViewer.setShowLights(not is_visible)
sceneViewerLopToggleLightGeo.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerOpenVisualizerMenu():
    reload(hctl_vis_menu)
    visualizerMenu = hctl_vis_menu.visualizerMenu()
    visualizerMenu.show()
sceneViewerOpenVisualizerMenu.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleBackface():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPrimBackfaces():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPrimBackfaces((is_visible + 1) % 2)
sceneViewerToggleBackface.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleDisplayOptionsToolbar():
    is_visible = 0
    sceneViewers = desktopGetSceneViewers()
    for sceneViewer in sceneViewers:
        if sceneViewer.isShowingDisplayOptionsBar():
            is_visible = 1
    for sceneViewer in sceneViewers:
        sceneViewer.showDisplayOptionsBar((is_visible + 1) % 2)
sceneViewerToggleDisplayOptionsToolbar.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleGrid():
    paneTab = hou.ui.paneTabUnderCursor()
    if paneTab.type() == hou.paneTabType.SceneViewer:
        is_visible = paneTab.referencePlane().isVisible()
        paneTab.referencePlane().setIsVisible(not is_visible)
sceneViewerToggleGrid.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleGroupList():
    is_visible = 0
    sceneViewers = desktopGetSceneViewers()
    for sceneViewer in sceneViewers:
        if sceneViewer.isGroupListVisible():
            is_visible = 1
    for sceneViewer in sceneViewers:
        sceneViewer.setGroupListVisible((is_visible + 1) % 2)
sceneViewerToggleGroupList.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleKeycam():
    sceneViewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
    if sceneViewer:
        networkEditorContext = sceneViewer.pwd()
        context_type = networkEditorContext.childTypeCategory().name()
        if context_type == "Object":
            sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam state in Obj context.")
        elif context_type == "Sop":
            sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam state in Sop context.")
        elif context_type == "Lop":
            sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam state in Lop context.")
        else:
            hou.ui.setStatusMessage("No Obj, Sop or Lop context.", hou.severityType.Error)
    else:
        hou.ui.setStatusMessage("No Scene Viewer.", hou.severityType.Error)
sceneViewerToggleKeycam.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePointMarkers():
    is_visible = 0
    displaySets = sceneViewerGetDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointMarkers():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPointMarkers((is_visible + 1) % 2)
sceneViewerTogglePointMarkers.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePointNormals():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointNormals():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPointNormals((is_visible + 1) % 2)
sceneViewerTogglePointNormals.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePointNumbers():
    is_visible = 0
    displaySets = sceneViewerGetDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointNumbers():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPointNumbers((is_visible + 1) % 2)
sceneViewerTogglePointNumbers.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePrimNumbers():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPrimNumbers():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPrimNumbers((is_visible + 1) % 2)
sceneViewerTogglePrimNumbers.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleToolbars():
    sceneViewer = getSceneViewers()[0]
    state1 = sceneViewer.isShowingOperationBar()
    state2 = sceneViewer.isShowingDisplayOptionsBar()
    state3 = sceneViewer.isShowingSelectionBar()
    if state1 + state2 + state3 > 0:
        sceneViewer.showOperationBar(0)
        sceneViewer.showDisplayOptionsBar(0)
        sceneViewer.showSelectionBar(0)
    else:
        sceneViewer.showOperationBar(1)
        sceneViewer.showDisplayOptionsBar(1)
        sceneViewer.showSelectionBar(1)
sceneViewerToggleToolbars.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleVectors():
    sceneViewers = get_scene_viewers()
    for sceneViewer in sceneViewers:
        viewports = sceneViewer.viewports()
        for viewport in viewports:
            viewportSettings = viewport.settings()
            vector_scale = viewportSettings.vectorScale()
            if vector_scale == 1:
                viewportSettings.setVectorScale(0)
            elif vector_scale == 0:
                viewportSettings.setVectorScale(1)
            else:
                viewportSettings.setVectorScale(1)
sceneViewerToggleVectors.interactive_contexts = ["paneTabType.SceneViewer"]

        
## Session

def sessionEvalBindings():
    reload(hctl_bindings)
    hctl_bindings.updateBindings()
sessionEvalBindings.interactive_contexts = ["all"]


def sessionEvalKeycam():
    hou.ui.reloadViewerState("keycam")
sessionEvalKeycam.interactive_contexts = ["all"]


def sessionGetAutoSaveState():
    state = hou.getPreference("autoSave")
    return state
sessionGetAutoSaveState.interactive_contexts = ["none"]


def sessionOpenFile():
    hou.ui.selectFile()
sessionOpenFile.interactive_contexts = ["all"]


def sessionRestart():
    return
sessionRestart.interactive_contexts = ["none"]


def sessionTriggerUpdate():
    hou.ui.triggerUpdate()
sessionTriggerUpdate.interactive_contexts = ["all"]


def sessionUpdateModeAuto():
    hou.setUpdateMode(hou.updateMode.AutoUpdate)
sessionUpdateModeAuto.interactive_contexts = ["all"]


def sessionUpdateModeManual():
    hou.setUpdateMode(hou.updateMode.Manual)
sessionUpdateModeManual.interactive_contexts = ["all"]


def sessionToggleAutoSave():
    is_autosave = hou.getPreference("autoSave")
    if is_autosave == "0":
        hou.setPreference("autoSave", "1")
    else:
        hou.setPreference("autoSave", "0");
sessionToggleAutoSave.interactive_contexts = ["none"]


## Viewport

def viewportGetVisualizers():
    viewport = paneTabGetCurrentViewport()
    if viewport:
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr
    else:
        return None 
