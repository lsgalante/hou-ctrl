import hou
from importlib import reload
import hou_ctl_finder


## get

def get_autosave_state():
    return hou.getPreference("autoSave")

def get_current_node():
    tabs = hou.ui.paneTabs()
    tabs = [tab for tab in tabs if tab.type() == hou.paneTabType.NetworkEditor]
    node = tabs[0].currentNode()    
    return node

def get_networks():
    tabs     = hou.ui.paneTabs()
    networks = [tab for tab in tabs if tab.type() == hou.paneTabType.NetworkEditor]
    return networks

def get_scene_viewers():
    tabs    = hou.ui.paneTabs()
    viewers = [tab for tab in tabs if tab.type() == hou.paneTabType.SceneViewer]
    return viewers

## hide

def hide_shelf():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(0)

## node

def node_rotate_inputs():
    node = get_current_node()
    connectors = node.inputConnectors()

## open

def open_color_editor():
    hou.ui.selectColor()

def open_hotkey_editor():
    print("open hotkey editor")

## reload

def reload_color_schemes():
    hou.ui.reloadColorScheme()
    hou.ui.reloadViewportColorSchemes()

def reload_keycam():
    hou.ui.reloadViewerState("keycam")

## rename

def rename_node():
    node = get_current_node()
    name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
    if name[0] == 0:
        node.setName(name[1])

## restart

def restart_houdini():
    return

## show

def show_shelf():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(1)

## toggle

def toggle_all_menus():
    show_master = 1

    # main menu
    show_main_menu = int(hou.getPreference("showmenu.val"))
    # network menu
    show_network_menu = 0
    networks = get_networks()
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
    viewer = get_scene_viewers()[0]
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

def toggle_autosave():
    state  = hou.getPreference("autoSave")
    states = ("0", "1")
    idx    = (states.index(state) + 1) % 2
    hou.setPreference("autosave", states[idx])

def toggle_dim_unused_nodes():
    networks = get_networks()
    dim = "1"
    for network in networks:
        pref = network.getPref("dimunusednodes")
        if pref == "1":
            dim = "0"
    for network in networks:
        network.setPref("dimunusednodes", dim) 

def toggle_finder():
    reload(hou_ctl_finder)
    finder = hou_ctl_finder.finder()
    finder.show()

def toggle_keycam():
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

def toggle_main_menubar():
    val  = hou.getPreference("showmenu.val")
    vals = ("0", "1")
    idx  = (vals.index(val) + 1) % 2
    hou.setPreference("showmenu.val",["0","1"][vals[idx]])

def toggle_network_locating():
    networks = get_networks()
    is_locating = 0
    for network in networks:
        if network.locatingEnabled():
            is_locating = 1
    for network in networks:
        network.setLocatingEnabled(is_locating)

def toggle_network_menubar():
    networks = get_networks()
    show_menu = 1
    for network in networks:
        if network.getPref("showmenu") == "1":
            show_menu = 0
    for network in networks:
        network.setPref("showmenu",["0","1"][show_menu])

def toggle_panetabs():
    panes = hou.ui.curDesktop().panes()
    show = 1
    for pane in panes:
        if pane.isShowingPaneTabs():
            show = 0
    [pane.showPaneTabs(show) for pane in panes]

def toggle_path():
    tabs = hou.ui.paneTabs()
    show_path = 1
    for tab in tabs:
        if tab.isShowingNetworkControls():
            show_path = 0
    [tab.showNetworkControls(show_path) for tab in tabs]

def toggle_point_markers():
    viewers = get_scene_viewers()
    for viewer in viewers:
        viewports = viewer.viewports()
        print(viewports)

def toggle_stowbars():
    hide = hou.ui.hideAllMinimizedStowbars()
    hou.ui.setHideAllMinimizedStowbars(not hide)

def toggle_vectors():
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

def toggle_viewer_toolbars():
    viewer = get_scene_viewers[0]
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

## trigger

def trigger_update():
    hou.ui.triggerUpdate()

## update

def update_main_menubar():
    hou.ui.updateMainMenuBar()

def update_mode_auto():
    hou.setUpdateMode(hou.updateMode.AutoUpdate)

def update_mode_manual():
    hou.setUpdateMode(hou.updateMode.Manual)

