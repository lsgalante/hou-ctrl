import hou
from .hcglobal import HCGlobal


class HCPane:

    def __init__(self, pane):
        self.hc_global= HCGlobal()
        self.pane = pane

    ## PANE ##

    def close(self):
        for tab in self.tabs():
            tab.close()

    def isMaximized(self):
        return self.pane.isMaximized()

    def only(self):
        tabs = self.hc_global.tabs()
        tabs.remove(self.tab())
        for tab in tabs:
            tab.close()

    def qtScreenGeometry(self):
        return self.pane.qtScreenGeometry()

    def setIsMaximized(self, bool):
        self.pane.setIsMaximized(bool)

    def toggleMaximize(self):
        self.setIsMaximized(not self.isMaximized())

    # SPLIT

    def contract(self):
        fraction = round(self.splitFraction(), 3) + 0.1
        self.setSplitFraction(fraction)
        hou.ui.setStatusMessage("Pane fraction: " + str(fraction))

    def expand(self):
        fraction = round(self.splitFraction(), 3) - 0.1
        self.setSplitFraction(fraction)
        hou.ui.setStatusMessage("Pane fraction: " + str(fraction))

    def isSplitMaximized(self):
        return self.pane.isSplitMaximized()

    # def resize(self):
    # import hctl.ui.resizedialog
    # panel = hctl.ui.resizedialog.resizeWidget(self)
    # panel.show()

    def setIsSplitMaximized(self, bool):
        self.pane.setIsSplitMaximized(bool)

    def setRatioHalf(self):
        self.setSplitFraction(0.5)

    def setRatioQuarter(self):
        self.setSplitFraction(0.25)

    def setRatioThird(self):
        self.setSplitFraction(0.333)

    def setSplitFraction(self, fraction):
        self.pane.setSplitFraction(fraction)

    def splitFraction(self):
        return self.pane.getSplitFraction()

    def splitHorizontal(self):
        self.pane.splitHorizontally()

    def splitRotate(self):
        self.pane.splitRotate()

    def splitSwap(self):
        self.pane.splitSwap()

    def splitVertical(self):
        self.pane.splitVertically()

    def toggleSplitMaximized(self):
        self.setIsSplitMaximized(not self.isSplitMaximized())

    ## TABS ##

    def hcTab(self):
        from .hctab import HCTab

        return HCTab(self.tab())

    def isShowingTabs(self):
        return self.pane.isShowingPaneTabs()

    # def newTab(self):
    #     reload(hcnewpanetabmenu)
    #     newPaneTabMenu = hcnewpanetabmenu.newPaneTabMenu()
    #     newPaneTabMenu.show()

    def showTabs(self, bool):
        self.pane.showPaneTabs(bool)

    def tab(self):
        return self.pane.currentTab()

    def tabs(self):
        return self.pane.tabs()

    def toggleTabs(self):
        self.showTabs(not self.isShowingTabs())
