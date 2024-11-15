import hou

def color_editor_open():
    hou.ui.selectColor()

def color_scheme_reload():
    hou.ui.reloadColorScheme()
    hou.ui.reloadViewportColorSchemes()

def houdini_restart():
    x=1

def keycam_reload():
    hou.ui.reloadViewerState("keycam")

def keycam_toggle():
    viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)
    if viewer != None:
        node = viewer.pwd()
        type = node.childTypeCategory().name()
        if type == "Object" or type == "Sop":
            viewer.setCurrentState("keycam")
        else:
            print("Only Sop or Obj contexts are available.")
    else:
        print("No available scene viewer.")
        return

def main_menu_update():
    hou.ui.updateMainMenuBar()

def menubar_toggle():
    show = 1
    if hou.getPreference("showmenu.val") == "1":
        show = 0
    hou.setPreference("showmenu.val",["0","1"][show])

def menubar_update():
    hou.ui.updateMainMenuBar()

def network_ctrl_toggle():
    tabs = hou.ui.paneTabs()
    show = 1
    for tab in tabs:
        if tab.isShowingNetworkControls():
            show = 0
    [tab.showNetworkControls(show) for tab in tabs]
    
def network_menu_toggle():
    tabs = hou.ui.paneTabs()
    show = 1
    for tab in tabs:
        if tab.type() == hou.paneTabType.NetworkEditor:
            if tab.getPref("showmenu") == "1":
                show = 0
    for tab in tabs:
        if tab.type() == hou.paneTabType.NetworkEditor:
            tab.setPref("showmenu",["0","1"][show])
            
def shelf_hide():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(0)

def shelf_show():
    desktop = hou.ui.curDesktop()
    desktop.shelfDock().show(1)

def stowbar_toggle():
    hide = hou.ui.hideAllMinimizedStowbars()
    hou.ui.setHideAllMinimizedStowbars(not hide)

def tab_toggle():
    panes = hou.ui.curDesktop().panes()
    show = 1
    for pane in panes:
        if pane.isShowingPaneTabs():
            show = 0
    [pane.showPaneTabs(show) for pane in panes]
    
def update_mode_auto():
    hou.setUpdateMode(hou.updateMode.AutoUpdate)
    
def update_mode_manual():
    hou.setUpdateMode(hou.updateMode.Manual)

def update_trigger():
    hou.ui.triggerUpdate()
