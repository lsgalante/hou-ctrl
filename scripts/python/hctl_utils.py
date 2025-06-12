import hou
from importlib import reload
import hctl
import hctl_vis_menu
import hctl_new_tab_menu
import hctl_resize
import hctl_bindings
import time



###########
# Desktop #
###########

def desktopEvalColorSchemes(*args):
    hou.ui.reloadColorScheme()
desktopEvalColorSchemes.interactive_contexts = ["all"]


def desktopLayoutA(paneTab):
    pane = paneTab.pane()
    # Close all panes but one
    paneOnly(pane)
    # Close all tabs but one
    paneTabOnly(paneTab)

    # There should be only 1 pane at this point
    panes = desktopPanes()
    # panes[0].tabs()[0].setPin(False)

    # Main center split
    panes[0].splitHorizontally()
    panes = desktopPanes()
    panes[0].setSplitFraction(0.6)

    # Left vertical split
    panes[0].splitVertically()
    panes[0].setSplitFraction(0.2)

    # Right vertical split
    panes[1].splitVertically()
    panes[1].setSplitFraction(0.666)

    paneTabs = desktopPaneTabs()
    paneTabs[0].setType(hou.paneTabType.SceneViewer) # Top left
    paneTabs[1].setType(hou.paneTabType.DetailsView) # Bas left
    paneTabs[2].setType(hou.paneTabType.Parm) # Top right
    paneTabs[3].setType(hou.paneTabType.NetworkEditor) # Bas right
    # paneTabs[3].setPin(True)
    # desktopToggleMenus()
    desktopToggleStowbars()
    desktopToggleStowbars()
desktopLayoutA.interactive_contexts = ["all"]


def desktopLayoutB(paneTab):
    paneOnly()
    paneTabOnly()

    panes = desktopPanes()
    panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
    panes[0].splitHorizontally()

    panes = desktopPanes()
    panes[0].splitVertically()
    panes[1].splitVertically()

    panes = desktopPanes()
    panes[0].tabs()[0].setType(hou.paneTabType.SceneViewer) # Top left
    panes[1].tabs()[0].setType(hou.paneTabType.Parm)
desktopLayoutB.interactive_contexts = ["all"]


def desktopLayoutQuad(paneTab):
    paneOnly(paneTab)
    paneTabOnly(paneTab)

    panes = desktopPanes()
    panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
    panes[0].splitHorizontally()

    panes = desktopPanes()
    panes[0].splitVertically()
    panes[1].splitVertically()
desktopLayoutQuad.interactive_contexts = ["all"]


def desktopLayoutTriH(paneTab):
    sessionRemoveEventLoopCallbacks()
    # Reduce
    paneOnly(paneTab)
    paneTabOnly(paneTab)
    # Make panes
    panes = desktopPanes()
    panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
    panes[0].splitHorizontally()
    panes = desktopPanes()
    panes[1].splitHorizontally()
    panes = desktopPanes()
    # Make paneTabs
    panes[1].createTab(hou.paneTabType.PythonShell)
    panes[1].tabs()[0].setIsCurrentTab()
    # Set types
    panes[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
    panes[1].tabs()[0].setType(hou.paneTabType.Parm)
    panes[1].tabs()[1].setType(hou.paneTabType.DetailsView)
    panes[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
    # Ratios
    panes[0].setSplitFraction(0.5)

    hou.session.lastPane = hou.ui.paneUnderCursor()
    hou.ui.addEventLoopCallback(triHCallback)
desktopLayoutTriH.interactive_contexts = ["all"]


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


def desktopLayoutTriV(paneTab):
    sessionRemoveEventLoopCallbacks()

    # Reduce
    paneOnly(paneTab)
    paneTabOnly(paneTab)

    # Make panes
    panes = desktopPanes()
    panes[0].tabs()[0].setType(hou.paneTabType.PythonShell)
    panes[0].splitHorizontally()
    panes = desktopPanes()
    panes[1].splitVertically()
    panes = desktopPanes()

    # Make paneTabs
    panes[1].createTab(hou.paneTabType.PythonShell)
    panes[1].tabs()[0].setIsCurrentTab()

    # Set types
    panes[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
    panes[1].tabs()[0].setType(hou.paneTabType.Parm)
    panes[1].tabs()[1].setType(hou.paneTabType.DetailsView)
    panes[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)

    # Set ratios
    panes[0].setSplitFraction(0.66)


    hou.session.lastPane = hou.ui.paneUnderCursor()
    hou.ui.addEventLoopCallback(triVCallback)
desktopLayoutTriV.interactive_contexts = ["all"]


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


def desktopNetworkEditors(*args):
    editors = []
    for paneTab in desktopPaneTabs():
        if paneTab.type() == hou.paneTabType.NetworkEditor:
            editors.append(paneTab)
    return editors
desktopNetworkEditors.interactive_contexts = ["none"]


def desktopPanes(*args):
    panes = hou.ui.curDesktop().panes()
    return panes
desktopPanes.interactive_contexts = ["none"]


def desktopSceneViewers(*args):
    paneTabs = hou.ui.paneTabs()
    sceneViewers = [paneTab for paneTab in paneTabs if paneTab.type() == hou.paneTabType.SceneViewer]
    return sceneViewers
desktopSceneViewers.interactive_contexts = ["none"]


def desktopShelfHide(*args):
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(0)
    hou.ui.reloadViewportColorSchemes()
desktopShelfHide.interactive_contexts = ["none"]


def desktopShelfShow(*args):
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(1)
desktopShelfShow.interactive_contexts = ["none"]


def desktopPaneTabs(*args):
    paneTabs = []
    for pane in desktopPanes():
        for paneTab in pane.tabs():
            paneTabs.append(paneTab)
    return paneTabs
desktopPaneTabs.interactive_contexts = ["none"]


def desktopToggleMainMenuBar(*args):
    if hou.getPreference("showmenu.val") == "1":
        hou.setPreference("showmenu.val", "0")
    else:
        hou.setPreference("showmenu.val", "1")
desktopToggleMainMenuBar.interactive_contexts = ["all"]


def desktopToggleMenus(*args):
    visible = 0
    # gather contexts
    editors = desktopNetworkEditors()
    panes = desktopPanes()
    viewers = desktopSceneViewers()
    paneTabs = desktopPaneTabs()
    # main menu
    if hou.getPreference("showmenu.val") == "1":
        visible = 1
    # network editor menu
    elif any(editor.getPref("showmenu") == "1" for editor in editors):
        visible = 1
    # network controls
    elif any(paneTab.isShowingNetworkControls() for paneTab in paneTabs):
        visible = 1
    # scene viewer toolbars (top, right, left)
    elif any(viewer.isShowingOperationBar() for viewer in viewers):
        visible = 1
    elif any(viewer.isShowingDisplayOptionsBar() for viewer in viewers):
        visible = 1
    elif any(viewer.isShowingSelectionBar() for sceneViewer in sceneViewers):
        visible = 1
    # paneTabs
    elif any(pane.isShowingPaneTabs() for pane in panes):
        visible = 1
    # hide all
    if visible:
        hou.setPreference("showmenu.val", "0")
        for editor in editors:
            editor.setPref("showmenu", "0")
        for paneTab in paneTabs:
            paneTab.showNetworkControls(0)
        for pane in panes:
            pane.showPaneTabs(0)
        for viewer in viewers:
            viewer.showOperationBar(0)
            viewer.showDisplayOptionsBar(0)
            viewer.showSelectionBar(0)
        hou.ui.setHideAllMinimizedStowbars(1)
    # show all
    else:
        hou.setPreference("showmenu.val", "1")
        for editor in editors:
            editor.setPref("showment", "1")
        for paneTab in paneTabs:
            paneTab.showNetworkControls(1)
        for pane in panes:
            pane.showPaneTabs(1)
        for viewer in viewers:
            viewer.showOperationBar(1)
            viewer.showDisplayOptionsBar(1)
            viewer.showSelectionBar(1)
        hou.ui.setHideAllMinimizedStowbars(0)
desktopToggleMenus.interactive_contexts = ["all"]


def desktopToggleHctl(*args):
    reload(hctl)
    hctl.dialog().show()
desktopToggleHctl.interactive_contexts = ["all"]


def desktopToggleNetworkControls(*args):
    visible = 0
    paneTabs = desktopPaneTabs()
    for paneTab in paneTabs:
        if paneTab.isShowingNetworkControls():
            visible = 1
    for paneTab in paneTabs:
        paneTab.showNetworkControls((visible + 1) % 2)
desktopToggleNetworkControls.interactive_contexts = ["all"]


def desktopTogglePaneTabs(*args):
    panes = desktopPanes()
    visible = 0
    for pane in panes:
        if pane.isShowingPaneTabs():
            visible = 1
    for pane in panes:
        pane.showPaneTabs(not visible)
desktopTogglePaneTabs.interactive_contexts = ["all"]


def desktopToggleStowbars(*args):
    hidden = hou.ui.hideAllMinimizedStowbars()
    hou.ui.setHideAllMinimizedStowbars(not hidden)
desktopToggleStowbars.interactive_contexts = ["all"]


def desktopUpdateMainMenuBar(*args):
    hou.ui.updateMainMenuBar()
desktopUpdateMainMenuBar.interactive_contexts = ["all"]


def desktopViewports(*args):
    viewports = []
    sceneViewers = desktopSceneViewers()
    for sceneViewer in sceneViewers:
        for viewport in sceneViewer.viewports():
            viewports.append(viewport)
desktopViewports.interactive_contexts = ["none"]


##################
# Network Editor #
##################

def networkEditorAddNetworkBox(editor):
    context = editor.pwd()
    node = editor.currentNode()
    networkBox = context.createNetworkBox()
    networkBox.setPosition(node.position())
networkEditorAddNetworkBox.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorAddStickyNote(editor):
    context = editor.pwd()
    stickyNote = context.createStickyNote()
    cursor_pos =  editor.cursorPosition()
    stickyNote.setPosition(cursor_pos)
    color = hou.Color(0.71, 0.784, 1.0)
    stickyNote.setColor(color)
networkEditorAddStickyNote.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorConnectNodeTo(editor):
    node = networkEditorCurrentNode(editor)
    choices = ("a", "b", "c")
    popup = hou.ui.selectFromList(choices)
networkEditorConnectNodeTo.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorCurrentNode(editor):
    return editor.currentNode()
networkEditorCurrentNode.interactive_contexts = ["none"]


def networkEditorDeselectAllNodes(editor):
    node = networkEditorCurrentNode(editor)
    node.setSelected(False)
networkEditorDeselectAllNodes.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorDisplayNode(editor):
    context = editor.pwd()
    return  context.displayNode()
networkEditorDisplayNode.interactive_contexts = ["none"]


def networkEditorRenameNode(editor):
    node = networkEditorCurrentNode(editor)
    name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
    if name[0] == 0:
        node.setName(name[1])
networkEditorRenameNode.interactive_contexts = ["paneTabType.NetworkEditor", "paneTabType.Parm"]


def networkEditorRotateNodeInputs(editor):
    node = networkEditorCurrentNode(editor)
    connectors = node.inputConnectors()
networkEditorRotateNodeInputs.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorSelectDisplayNode(editor):
    displayNode = networkEditorDisplayNode(editor)
    displayNode.setCurrent(True, True)
networkEditorSelectDisplayNode.interactive_contexts = ["paneTabType.NetworkEditor"]


def networkEditorToggleDimUnusedNodes(editor):
    dim = "0"
    if editor.getPref("dimunusednodes") == "1":
        dim = "1"
    if dim == "0":
        editor.setPref("dimunusednodes", "1")
    else:
        editor.setPref("dimunusednodes", "0")
networkEditorToggleDimUnusedNodes.interactive_contexts = ["all"]


def networkEditorToggleGridLines(editor):
    visible = "0"
    if editor.getPref("gridmode") == "1":
        visible = "1"
    if editor.getPref("gridmode") == "0":
        editor.setPref("gridmode", "1")
    else:
        editor.setPref("gridmode", "0")
networkEditorToggleGridLines.interactive_contexts = ["all"]


def networkEditorToggleLocating(editor):
    locating = 0
    if editor.locatingEnabled():
        locating = 1
    editor.setLocatingEnabled(not locating)
networkEditorToggleLocating.interactive_contexts = ["all"]


def networkEditorToggleMenu(editor):
    visible = 0
    if editor.getPref("showmenu") == "1":
        visible = 1
    if visible:
        networkEditor.setPref("showmenu", str(not visible))
networkEditorToggleMenu.interactive_contexts = ["all"]


def networkEditorToggleGridPoints(editor):
    visible = int(editor.getPref("gridmode"))
    editor.setPref("gridmode", str(not visible))
networkEditorToggleGridPoints.interactive_contexts = ["all"]


########
# Open #
########

def openColorEditor(*args):
    hou.ui.selectColor()
openColorEditor.interactive_contexts = ["all"]


def openFloatingParameterEditor(paneTab):
    if paneTab.type() == hou.paneTabType.NetworkEditor:
        node = paneTab.currentNode()
        hou.ui.showFloatingParameterEditor(node)
    else:
        hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)
openFloatingParameterEditor.interactive_contexts = ["all"]


def openHotkeyEditor(*args):
    print("open hotkey editor")
openHotkeyEditor.interactive_contexts = ["none"]


########
# Pane #
########

def paneContract(paneTab):
    pane = paneTab.pane()
    fraction = pane.getSplitFraction()
    fraction = round(fraction, 3) + 0.1
    message = "Pane fraction: " + str(fraction)
    hou.ui.setStatusMessage(message)
    pane = pane.setSplitFraction(fraction)
paneContract.interactive_contexts = ["all"]


def paneExpand(paneTab):
    pane = paneTab.pane()
    fraction = pane.getSplitFraction()
    fraction = round(fraction, 3) - 0.1
    message = "Pane fraction: " + str(fraction)
    hou.ui.setStatusMessage(message)
    pane = pane.setSplitFraction(fraction)
paneExpand.interactive_contexts = ["all"]


def paneNewPaneTab(paneTab):
    pane = paneTab.pane()
    reload(hctl_new_pane_tab_menu)
    newPaneTabMenu = hctl_new_pane_tab_menu.newPaneTabMenu()
    newPaneTabMenu.show()
paneNewPaneTab.interactive_contexts = ["all"]


def paneOnly(paneTab):
    this_pane = paneTab.pane()
    for pane in hou.ui.curDesktop().panes():
        if pane != this_pane:
            for paneTab in pane.tabs():
                paneTab.close()
paneOnly.interactive_contexts = ["all"]


def paneRatioGet(pane):
    return pane.getSplitFraction()
paneRatioGet.interactive_contexts = ["none"]


def paneRatioSet(pane, ratio):
    pane.setSplitFraction(ratio)
paneRatioSet.interactive_contexts = ["none"]


def paneRatioHalf(paneTab):
    pane = paneTab.pane()
    pane.setSplitFraction(0.5)
paneRatioHalf.interactive_contexts = ["all"]


def paneRatioQuarter(paneTab):
    pane = paneTab.pane()
    pane.setSplitFraction(0.25)
paneRatioQuarter.interactive_contexts = ["all"]


def paneRatioThird(paneTab):
    pane = paneTab.pane()
    pane.setSplitFraction(0.333)
paneRatioThird.interactive_contexts = ["all"]


def paneResize(paneTab):
    pane = paneTab.pane()
    reload(hctl_resize)
    resizeWidget = hctl_resize.resizeWidget(pane)
    resizeWidget.show()
paneResize.interactive_contexts = ["all"]


def paneSplitHorizontal(paneTab):
    pane = paneTab.pane()
    newPane = pane.splitHorizontally()
paneSplitHorizontal.interactive_contexts = ["all"]


def paneSplitVertical(paneTab):
    pane = paneTab.pane()
    newPane = pane.splitVertically()
paneSplitVertical.interactive_contexts = ["all"]


def paneSplitRotate(paneTab):
    pane = paneTab.pane()
    pane.splitRotate()
paneSplitRotate.interactive_contexts = ["all"]


def paneSplitSwap(paneTab):
    pane = paneTab.pane()
    pane.splitSwap()
paneSplitSwap.interactive_contexts = ["all"]


def paneToggleMaximized(paneTab):
    pane = paneTab.pane()
    pane.setIsMaximized(not pane.isMaximized())
paneToggleMaximized.interactive_contexts = ["all"]


def paneTogglePaneTabs(paneTab):
    pane = paneTab.pane()
    pane.showPaneTabs(not pane.isShowingPaneTabs())
paneTogglePaneTabs.interactive_contexts = ["all"]


def paneToggleSplitMaximized(paneTab):
    pane = paneTab.pane()
    pane.setIsSplitMaximized(not pane.isSplitMaximized())
paneToggleSplitMaximized.interactive_contexts = ["all"]


###########
# Panetab #
###########

def paneTabClose(paneTab):
    paneTab.close()
paneTabClose.interactive_contexts = ["all"]


def paneTabCurrentNode(paneTab):
    if paneTab.hasNetworkControls():
        return paneTab.currentNode()
paneTabCurrentNode.interactive_contexts = ["none"]


def paneTabPath(paneTab):
    if paneTab.hasNetworkControls():
        return paneTab.pwd().path()
    else:
        return "No path"
paneTabPath.interactive_contexts = ["none"]


def paneTabOnly(this_paneTab):
    for paneTab in desktopPaneTabs():
        if paneTab != this_paneTab:
            paneTab.close()
paneTabOnly.interactive_contexts = ["all"]


def paneTabSetTypeDetailsView(paneTab):
    paneTab.setType(hou.paneTabType.DetailsView)
paneTabSetTypeDetailsView.interactive_contexts = ["all"]


def paneTabSetTypeNetworkEditor(paneTab):
    paneTab.setType(hou.paneTabType.NetworkEditor)
paneTabSetTypeNetworkEditor.interactive_contexts = ["all"]


def paneTabSetTypeParm(paneTab):
    paneTab.setType(hou.paneTabType.Parm)
paneTabSetTypeParm.interactive_contexts = ["all"]


def paneTabSetTypePythonShell(paneTab):
    paneTab.setType(hou.paneTabType.PythonShell)
paneTabSetTypePythonShell.interactive_contexts = ["all"]


def paneTabSetTypeSceneViewer(paneTab):
    paneTab.setType(hou.paneTabType.SceneViewer)
paneTabSetTypeSceneViewer.interactive_contexts = ["all"]


def paneTabToggleNetworkControls(paneTab):
    if paneTab.hasNetworkControls():
        paneTab.showNetworkControls(not paneTab.isShowingNetworkControls())
paneTabToggleNetworkControls.interactive_contexts = ["all"]


def paneTabTogglePin(paneTab):
    paneTab.setPin(not paneTab.isPin())
paneTabTogglePin.interactive_contexts = ["all"]


#########
# Print #
#########

def printLayout(*args):
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


################
# Scene Viewer #
################

def sceneViewerCurrentViewport(sceneViewer):
    return sceneViewer.curViewport()
sceneViewerCurrentViewport.interactive_contexts = ["none"]


def sceneViewerDisplaySets(sceneViewer):
    viewports = sceneViewer.viewports()
    displaySets = []
    for viewport in viewports:
        settings = viewport.settings()
        displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
        displaySets.append(displaySet)
    return(displaySets)
sceneViewerDisplaySets.interactive_contexts = ["none"]


def sceneViewerLayoutDoubleSide(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleSide)
sceneViewerLayoutDoubleSide.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutDoubleStack(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleStack)
sceneViewerLayoutDoubleStack.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutQuad(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.Quad)
sceneViewerLayoutQuad.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutQuadBottomSplit(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadBottomSplit)
sceneViewerLayoutQuadBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutQuadLeftSplit(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadLeftSplit)
sceneViewerLayoutQuadLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutSingle(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.Single)
sceneViewerLayoutSingle.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutTripleBottomSplit(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleBottomSplit)
sceneViewerLayoutTripleBottomSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLayoutTripleLeftSplit(sceneViewer):
    sceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleLeftSplit)
sceneViewerLayoutTripleLeftSplit.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerLopToggleLightGeo(sceneViewer):
    visible = sceneViewer.showLights()
    sceneViewer.setShowLights(not visible)
sceneViewerLopToggleLightGeo.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerVisualizerMenu(sceneViewer):
    reload(hctl_vis_menu)
    visualizerMenu = hctl_vis_menu.visualizerMenu()
    visualizerMenu.show()
sceneViewerVisualizerMenu.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleBackface(sceneViewer):
    visible = 0
    displaySets = sceneViewerDisplaySets(sceneViewer)
    for displaySet in displaySets:
        if displaySet.isShowingPrimBackfaces():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPrimBackfaces(not visible)
sceneViewerToggleBackface.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleDisplayOptionsToolbar(sceneViewer):
    visible = 0
    if sceneViewer.isShowingDisplayOptionsBar():
        visible = 1
    sceneViewer.showDisplayOptionsBar(not visible)
sceneViewerToggleDisplayOptionsToolbar.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleGrid(sceneViewer):
    visible = sceneViewer.referencePlane().isVisible()
    sceneViewer.referencePlane().setIsVisible(not visible)
sceneViewerToggleGrid.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleGroupList(sceneViewer):
    visible = 0
    if sceneViewer.isGroupListVisible():
        visible = 1
    sceneViewer.setGroupListVisible(not visible)
sceneViewerToggleGroupList.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleKeycam(sceneViewer):
    context = sceneViewer.pwd()
    context_type = context.childTypeCategory().name()
    if context_type == "Object":
        sceneViewer.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam viewer state in Obj context.")
    elif context_type == "Sop":
        sceneViewer.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam viewer state in Sop context.")
    elif context_type == "Lop":
        sceneViewer.setCurrentState("keycam")
        hou.ui.setStatusMessage("Entered keycam viewer state in Lop context.")
    else:
        hou.ui.setStatusMessage("No Obj, Sop or Lop context.", hou.severityType.Error)
sceneViewerToggleKeycam.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePointMarkers(sceneViewer):
    visible = 0
    displaySets = sceneViewerGetDisplaySets(sceneViewer)
    for displaySet in displaySets:
        if displaySet.isShowingPointMarkers():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPointMarkers(not visible)
sceneViewerTogglePointMarkers.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePointNormals(sceneViewer):
    visible = 0
    displaySets = sceneViewerGetDisplaySets(sceneViewer)
    for displaySet in displaySets:
        if displaySet.isShowingPointNormals():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPointNormals(not visible)
sceneViewerTogglePointNormals.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePointNumbers(sceneViewer):
    visible = 0
    displaySets = sceneViewerGetDisplaySets(sceneViewer)
    for displaySet in displaySets:
        if displaySet.isShowingPointNumbers():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPointNumbers(not visible)
sceneViewerTogglePointNumbers.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePrimNormals(sceneViewer):
    visible = 0
    displaySets = sceneViewerGetDisplaySets(sceneViewer)
    for displaySet in displaySets:
        if displaySet.isShowingPrimNormals():
            visible = 1
        for displaySet in displaySets:
            displaySet.showPrimNormals(not_visible)
sceneViewerTogglePrimNormals.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerTogglePrimNumbers(sceneViewer):
    visible = 0
    displaySets = sceneViewerGetDisplaySets(sceneViewer)
    for displaySet in displaySets:
        if displaySet.isShowingPrimNumbers():
            visible = 1
    for displaySet in displaySets:
        displaySet.showPrimNumbers(not visible)
sceneViewerTogglePrimNumbers.interactive_contexts = ["paneTabType.SceneViewer"]


def sceneViewerToggleToolbars(sceneViewer):
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


def sceneViewerToggleVectors(sceneViewer):
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


###########
# Session #
###########

def sessionAutoSaveState(*args):
    state = hou.getPreference("autoSave")
    return state
sessionAutoSaveState.interactive_contexts = ["none"]


def sessionEvalBindings(*args):
    reload(hctl_bindings)
    hctl_bindings.updateBindings()
sessionEvalBindings.interactive_contexts = ["all"]


def sessionEvalKeycam(*args):
    hou.ui.reloadViewerState("keycam")
sessionEvalKeycam.interactive_contexts = ["all"]


def sessionOpenFile(*args):
    hou.ui.selectFile()
sessionOpenFile.interactive_contexts = ["all"]


def sessionRemoveEventLoopCallbacks(*args):
    callbacks = hou.ui.eventLoopCallbacks()
    for callback in callbacks:
        hou.ui.removeEventLoopCallback(callback)
sessionRemoveEventLoopCallbacks.interactive_contexts = ["all"]


def sessionRestart(*args):
    return
sessionRestart.interactive_contexts = ["none"]


def sessionTriggerUpdate(*args):
    hou.ui.triggerUpdate()
sessionTriggerUpdate.interactive_contexts = ["all"]


def sessionUpdateModeAuto(*args):
    hou.setUpdateMode(hou.updateMode.AutoUpdate)
sessionUpdateModeAuto.interactive_contexts = ["all"]


def sessionUpdateModeManual(*args):
    hou.setUpdateMode(hou.updateMode.Manual)
sessionUpdateModeManual.interactive_contexts = ["all"]


def sessionToggleAutoSave(*args):
    autosave = hou.getPreference("autoSave")
    if autosave == "0":
        hou.setPreference("autoSave", "1")
    else:
        hou.setPreference("autoSave", "0");
sessionToggleAutoSave.interactive_contexts = ["none"]


############
# Viewport #
############

def viewportVisualizers(viewport):
    category = hou.viewportVisualizerCategory.Scene
    vis_arr = hou.viewportVisualizers.visualizers(category)
    return vis_arr
