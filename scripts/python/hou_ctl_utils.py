import hou
from importlib import reload
import hou_ctl_finder
import hou_ctl_vis_menu
import hou_ctl_new_tab_menu


## Add

def addStickyNote():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        node = tab.pwd()
        stickynote = node.createStickyNote()
        cursor_pos =  tab.cursorPosition()
        stickynote.setPosition(cursor_pos)
        color = hou.Color(0.71, 0.784, 1.0)
        stickynote.setColor(color)
    else:
        hou.ui.setStatusMessage("Focused tab is not a network editor.", hou.severityType.Error) 
      

## Get

def getAutosaveState():
    state = hou.getPreference("autoSave")
    return state

def getCurrentNode():
    tabs = hou.ui.paneTabs()
    tabs = [tab for tab in tabs if tab.type() == hou.paneTabType.NetworkEditor]
    node = tabs[0].currentNode()    
    return node

def getDisplaySets():
    displaySets = []
    viewers = getSceneViewers()
    for viewer in viewers:
        viewports = viewer.viewports()
        for viewport in viewports:
            settings = viewport.settings()
            displaySet = settings.displaySet(hou.displaySetType.DisplayModel)
            displaySets.append(displaySet)
    return(displaySets)
    
def getNetworks():
    tabs = hou.ui.paneTabs()
    networks = [tab for tab in tabs if tab.type() == hou.paneTabType.NetworkEditor]
    return networks

def getSceneViewers():
    tabs  = hou.ui.paneTabs()
    viewers = [tab for tab in tabs if tab.type() == hou.paneTabType.SceneViewer]
    return viewers

def getViewports():
    viewports = []
    viewers = getSceneViewers()
    for viewer in viewers:
        for viewport in viewer.viewports():
            viewports.append(viewport)
    return(viewports)

## Hide

def hideShelf():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(0)


## Network

def networkBox():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        parent = tab.pwd()
        node = tab.currentNode()
        box = parent.createNetworkBox()
        box.setPosition(node.position())
    else:
        hou.ui.setStatusMessage("Network editor not focused", hou.severityType.Error)


## New tab

def newTab():
    reload(hou_ctl_new_tab_menu)
    new_tab_menu = hou_ctl_new_tab_menu.newTabMenu()
    new_tab_menu.show()


## Node

def nodeDeselectAll():
    node = getCurrentNode()
    node.setSelected(False)

def nodeRotateInputs():
    node = getCurrentNode()
    connectors = node.inputConnectors()


## Open

def openColorEditor():
    hou.ui.selectColor()

def openFloatingParameterEditor():
    tab = hou.ui.paneTabUnderCursor()
    if tab.type() == hou.paneTabType.NetworkEditor:
        node = tab.currentNode()
        hou.ui.showFloatingParameterEditor(node)
    else:
        hou.ui.setStatusMessage("Focused tab is not a network editor.", hou.severityType.Error) 

def openHotkeyEditor():
    print("open hotkey editor")

def openVisualizerMenu():
    reload(hou_ctl_vis_menu)
    visualizerMenu = hou_ctl_vis_menu.visualizerMenu()
    visualizerMenu.show()

## Pane

def paneContract():
    pane = hou.ui.paneUnderCursor()
    fraction = pane.getSplitFraction()
    fraction = round(fraction, 3) + 0.1
    message = "Pane fraction: " + str(fraction)
    hou.ui.setStatusMessage(message)
    pane = pane.setSplitFraction(fraction)

def paneExpand():
    pane = hou.ui.paneUnderCursor()
    fraction = pane.getSplitFraction()
    fraction = round(fraction, 3) - 0.1
    message = "Pane fraction: " + str(fraction)
    hou.ui.setStatusMessage(message)
    pane = pane.setSplitFraction(fraction)

def paneRatioHalf():
    pane = hou.ui.paneUnderCursor()
    pane.setSplitFraction(0.5)

def paneRatioQuarter():
    pane = hou.ui.paneUnderCursor()
    pane.setSplitFraction(0.25)

def paneRatioThird():
    pane.hou.ui.paneUnderCursor()
    pane.setSplitFraction(0.333)

def paneSplitHorizontal():
    pane = hou.ui.paneUnderCursor()
    new_pane = pane.splitHorizontally()

def paneSplitVertical():
    pane = hou.ui.paneUnderCursor()
    new_pane = pane.splitVertically()

def paneSplitRotate():
    pane = hou.ui.paneUnderCursor()
    pane.splitRotate()

def paneSplitSwap():
    pane = hou.ui.paneUnderCursor()
    pane.splitSwap()


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


## Reload

def reloadColorSchemes():
    hou.ui.reloadColorScheme()
    hou.ui.reloadViewportColorSchemes()

def reloadKeycam():
    hou.ui.reloadViewerState("keycam")


## Rename

def renameNode():
    node = getCurrentNode()
    name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
    if name[0] == 0:
        node.setName(name[1])


## Restart

def restartHoudini():
    return


## Scene

def sceneSetA():
    panes = hou.ui.panes()
    print(panes)

## Set

def setTabTypeNetwork():
    tab = hou.ui.paneTabUnderCursor()
    tab.setType(hou.paneTabType.NetworkEditor)

def setTabTypeParameters():
    tab = hou.ui.paneTabUnderCursor()
    tab.setType(hou.paneTabType.Parm)

def setTabTypePython():
    tab = hou.ui.paneTabUnderCursor()
    tab.setType(hou.paneTabType.PythonShell)

def setTabTypeSceneViewer():
    tab = hou.ui.paneTabUnderCursor()
    tab.setType(hou.paneTabType.SceneViewer)

def setTabTypeSpreadsheet():
    tab = hou.ui.paneTabUnderCursor()
    tab.setType(hou.paneTabType.DetailsView)


## Show

def showShelf():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(1)


## Tab

def tabClose():
    tab = hou.ui.paneTabUnderCursor()
    tab.close()

def tabTogglePin():
    tab = hou.ui.paneTabUnderCursor()
    if tab.isPin():
        tab.setPin(False)
    else:
        tab.setPin(True)


## Toggle

def toggleAllMenus():
    is_visible = 0

    # gather contexts
    networks = getNetworks()
    tabs = hou.ui.paneTabs()
    panes = hou.ui.curDesktop().panes()
    viewers = getSceneViewers()

    # main menu
    if hou.getPreference("showmenu.val") == "1":
        is_visible = 1

    # network menu
    for network in networks:
        if network.getPref("showmenu") == "1":
            is_visible = 1

    # network controls
    for tab in tabs:
        if tab.isShowingNetworkControls():
            is_visible = 1

    # tabs
    for pane in panes:
        if pane.isShowingPaneTabs():
            is_visible = 1

    # scene viewer operation toolbar (top)
    for viewer in viewers:
        if viewer.isShowingOperationBar():
            is_visible = 1

    # scene viewer display options toolbar (right)
    for viewer in viewers:
        if viewer.isShowingDisplayOptionsBar():
            is_visible = 1

    # scene viewer selection toolbar (left)
    for viewer in viewers:
        if viewer.isShowingSelectionBar():
            is_visible = 1
    
    if is_visible:
        hou.setPreference("showmenu.val", "0")
        for network in networks:
            network.setPref("showmenu", "0")
        for tab in tabs:
            tab.showNetworkControls(0)
        for pane in panes:
            pane.showPaneTabs(0)
        for viewer in viewers:
            viewer.showOperationBar(0)
            viewer.showDisplayOptionsBar(0)
            viewer.showSelectionBar(0)
        hou.ui.setHideAllMinimizedStowbars(1)

    else:
        hou.setPreference("showmenu.val", "1")
        for network in networks:
            network.setPref("showment", "1")
        for tab in tabs:
            tab.showNetworkControls(1)
        for pane in panes:
            pane.showPaneTabs(1)
        for viewer in viewers:
            viewer.showOperationBar(1)
            viewer.showDisplayOptionsBar(1)
            viewer.showSelectionBar(1)
        hou.ui.setHideAllMinimizedStowbars(0)

def toggleAutosave():
    is_autosave = hou.getPreference("autoSave")
    if is_autosave == "0":
        hou.setPreference("autoSave", "1")
    else:
        hou.setPreference("autoSave", "0");

def toggleBackface():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPrimBackfaces():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPrimBackfaces((is_visible + 1) % 2)

def toggleDimUnusedNodes():
    is_dim = "0"
    networks = getNetworks()
    for network in networks:
        if network.getPref("dimunusednodes") == "1":
            is_dim = "1"
    for network in networks:
        if is_dim == "0":
            network.setPref("dimunusednodes", "1") 
        else:
            network.setPref("dimunusednodes", "0")

def toggleDisplayOptionsToolbar():
    is_visible = 0
    viewers = getSceneViewers()
    for viewer in viewers:
        if viewer.isShowingDisplayOptionsBar():
            is_visible = 1
    for viewer in viewers:
        viewer.showDisplayOptionsBar((is_visible + 1) % 2)

def toggleFinder():
    reload(hou_ctl_finder)
    finder = hou_ctl_finder.finder()
    finder.show()

def toggleGroupList():
    is_visible = 0
    viewers = getSceneViewers()
    for viewer in viewers:
        if viewer.isGroupListVisible():
            is_visible = 1
    for viewer in viewers:
        viewer.setGroupListVisible((is_visible + 1) % 2)

def toggleKeycam():
    viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
    if viewer != None:
        node = viewer.pwd()
        type = node.childTypeCategory().name()
        if type == "Object" or type == "Sop":
            viewer.setCurrentState("keycam")
        else:
            print("sop or obj only")
    else:
        print("no scene viewer")
        return

def toggleMainMenubar():
    if hou.getPreference("showmenu.val") == "1":
        hou.setPreference("showmenu.val", "0")
    else:
        hou.setPreference("showmenu.val", "1")

def toggleNetworkControls():
    is_visible = 0
    tabs = hou.ui.paneTabs()
    for tab in tabs:
        if tab.isShowingNetworkControls():
            is_visible = 1
    for tab in tabs:
        tab.showNetworkControls((is_visible + 1) % 2)

def toggleNetworkGridPoints():
    is_visible = "0"
    networks = getNetworks()
    for network in networks:
        if network.getPref("gridmode") == "1":
            is_visible = "1"
    for network in networks:
        if is_visible == "0":
            network.setPref("gridmode", "1")
        else:
            network.setPref("gridmode", "0")

def toggleNetworkGridLines():
    is_visible = "0"
    networks = getNetworks()
    for network in networks:
        if network.getPref("gridmode") == "1":
            is_visible = "1"
    for network in networks:
        if pref == "0":
            network.setPref("gridmode", "1")
        else:
            network.setPref("gridmode", "0")

def toggleNetworkLocating():
    is_locating = 0
    networks = getNetworks()
    for network in networks:
        if network.locatingEnabled():
            is_locating = 1
    for network in networks:
        network.setLocatingEnabled((is_locating + 1) % 2)

def toggleNetworkEditorMenu():
    is_visible = 0
    networks = getNetworks()
    for network in networks:
        if network.getPref("showmenu") == "1":
            is_visible = 1
    for network in networks:
        if is_visible:
            network.setPref("showmenu", "0")
        else:
            network.setPref("showmenu", "1")

def togglePaneMaximized():
    pane = hou.ui.paneUnderCursor()
    if pane.isMaximized():
        pane.setIsMaximized(False)
    else:
        pane.setIsMaximized(True)

def togglePanetabs():
    panes = hou.ui.curDesktop().panes()
    show = 1
    for pane in panes:
        if pane.isShowingPaneTabs():
            show = 0
    [pane.showPaneTabs(show) for pane in panes]

def togglePointMarkers():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointMarkers():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPointMarkers((is_visible + 1) % 2)

def togglePointNormals():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointNormals():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPointNormals((is_visible + 1) % 2)

def togglePointNumbers():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPointNumbers():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPointNumbers((is_visible + 1) % 2)

def togglePrimNumbers():
    is_visible = 0
    displaySets = getDisplaySets()
    for displaySet in displaySets:
        if displaySet.isShowingPrimNumbers():
            is_visible = 1
    for displaySet in displaySets:
        displaySet.showPrimNumbers((is_visible + 1) % 2)

def toggleSplitMaximized():
    pane = hou.ui.paneUnderCursor()
    is_maximized = 0
    if pane.isSplitMaximized():
        is_maximized = 1
    pane.setIsSplitMaximized((is_maximized + 1) % 2)

def toggleStowbars():
    is_hidden = hou.ui.hideAllMinimizedStowbars()
    hou.ui.setHideAllMinimizedStowbars(not is_hidden)

def toggleVectors():
    viewers = get_scene_viewers()
    for viewer in viewers:
        viewports = viewer.viewports()
        for viewport in viewports:
            settings = viewport.settings()
            vector_scale = settings.vectorScale()
            if vector_scale == 1:
                settings.setVectorScale(0)
            elif vector_scale == 0:
                settings.setVectorScale(1)
            else:
                settings.setVectorScale(1)

def toggleViewerToolbars():
    viewer = getSceneViewers()[0]
    state1 = viewer.isShowingOperationBar()
    state2 = viewer.isShowingDisplayOptionsBar()
    state3 = viewer.isShowingSelectionBar()
    if state1 + state2 + state3 > 0:
        viewer.showOperationBar(0)
        viewer.showDisplayOptionsBar(0)
        viewer.showSelectionBar(0)
    else:
        viewer.showOperationBar(1)
        viewer.showDisplayOptionsBar(1)
        viewer.showSelectionBar(1)


## Trigger

def triggerUpdate():
    hou.ui.triggerUpdate()


## Update

def updateMainMenubar():
    hou.ui.updateMainMenuBar()

def updateModeAuto():
    hou.setUpdateMode(hou.updateMode.AutoUpdate)

def updateModeManual():
    hou.setUpdateMode(hou.updateMode.Manual)



