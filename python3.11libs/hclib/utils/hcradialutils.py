import hou
from ..core.hcglobal import HCGlobal
from ..core.hcpane import HCPane
from ..core.hcsceneviewer import HCSceneViewer
from ..core.hctab import HCTab
from hclib import HCGlobal, HCTab, HCPane

"""
Notes:
tab object is retrieved by calling kwargs["pane"]
"""

"""
Viewer menu
"""

def viewerRadial(**kwargs):
    viewer_menu = hou.ui.createRadialMenu("hcviewerradial", "HC Viewer Radial")
    viewer = kwargs["pane"]
    hcviewer = HCSceneViewer(viewer)

    keycam_item = hou.ui.createRadialItem()
    keycam_item.setLabel("keycam")
    keycam_item.setScript('from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).keycam()')
    # keycam_item.setScript(keycam_script)
    hou.ui.injectRadialItem(0, keycam_item)
    return viewer_menu

def install_viewer_radial_menu(radialmenu, **kwargs):
    menu = {
        "n": {
            "type": "script_action",
            "label": "keycam",
            "script": viewer_keycam
        },
        "ne": {
            "type": "script_submenu",
            "label": "Pane actions",
            "script": viewer_pane_submenu
        },
        "e": {
            "type": "script_submenu",
            "label": "Global actions",
            "script": viewer_global_submenu
        },
        "se": {
            "type": "script_submenu",
            "label": "Viewport layout",
            "script": viewer_layout_submenu
        },
        "sw": {
            "type": "script_action",
            "label": "Operation bar",
            "script": viewer_operation_bar
        },
        "w": {
            "type": "script_action",
            "label": "Display bar",
            "script": viewer_display_bar
        },
        "nw": {
            "type": "script_action",
            "label": "Selection bar",
            "script": viewer_selection_bar
        }
    }

    radialmenu.setRadialMenu(menu)

def viewer_global_submenu(**kwargs):
    submenu = {
        "n": {
            "type": "script_action",
            "label": "Tabs",
            "script": global_tabs
        },
        "ne": {
            "type": "script_action",
            "label": "Paths",
            "script": global_paths
        },
        "e": {
            "type": "script_action",
            "label": "Stowbars",
            "script": global_stowbars
        }
    }
    radialmenu.setRadialMenu(submenu)

def viewer_pane_submenu(**kwargs):
    submenu = {
        "n": {
            "type": "script_action",
            "label": "Tabs",
            "script": pane_tabs
        },
        "ne": {
            "type": "script_action",
            "label": "Path",
            "script": pane_path
        },
        "e": {
            "type": "script_action",
            "label": "Maximize",
            "script": pane_maximize
        }
    }
    radialmenu.setRadialMenu(submenu)

def viewer_layout_submenu(**kwargs):
    submenu = {
        "n": {
            "type": "script_action",
            "label": "Single",
            "script": test
        },
        "ne": {
            "type": "script_action",
            "label": "Quad",
            "script": test
        },
        "e": {
            "type": "script_action",
            "label": "Double side",
            "script": test
        },
        "se": {
            "type": "script_action",
            "label": "Double stack",
            "script": test
        },
        "s": {
            "type": "script_action",
            "label": "Triple bottom split",
            "script": test
        },
        "sw": {
            "type": "script_action",
            "label": "Triple left split",
            "script": test
        },
        "w": {
            "type": "script_action",
            "label": "Quad bottom split",
            "script": test
        }
    }
    radialmenu.setRadialMenu(submenu)

"""
Editor menu
"""

def install_editor_radial_menu(radialmenu, **kwargs):
    return

"""
Menu functions
"""

def global_paths(**kwargs):
    HCGlobal().toggleNetworkControls()

def global_stowbars(**kwargs):
    HCGlobal().toggleStowbars()

def global_tabs(**kwargs):
    HCGlobal().toggleTabs()

def pane_maximize(**kwargs):
    HCTab(kwargs["pane"]).hcPane().toggleMaximize()

def pane_path(**kwargs):
    HCTab(kwargs["pane"]).toggleNetworkControls()

def pane_tabs(**kwargs):
    HCTab(kwargs["pane"]).hcPane().toggleTabs()

def viewer_display_bar(**kwargs):
    HCSceneViewer(kwargs["pane"]).toggleDisplayOptionsToolbar()

def viewer_keycam(**kwargs):
    HCSceneViewer(kwargs["pane"]).keycam()

def viewer_operation_bar(**kwargs):
    HCSceneViewer(kwargs["pane"]).toggleOperationBar()

def viewer_selection_bar(**kwargs):
    HCSceneViewer(kwargs["pane"]).toggleSelectionBar()
