import hou
from hclib import HCGlobal, HCPane, HCSceneViewer, HCTab

"""
Notes: tab object is retrieved by calling kwargs["pane"]
"""

def createItem(label="label", pos=0, submenu=False, script='script'):
    item = hou.ui.createRadialItem(submenu=submenu)
    item.setLabel(label)
    item.setScript(script)
    hou.ui.injectRadialItem(pos, item)

"""
Viewer menu
"""

def viewerRadialMain(**kwargs):
    menu = hou.ui.createRadialMenu('hcviewerradial', "HC Viewer Radial")
    createItem(
        pos=0,
        label="Keycam",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).keycam()'
    )
    createItem(
        pos=7,
        label="Display bar",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).toggleDisplayOptionsToolbar()'
    )
    createItem(
        pos=6,
        label="Operation bar",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).toggleOperationBar()'
    )
    createItem(
        pos=5,
        label="Selection bar",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).toggleSelectionBar()'
    )
    createItem(
        pos=4,
        label="UI",
        submenu=True, script='from hclib import hcradialutils; hcradialutils.viewerRadialUI()'
    )
    return menu

def viewerRadialLayout(**kwargs):
    menu = hou.ui.createRadialMenu('hcviewerradial', "HC Viewer Radial")
    createItem(
        pos=0,
        label="DoubleSide",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("DoubleSide")'
    )
    createItem(
        pos=1,
        label="DoubleStack",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("DoubleStack")'
    )
    createItem(
        pos=2,
        label="Quad",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("Quad")'
    )
    createItem(
        pos=3,
        label="QuadBottomSplit",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("QuadBottomSplit")'
    )
    createItem(
        pos=4,
        label="QuadLeftSplit",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("QuadLeftSplit")'
    )
    createItem(
        pos=5,
        label="Single",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("Single")'
    )
    createItem(
        pos=6,
        label="TripleBottomSplit",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("TripleBottomSplit")'
    )
    createItem(
        pos=7,
        label="TripleLeftSplit",
        script='from hclib import HCSceneViewer; HCSceneViewer(kwargs["pane"]).setLayout("TripleLeftSplit")'
    )
    return menu

def viewerRadialUI(**kwargs):
    menu = hou.ui.createRadialMenu('hcviewerradial', "HC Viewer Radial")
    createItem(
        pos=0,
        label="Pane tabs",
        script='from hclib import HCTab; HCTab(kwargs["pane"]).hcPane().toggleTabs()'
    )
    createItem(
        pos=7,
        label="Pane path",
        script='from hclib import HCTab; HCTab(kwargs["pane"]).toggleNetworkControls()'
    )
    createItem(
        pos=6,
        label="Pane maximize",
        script='from hclib import HCTab; HCTab(kwargs["pane"]).hcPane().toggleMaximize()'
    )
    createItem(
        pos=5,
        label="Global tabs",
        script='from hclib import HCGlobal; HCGlobal().toggleTabs()'
    )
    createItem(
        pos=4,
        label="Global paths",
        script='from hclib import HCGlobal; HCGlobal().toggleNetworkControls()'
    )
    createItem(
        pos=3,
        label="Stowbars",
        script='from hclib import HCGlobal; HCGlobal().toggleStowbars()'
    )
    createItem(
        pos=2,
        label="Layout",
        submenu=True, script='from hclib import hcradialutils; hcradialutils.viewerRadialLayout()'
    )
    return menu


def editorRadialMain(**kwargs):
    menu = hou.ui.createRadialMenu('hceditorradial', "HC Editor Radial")
    createItem(
        pos=0,
        label="Menu",
        script='from hclib import HCNetworkEditor; HCNetworkEditor(kwargs["pane"]).toggleMenu()'
    )
    createItem(
        pos=7,
        label="Frame all",
        script='from hclib import HCNetworkEditor; HCNetworkEditor(kwargs["pane"]).frameAll()'
    )
    createItem(
        pos=1,
        submenu=True,
        label="UI",
        script='from hclib import hcradialutils; hcradialutils.editorRadialUI()'
    )
    return menu

def editorRadialUI(**kwargs):
    menu = hou.ui.createRadialMenu('hceditorradial', "HC Editor Radial")
    createItem(
        pos=0,
        label="Pane tabs",
        script='from hclib import HCTab; HCTab(kwargs["pane"]).hcPane().toggleTabs()'
    )
    createItem(
        pos=1,
        label="Pane Maximize",
        script='from hclib import HCTab; HCTab(kwargs["pane"]).hcPane().toggleMaximize()'
    )
    createItem(
        pos=2,
        label="Pane path",
        script='from hclib import HCTab; HCTab(kwargs["pane"]).toggleNetworkControls()'
    )
    createItem(
        pos=3,
        label="Global tabs",
        script='from hclib import HCGlobal; HCGlobal().toggleTabs()'
    )
    createItem(
        pos=4,
        label="Global paths",
        script='from hclib import HCGlobal; HCGlobal().toggleNetworkControls()'
    )
    createItem(
        pos=5,
        label="Stowbars",
        script='from hclib import HCGlobal; HCGlobal().toggleStowbars()'
    )
    return menu
