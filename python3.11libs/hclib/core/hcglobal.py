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
        network_editors = []
        for tab in self.tabs():
            if tab.type() == hou.paneTabType.NetworkEditor:
                network_editors.append(tab)
        return network_editors

    def pane(self):
        return hou.ui.paneUnderCursor()

    def panes(self):
        return self.desktop().panes()

    def sceneViewers(self):
        scene_viewers = []
        for tab in self.tabs():
            if tab.type() == hou.paneTabType.SceneViewer:
                scene_viewers.append(tab)
        return scene_viewers

    ## tab and tabs functions intentionally do not use the hou.ui.paneTabUnderCursor method
    def tab(self):
        return self.pane().currentTab()

    def tabs(self):
        return self.pane().tabs()

    def viewports(self):
        viewports = []
        scene_viewers = self.sceneViewers
        for scene_viewer in scene_viewers:
            for viewport in scene_viewer.viewports():
                viewports.append(viewport)
        return viewports

    """
    Menus
    """

    def colorEditor(self):
        hou.ui.selectColor()

    def debugger(self):
        from ..ui.hcdebugger import HCDebugger

        hc_debugger= HCDebugger()
        hc_debugger.show()

    def floatingParameterEditor(self):
        tab = self.tab()
        if tab.type() == hou.paneTabType.NetworkEditor:
            hou.ui.showFloatingParameterEditor(self.node())
        else:
            hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)

    def hcPanel(self):
        from ..ui.hcpanel import HCPanel
        from .hctab import HCTab

        mainWindow = hou.qt.mainWindow()
        children = mainWindow.children()
        for child in children:
            if isinstance(child, HCPanel):
                child.close()
                # return
        hc_tab = HCTab(self.tab())
        panel = HCPanel(hc_tab)
        panel.show()

    def openFile(self):
        hou.ui.selectFile()

    """
    Utils
    """

    def autosave(self):
        return hou.getPreference('autoSave')

    def keycam(self):
        sceneViewer = self.sceneViewers()[0]
        category = sceneViewer.pwd().childTypeCategory().name()
        if category == "Object":
            sceneViewer.setCurrentState('keycam')
            hou.ui.setStatusMessage("Entered keycam in an obj/object context")
        elif category == "Sop":
            sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam in a sop/geometry context")
        elif category == "Lop":
            sceneViewer.setCurrentState('keycam')
            hou.ui.setStatusMessage("Entered keycam in a lop context")
        else:
            hou.ui.setStatusMessage(
                "Keycam is only available in obj, sop and lop contexts",
                hou.severityType.Error,
            )

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
        if hou.getPreference('showmenu.val') == '1':
            hou.setPreference("showmenu.val", '0')
        else:
            hou.setPreference("showmenu.val", '1')

    def toggleMenus(self):
        visible = 0
        panes = self.panes()
        tabs = self.tabs()
        network_editors = self.networkEditors()
        scene_viewers = self.sceneViewers()
        # Main menu
        if hou.getPreference('showmenu.val') == '1':
            visible = 1
        # Network editor menu
        elif any(network_editor.getPref('showmenu'') == '1' for network_editor in network_editors):
            visible = 1
        # Network controls
        elif any(tab.isShowingNetworkControls() for tab in tabs):
            visible = 1
        # Scene viewer toolbars (top, right, left)
        elif any(scene_viewer.isShowingOperationBar() for scene_viewer in scene_viewers):
            visible = 1
        elif any(
            scene_viewer.isShowingDisplayOptionsBar() for scene_viewer in scene_viewers
        ):
            visible = 1
        elif any(scene_viewer.isShowingSelectionBar() for scene_viewer in scene_viewers):
            visible = 1
        # Tabs
        elif any(pane.isShowingPaneTabs() for pane in panes):
            visible = 1

        # Set state
        hou.setPreference('showmenu.val', str(not visible))
        for network_editor in network_editors:
            network_editor.setPref('showmenu'', str(not visible))
        for tab in tabs:
            tab.showNetworkControls(not visible)
        for pane in panes:
            pane.showPaneTabs(not visible)
        for scene_viewer in scene_viewers:
            scene_viewer.showOperationBar(not visible)
            scene_viewer.showDisplayOptionsBar(not visible)
            scene_viewer.showSelectionBar(not visible)
        # Needs to be called twice for some reason
        hou.ui.setHideAllMinimizedStowbars(visible)
        hou.ui.setHideAllMinimizedStowbars(visible)

    def toggleNetworkControls(self):
        print('x')
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
