import hou

class HCSession():
    def __init__(self):
        return

    def autosave(self):
        return hou.getPreference("autoSave")

    def clearLayout(self):
        paneTabs = self.paneTabs()
        for paneTab in paneTabs:
            if paneTab != paneTabs[0]:
                paneTab.close()
        # self.paneOnly(paneTab.pane())
        # self.paneTabOnly(paneTab)
        # self.update()

    def colorEditor(self):
        hou.ui.selectColor()

    def desktop(self):
        return hou.ui.curDesktop()

    def floatingParameterEditor(self):
        paneTab = self.paneTab()
        if paneTab.type() == hou.paneTabType.NetworkEditor:
            hou.ui.showFloatingParameterEditor(self.node())
        else:
            hou.ui.setStatusMessage("Not a network editor", hou.severityType.Error)

    def hCPanel(self):
        from ..ui.hcpanel import HCPanel
        from .hcpanetab import HCPaneTab
        mainWindow = hou.qt.mainWindow()
        children = mainWindow.children()
        for child in children:
            if isinstance(child, HCPanel):
                child.close()
                # return
        hCPaneTab = HCPaneTab(self.paneTab())
        HCPanel(hCPaneTab).show()

    def hideShelf(self):
        self.desktop().shelfDock().show(0)

    def keycam(self):
        sceneViewer = self.sceneViewers()[0]
        category = sceneViewer.pwd().childTypeCategory().name()
        if category == "Object":
            sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam in an obj/object context")
        elif category== "Sop":
            sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam in a sop/geometry context")
        elif category== "Lop":
            sceneViewer.setCurrentState("keycam")
            hou.ui.setStatusMessage("Entered keycam in a lop context")
        else:
            hou.ui.setStatusMessage("Keycam is only available in obj, sop and lop contexts", hou.severityType.Error)


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
        for paneTab in self.paneTabs():
            if paneTab.type() == hou.paneTabType.NetworkEditor:
                editors.append(paneTab)
        return editors


    def node(self):
        return self.paneTab().currentNode()


    def openFile(self):
        hou.ui.selectFile()


    def pane(self):
        return hou.ui.paneUnderCursor()


    def panes(self):
        return self.desktop().panes()


    def paneTab(self):
        return hou.ui.paneTabUnderCursor()


    def paneTabs(self):
        return self.desktop().paneTabs()


    def projectPath(self):
        return hou.hipFile.path()


    def reloadColorSchemes(self):
        hou.ui.reloadColorScheme()
        hou.ui.reloadViewportColorSchemes()


    def reloadHotkeys(self):
        from ..input.hcbindings import load
        load()


    def reloadKeycam(self):
        hou.ui.reloadViewerState("keycam")


    def removeEventLoopCallbacks(self):
        callbacks = hou.ui.eventLoopCallbacks()
        for callback in callbacks:
            hou.ui.removeEventLoopCallback(callback)


    def restartHoudini(self):
        # import os
        # import subprocess
        # executable = sys.argv[0]
        # executable = os.environ.get("HFS") + "/bin/houdini"
        # subprocess.Popen([executable])
        # hou.exit()
        return


    def sceneViewers(self):
        scene_viewers = []
        for paneTab in self.paneTabs():
            if paneTab.type() == hou.paneTabType.SceneViewer:
                scene_viewers.append(paneTab)
        return scene_viewers


    def setLayoutQuad(self):
        self.clearLayout()
        self.paneTabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[0].splitVertically()
        self.panes()[1].splitVertically()


    def setLayoutRamp(self):
        self.removeEventLoopCallbacks()
        self.clearLayout()
        self.panes()[0].splitVertically()
        self.paneTabs()[1].setType(hou.paneTabType.Parm)
        self.panes()[1].setSplitRatio(0.3)
        self.panes()[1].createTab()


    def setLayoutTriH(self):
        self.removeEventLoopCallbacks()
        self.clearLayout()
        # Make panes
        self.paneTabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[1].splitHorizontally()
        # Make paneTabs
        self.panes()[1].createTab(hou.paneTabType.PythonShell)
        self.panes()[1].tabs()[0].setIsCurrentTab()
        # Set types
        self.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
        self.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
        self.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
        # Ratios
        self.panes()[0].setSplitFraction(0.5)
        hou.session.lastPane = self.pane()
        hou.ui.addEventLoopCallback(self.triHCallback)


    def status(self):
        from ..ui.hcstatuspanel import HCStatusPanel
        panel = HCStatusPanel()
        panel.show()


    def triHCallback():
        panes = self.panes()
        pane = self.pane()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[1]):
                pane.setSplitFraction(0.6)
            elif str(pane) == str(panes[2]):
                pane.setSplitFraction(0.3)
        return True


    def setLayoutTriV(self):
        # Remove other callbacks
        self.removeEventLoopCallbacks()
        # Reset pane layout
        self.clearLayout()
        # Make panes
        self.panes()[0].tabs()[0].setType(hou.paneTabType.PythonShell)
        self.panes()[0].splitHorizontally()
        self.panes()[1].splitVertically()
        # Make pane tabs
        self.panes()[1].createTab(hou.paneTabType.PythonShell)
        self.panes()[1].tabs()[0].setIsCurrentTab()
        # Set types
        self.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
        self.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
        self.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
        self.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
        # Set ratios
        self.panes()[0].setSplitFraction(0.66)
        # Ok
        hou.session.lastPane = self.pane()
        hou.ui.addEventLoopCallback(self.triVCallback)


    def triVCallback(self):
        panes = self.panes()
        pane = self.pane()
        if str(pane) != str(hou.session.lastPane):
            hou.session.lastPane = pane
            if str(pane) == str(panes[0]):
                pane.setSplitFraction(0.7)
            elif str(pane) == str(panes[1]):
                panes[0].setSplitFraction(0.4)
                pane.setSplitFraction(0.33)
            elif str(pane) == str(panes[2]):
                panes[0].setSplitFraction(0.4)
                pane.setSplitFraction(0.66)
        return True


    def setUpdateModeAuto(self):
        hou.setUpdateMode(hou.updateMode.AutoUpdate)


    def setUpdateModeManual(self):
        hou.setUpdateMode(hou.updateMode.Manual)


    def showShelf(self):
        self.shelfDock().show(1)


    def toggleMainMenuBar(self):
        if hou.getPreference("showmenu.val") == "1":
            hou.setPreference("showmenu.val", "0")
        else:
            hou.setPreference("showmenu.val", "1")


    def toggleMenus(self):
        visible = 0
        panes = self.panes()
        paneTabs = self.paneTabs()
        editors = self.networkEditors()
        sceneViewers = self.sceneViewers()
        # Main menu
        if hou.getPreference("showmenu.val") == "1":
            visible = 1
        # Network editor menu
        elif any(editor.getPref("showmenu") == "1" for editor in editors):
            visible = 1
        # Network controls
        elif any(paneTab.isShowingNetworkControls() for paneTab in paneTabs):
            visible = 1
        # Scene viewer toolbars (top, right, left)
        elif any(sceneViewer.isShowingOperationBar() for sceneViewer in sceneViewers):
            visible = 1
        elif any(sceneViewer.isShowingDisplayOptionsBar() for sceneViewer in sceneViewers):
            visible = 1
        elif any(sceneViewer.isShowingSelectionBar() for sceneViewer in sceneViewers):
            visible = 1
        # Panetabs
        elif any(pane.isShowingPaneTabs() for pane in panes):
            visible = 1

        # Set state
        hou.setPreference("showmenu.val", str(not visible))
        for editor in editors:
            editor.setPref("showmenu", str(not visible))
        for paneTab in paneTabs:
            paneTab.showNetworkControls(not visible)
        for pane in panes:
            pane.showPaneTabs(not visible)
        for viewer in sceneViewers:
            viewer.showOperationBar(not visible)
            viewer.showDisplayOptionsBar(not visible)
            viewer.showSelectionBar(not visible)
        hou.ui.setHideAllMinimizedStowbars(visible)
        hou.ui.setHideAllMinimizedStowbars(visible)


    def toggleNetworkControls(self):
        visible = 0
        paneTabs = self.paneTabs()
        for paneTab in paneTabs:
            if paneTab.isShowingNetworkControls():
                visible = 1
        for paneTab in paneTabs:
            paneTab.showNetworkControls(not visible)


    def toggleTabs(self):
        print("x")
        visible = 0
        panes = self.panes()
        for pane in panes:
            if pane.isShowingPaneTabs():
                visible = 1
        for pane in panes:
            pane.showPaneTabs(not visible)


    def toggleStowbars(self):
        hidden = hou.ui.hideAllMinimizedStowbars()
        hou.ui.setHideAllMinimizedStowbars(not hidden)


    def triggerUpdate(self):
        hou.ui.triggerUpdate()


    def toggleAutoSave(self):
        if hou.getPreference("autoSave"):
            hou.setPreference("autoSave", "0")
        else:
            hou.setPreference("autoSave", "1")


    def updateMainMenuBar(self):
        hou.ui.updateMainMenuBar()


    def viewports(self):
        viewports = []
        sceneViewers = self.sceneViewers
        for sceneViewer in sceneViewers:
            for viewport in sceneViewer.viewports():
                viewports.append(viewport)
        return(viewports)
