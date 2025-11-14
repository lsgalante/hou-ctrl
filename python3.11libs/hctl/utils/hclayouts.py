import ..core.hcglobal as hcglobal

def setLayoutQuad(self, hc_global):
    hc_global.clearLayout()
    hc_global.tabs()[0].setType(hou.paneTabType.PythonShell)
    hc_global.panes()[0].splitHorizontally()
    hc_global.panes()[0].splitVertically()
    hc_global.panes()[1].splitVertically()

def setLayoutRamp(self, hc_global):
    hc_global.removeEventLoopCallbacks()
    hc_global.clearLayout()
    hc_global.panes()[0].splitVertically()
    hc_global.paneTabs()[1].setType(hou.paneTabType.Parm)
    hc_global.panes()[1].setSplitRatio(0.3)
    hc_global.panes()[1].createTab()

def setLayoutTriH(self):
    hc_global.removeEventLoopCallbacks()
    hc_global.clearLayout()
    # Make panes
    hc_global.tabs()[0].setType(hou.paneTabType.PythonShell)
    hc_global.panes()[0].splitHorizontally()
    hc_global.panes()[1].splitHorizontally()
    # Make paneTabs
    hc_global.panes()[1].createTab(hou.paneTabType.PythonShell)
    hc_global.panes()[1].tabs()[0].setIsCurrentTab()
    # Set types
    hc_global.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
    hc_global.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
    hc_global.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
    hc_global.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
    # Ratios
    hc_global.panes()[0].setSplitFraction(0.5)
    hou.session.last_pane = self.pane()
    hou.ui.addEventLoopCallback(triHCallback)

def triHCallback(hc_global):
    panes = hc_global.panes()
    pane = hc_global.pane()
    if str(pane) != str(hou.session.lastPane):
        hou.session.last_pane = pane
        if str(pane) == str(panes[1]):
            pane.setSplitFraction(0.6)
        elif str(pane) == str(panes[2]):
            pane.setSplitFraction(0.3)
    return True

def setLayoutTriV(hc_global):
    # Remove callbacks
    hc_global.removeEventLoopCallbacks()
    # Reset layout
    hc_global.clearLayout()
    # Make panes
    hc_global.panes()[0].tabs()[0].setType(hou.paneTabType.PythonShell)
    hc_global.panes()[0].splitHorizontally()
    hc_global.panes()[1].splitVertically()
    # Make pane tabs
    hc_global.panes()[1].createTab(hou.paneTabType.PythonShell)
    hc_global.panes()[1].tabs()[0].setIsCurrentTab()
    # Set types
    hc_global.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
    hc_global.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
    hc_global.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
    hc_global.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
    # Set ratios
    hc_global.panes()[0].setSplitFraction(0.66)
    # Ok
    hou.session.last_pane = self.pane()
    hou.ui.addEventLoopCallback(self.triVCallback)

def triVCallback(hc_global):
    panes = hc_global.panes()
    pane = hc_global.pane()
    if str(pane) != str(hou.session.last_pane):
        hou.session.last_pane = pane
        if str(pane) == str(panes[0]):
            pane.setSplitFraction(0.7)
        elif str(pane) == str(panes[1]):
            panes[0].setSplitFraction(0.4)
            pane.setSplitFraction(0.33)
        elif str(pane) == str(panes[2]):
            panes[0].setSplitFraction(0.4)
            pane.setSplitFraction(0.66)
    return True
