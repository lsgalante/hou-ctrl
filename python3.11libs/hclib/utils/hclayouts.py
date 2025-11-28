from ..core.hcglobal import HCGlobal

def setLayoutQuad(self, hcglobal):
    hcglobal.clearLayout()
    hcglobal.tabs()[0].setType(hou.paneTabType.PythonShell)
    hcglobal.panes()[0].splitHorizontally()
    hcglobal.panes()[0].splitVertically()
    hcglobal.panes()[1].splitVertically()

def setLayoutRamp(self, hc_global):
    hcglobal.removeEventLoopCallbacks()
    hcglobal.clearLayout()
    hcglobal.panes()[0].splitVertically()
    hcglobal.paneTabs()[1].setType(hou.paneTabType.Parm)
    hcglobal.panes()[1].setSplitRatio(0.3)
    hcglobal.panes()[1].createTab()

def setLayoutTriH(self):
    hcglobal.removeEventLoopCallbacks()
    hcglobal.clearLayout()
    # Make panes
    hcglobal.tabs()[0].setType(hou.paneTabType.PythonShell)
    hcglobal.panes()[0].splitHorizontally()
    hcglobal.panes()[1].splitHorizontally()
    # Make paneTabs
    hcglobal.panes()[1].createTab(hou.paneTabType.PythonShell)
    hcglobal.panes()[1].tabs()[0].setIsCurrentTab()
    # Set types
    hcglobal.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
    hcglobal.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
    hcglobal.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
    hcglobal.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
    # Ratios
    hcglobal.panes()[0].setSplitFraction(0.5)
    hou.session.last_pane = self.pane()
    hou.ui.addEventLoopCallback(triHCallback)

def triHCallback(hcglobal):
    panes = hcglobal.panes()
    pane = hcglobal.pane()
    if str(pane) != str(hou.session.lastPane):
        hou.session.last_pane = pane
        if str(pane) == str(panes[1]):
            pane.setSplitFraction(0.6)
        elif str(pane) == str(panes[2]):
            pane.setSplitFraction(0.3)
    return True

def setLayoutTriV(hcglobal):
    # Remove callbacks
    hcglobal.removeEventLoopCallbacks()
    # Reset layout
    hcglobal.clearLayout()
    # Make panes
    hcglobal.panes()[0].tabs()[0].setType(hou.paneTabType.PythonShell)
    hcglobal.panes()[0].splitHorizontally()
    hcglobal.panes()[1].splitVertically()
    # Make pane tabs
    hcglobal.panes()[1].createTab(hou.paneTabType.PythonShell)
    hcglobal.panes()[1].tabs()[0].setIsCurrentTab()
    # Set types
    hcglobal.panes()[0].tabs()[0].setType(hou.paneTabType.SceneViewer)
    hcglobal.panes()[1].tabs()[0].setType(hou.paneTabType.Parm)
    hcglobal.panes()[1].tabs()[1].setType(hou.paneTabType.DetailsView)
    hcglobal.panes()[2].tabs()[0].setType(hou.paneTabType.NetworkEditor)
    # Set ratios
    hcglobal.panes()[0].setSplitFraction(0.66)
    # Ok
    hou.session.last_pane = self.pane()
    hou.ui.addEventLoopCallback(self.triVCallback)

def triVCallback(hcglobal):
    panes = hcglobal.panes()
    pane = hcglobal.pane()
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
