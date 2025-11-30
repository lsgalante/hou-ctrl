import hou


class HCGlobal:
    def __init__(self):
        return

    """
    Context
    """

    def node(self):
        return self.tab().currentNode()

    """
    Layout
    """

    def clearLayout(self):
        tabs = self.tabs()
        for tab in tabs:
            if tab != tabs[0]:
                tab.close()

    def desktop(self):
        return hou.ui.curDesktop()

    def hcPane(self):
        from .hcpane import HCPane

        return HCPane(self.pane())

    def hcTab(self):
        from .hctab import HCTab

        return HCTab(self.pane())

    def layout(self):
        lefts = []
        tops = []
        for pane in self.panes():
            geo = pane.qtScreenGeometry()
            lefts.append(geo.left())
            tops.append(geo.top())
        print(lefts)
        print(tops)

    def networkEditors(self):
        editors = []
        for tab in self.tabs():
            if tab.type() == hou.paneTabType.NetworkEditor:
                editors.append(tab)
        return editors

    def pane(self):
        return hou.ui.paneUnderCursor()

    def panes(self):
        return self.desktop().panes()

    def sceneViewers(self):
        viewers = []
        for tab in self.tabs():
            if tab.type() == hou.paneTabType.SceneViewer:
                viewers.append(tab)
        return viewers

    ## tab and tabs functions intentionally do not use the hou.ui.paneTabUnderCursor method
    def tab(self):
        return self.pane().currentTab()

    def tabs(self):
        return self.pane().tabs()

    def viewports(self):
        viewports = []
        viewers = self.sceneViewers
        for viewer in viewers:
            for viewport in viewer.viewports():
                viewports.append(viewport)
        return viewports

    """
    Menus
    """

    def colorEditor(self):
        hou.ui.selectColor()

    def floatingParameterEditor(self):
        tab = self.tab()
        if tab.type() == hou.paneTabType.NetworkEditor:
            hou.ui.showFloatingParameterEditor(self.node())
        else:
            hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)

    def openFile(self):
        hou.ui.selectFile()

    """
    Utils
    """

    def autosave(self):
        return hou.getPreference('autoSave')

    def keycam(self):
        msgmap = {
            "Object": "Entered keycam in an obj/object context",
            "Sop": "Entered keycam in a sop/geometry context",
            "Lop": "Entered keycam in a lop context"
        }
        viewer = self.sceneViewers()[0]
        category = viewer.pwd().childTypeCategory().name()
        if category in msgmap:
            viewer.setCurrentState('keycam')
            hou.ui.setStatusMessage(msgmap[category])
        else:
            hou.ui.setStatusMessage("Keycam is only available in obj, sop and lop contexts",
                hou.severityType.Error)

    def projectPath(self):
        return hou.hipFile.path()

    def reloadColorSchemes(self):
        hou.ui.reloadColorScheme()
        hou.ui.reloadViewportColorSchemes()

    def reloadHotkeys(self):
        from ..utils.hcbindings import load

        load()

    def reloadKeycam(self):
        hou.ui.reloadViewerState('keycam')

    def removeEventLoopCallbacks(self):
        callbacks = hou.ui.eventLoopCallbacks()
        for callback in callbacks:
            hou.ui.removeEventLoopCallback(callback)

    # def restartHoudini(self):
        # import os
        # import subprocess
        # executable = sys.argv[0]
        # executable = os.environ.get("HFS") + "/bin/houdini"
        # subprocess.Popen([executable])
        # hou.exit()
        # return

    def setUpdateModeAuto(self):
        hou.setUpdateMode(hou.updateMode.AutoUpdate)

    def setUpdateModeManual(self):
        hou.setUpdateMode(hou.updateMode.Manual)

    def triggerUpdate(self):
        hou.ui.triggerUpdate()

    def toggleAutoSave(self):
        map = {'0': '1', '1': '0'}
        hou.setPreference('autoSave', map[hou.getPreference('autoSave')])

    def updateMainMenuBar(self):
        hou.ui.updateMainMenuBar()

    """
    Visibility
    """

    def hideShelf(self):
        self.desktop().shelfDock().show(0)

    def showShelf(self):
        self.shelfDock().show(1)

    def toggleMainMenuBar(self):
        map = {'1': '0', '0': '1'}
        hou.setPreference('showmenu.val', map[hou.getPreference('showmenu.val')])

    def toggleMenus(self):
        visible = 0
        panes = self.panes()
        tabs = self.tabs()
        editors = self.networkEditors()
        viewers = self.sceneViewers()
        ## Main menu
        if hou.getPreference('showmenu.val') == '1':
            visible = 1
        ## Network editor menu
        elif any(editor.getPref('showmenu') == '1' for editor in editors):
            visible = 1
        ## Network controls
        elif any(tab.isShowingNetworkControls() for tab in tabs):
            visible = 1
        ## Scene viewer toolbars (top, right, left)
        elif any(viewer.isShowingOperationBar() for viewer in viewers):
            visible = 1
        elif any(viewer.isShowingDisplayOptionsBar() for viewer in viewers):
            visible = 1
        elif any(viewer.isShowingSelectionBar() for viewer in viewers):
            visible = 1
        ## Tabs
        elif any(pane.isShowingPaneTabs() for pane in panes):
            visible = 1

        ## Set state
        hou.setPreference('showmenu.val', str(not visible))
        for editor in editors:
            editor.setPref('showmenu', str(not visible))
        for tab in tabs:
            tab.showNetworkControls(not visible)
        for pane in panes:
            pane.showPaneTabs(not visible)
        for viewer in viewers:
            viewer.showOperationBar(not visible)
            viewer.showDisplayOptionsBar(not visible)
            viewer.showSelectionBar(not visible)
        ## Needs to be called twice for some reason
        hou.ui.setHideAllMinimizedStowbars(visible)
        hou.ui.setHideAllMinimizedStowbars(visible)

    def toggleNetworkControls(self):
        visible = 0
        tabs = self.tabs()
        for tab in tabs:
            if tab.isShowingNetworkControls():
                visible = 1
        for tab in tabs:
            tab.showNetworkControls(not visible)

    def toggleStowbars(self):
        hidden = hou.ui.hideAllMinimizedStowbars()
        hou.ui.setHideAllMinimizedStowbars(not hidden)

    def toggleTabs(self):
        visible = 0
        panes = self.panes()
        for pane in panes:
            if pane.isShowingPaneTabs():
                visible = 1
        for pane in panes:
            pane.showPaneTabs(not visible)
