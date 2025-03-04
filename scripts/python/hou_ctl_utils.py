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
    show_master = 1

    # main menu
    show_main_menu = int(hou.getPreference("showmenu.val"))
    # network menu
    show_network_menu = 0
    networks = getNetworks()
    for network in networks:
        show_network_menu += int(network.getPref("showmenu"))
    # path
    show_path = 0
    tabs = hou.ui.paneTabs()
    for tab in tabs:
        if tab.isShowingNetworkControls():
            show_path += 1
    # panetabs
    show_tabs = 0
    panes = hou.ui.curDesktop().panes()
    for pane in panes:
        if pane.isShowingPaneTabs():
            show_tabs += 1
    # viewer menus
    show_viewer_menus = 0
    viewer = getSceneViewers()[0]
    if viewer.isShowingOperationBar():
        show_viewer_menus += 1
    elif viewer.isShowingDisplayOptionsBar():
        show_viewer_menus += 1
    elif viewer.isShowingSelectionBar():
        show_viewer_menus += 1

    if int(show_main_menu) + show_path + show_tabs + show_viewer_menus > 0: show_master = 0
    else: show_master = 1

    hou.setPreference("showmenu.val",["0","1"][show_master])
    for network in networks: network.setPref("showmenu",["0","1"][show_master])
    [tab.showNetworkControls(show_master) for tab in tabs]
    [pane.showPaneTabs(show_master) for pane in panes]
    viewer.showOperationBar(show_master)
    viewer.showDisplayOptionsBar(show_master)
    viewer.showSelectionBar(show_master)
    
    hou.ui.setHideAllMinimizedStowbars(not show_master)
    return

def toggleAutosave():
    state = hou.getPreference("autoSave")
    if state == "0":
        hou.setPreference("autoSave", "1")
    elif state == "1":
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
    networks = getNetworks()
    dim = "1"
    for network in networks:
        pref = network.getPref("dimunusednodes")
        if pref == "1":
            dim = "0"
    for network in networks:
        network.setPref("dimunusednodes", dim) 

def toggleFinder():
    reload(hou_ctl_finder)
    finder = hou_ctl_finder.finder()
    finder.show()

def toggleGroupList():
    viewers = getSceneViewers()
    is_visible = 0
    for viewer in viewers:
        if viewer.isGroupListVisible():
            is_visible = 1
    if is_visible:
        for viewer in viewers:
            viewer.setGroupListVisible(0)
    else:
        for viewer in viewers:
            viewer.setGroupListVisible(1)

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
    val = hou.getPreference("showmenu.val")
    vals = ("0", "1")
    idx = vals.index(val)
    idx = (idx + 1) % 2
    hou.setPreference("showmenu.val",["0","1"][idx])

def toggleNetworkControls():
    tabs = hou.ui.paneTabs()
    show_path = 1
    for tab in tabs:
        if tab.isShowingNetworkControls():
            show_path = 0
    [tab.showNetworkControls(show_path) for tab in tabs]

def toggleNetworkGridPoints():
    networks = getNetworks()
    for network in networks:
        pref = network.getPref("gridmode")
        if pref != "1":
            network.setPref("gridmode", "1")
        else:
            network.setPref("gridmode", "0")

def toggleNetworkGridLines():
    networks = getNetworks()
    for network in networks:
        pref = network.getPref("gridmode")
        if pref != "2":
            network.setPref("gridmode", "2")
        else:
            network.setPref("gridmode", "0")

def toggleNetworkLocating():
    networks = getNetworks()
    is_locating = 0
    for network in networks:
        if network.locatingEnabled():
            is_locating = 1
    for network in networks:
        network.setLocatingEnabled(is_locating)

def toggleNetworkMenubar():
    networks = getNetworks()
    show_menu = 1
    for network in networks:
        if network.getPref("showmenu") == "1":
            show_menu = 0
    for network in networks:
        network.setPref("showmenu",["0","1"][show_menu])

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



