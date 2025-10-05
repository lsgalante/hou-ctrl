import hou
from .hcsession import HCSession


class HCPane:
    def __init__(self, pane):
        self.hCSession = HCSession()
        self.pane = pane

    def close(self):
        for paneTab in self.paneTabs():
            paneTab.close()

    def contract(self):
        fraction = self.splitFraction()
        fraction = round(fraction, 3) + 0.1
        hou.ui.setStatusMessage("Pane fraction: " + str(fraction))
        self.setSplitFraction(fraction)

    def expand(self):
        fraction = self.splitFraction()
        fraction = round(fraction, 3) - 0.1
        message = "Pane fraction: " + str(fraction)
        hou.ui.setStatusMessage(message)
        self.setSplitFraction(fraction)

    def isMaximized(self):
        return self.pane.isMaximized()

    def isShowingPaneTabs(self):
        return self.pane.isShowingPaneTabs()

    def isSplitMaximized(self):
        return self.pane.isSplitMaximized()

    # def newPaneTab(self):
    #     reload(hcnewpanetabmenu)
    #     newPaneTabMenu = hcnewpanetabmenu.newPaneTabMenu()
    #     newPaneTabMenu.show()

    def only(self):
        paneTabs = self.hCSession.paneTabs()
        paneTabs.remove(self.paneTab())
        for paneTab in paneTabs:
            paneTab.close()

    # def resize(self):
    # import hctl.ui.resizedialog
    # panel = hctl.ui.resizedialog.resizeWidget(self)
    # panel.show()

    def setIsMaximized(self, bool):
        self.pane.setIsMaximized(bool)

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

    def showPaneTabs(self, bool):
        self.pane.showPaneTabs(bool)

    def splitFraction(self):
        return self.pane.getSplitFraction()

    def splitHorizontally(self):
        self.pane.splitHorizontally()

    def splitRotate(self):
        self.pane.splitRotate()

    def splitSwap(self):
        self.pane.splitSwap()

    def splitVertically(self):
        self.pane.splitVertically()

    def paneTab(self):
        return self.pane.currentTab()

    def paneTabs(self):
        return self.pane.tabs()

    def toggleMaximized(self):
        self.setIsMaximized(not self.isMaximized())

    def togglePaneTabs(self):
        self.showPaneTabs(not self.isShowingPaneTabs())

    def toggleSplitMaximized(self):
        self.setIsSplitMaximized(not self.isSplitMaximized())
