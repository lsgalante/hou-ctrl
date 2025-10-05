import hou


class HCNetworkEditor:
    def __init__(self, tab):
        pass

    def addNetworkBox(self):
        # self.update()
        networkBox = self.pwd().createNetworkBox()
        networkBox.setPosition(self.currentNode().position())

    def addStickyNote(self):
        stickyNote = self.pwd().createStickyNote()
        cursor_pos = self.cursorPosition()
        stickyNote.setPosition(cursor_pos)
        stickyNote.setColor(hou.Color(0.71, 0.78, 1.0))

    # def connectNode(self):
    # return
    # choices = ("a", "b", "c")
    # popup = hou.ui.selectFromList(choices)

    def nextGrid(self):
        mode = int(self.getPref("gridmode"))
        mode = (mode + 1) % 3
        self.setPref("gridmode", mode)

    def deselectAll(self):
        self.currentNode().setSelected(False)

    def renameNode(self):
        node = self.currentNode()
        name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
        if name[0] == 0:
            node.setName(name[1])

    # def rotateNodeInputs(self):
    # return
    # node = self.currentNode()
    # connectors = node.inputConnectors()

    def selectDisplayNode(self):
        self.pwd().setCurrent(True, True)

    def toggleDimUnusedNodes(self):
        dim = int(self.getPref("dimunusednodes"))
        self.setPref("dimunusednodes", str(not dim))

    def toggleLocating(self):
        self.setLocatingEnabled(not self.locatingEnabled())

    def toggleMenu(self):
        visible = int(self.getPref("showmenu"))
        self.setPref("showmenu", str(not visible))

    def toggleGridPoints(self):
        visible = int(self.getPref("gridmode"))
        self.setPref("gridmode", str(not visible))
