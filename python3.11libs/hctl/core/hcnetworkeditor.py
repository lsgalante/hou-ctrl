import hou
import types

def addFunctions(hc_tab):
    hc_tab.addNetworkBox = types.MethodType(addNetworkBox, hc_tab)
    hc_tab.addStickyNote = types.MethodType(addStickyNote, hc_tab)
    hc_tab.nextGridMode = types.MethodType(nextGrid, hc_tab)
    hc_tab.deselectAll = types.MethodType(nextGrid, hc_tab)
    hc_tab.renameNode = types.MethodType(renameNode, hc_tab)
    hc_tab.selectDisplayNode = types.MethodType(selectDisplayNode, hc_tab)
    hc_tab.toggleDimUnusedNodes = types.MethodType(toggleDimUnusedNodes, hc_tab)
    hc_tab.toggleLocating = types.MethodType(toggleLocating, hc_tab)
    hc_tab.toggleMenu = types.MethodType(toggleMenu, hc_tab)

## CONNECTIONS ##

# def connectNode(self):
# return
# choices = ("a", "b", "c")
# popup = hou.ui.selectFromList(choices)

# def rotateNodeInputs(self):
# return
# node = self.currentNode()
# connectors = node.inputConnectors()

## OBJECTS ##

def addNetworkBox(self):
    network_box = self.pwd().createNetworkBox()
    network_box.setPosition(self.currentNode().position())

def addStickyNote(self):
    sticky_note = self.pwd().createStickyNote()
    cursor_pos = self.cursorPosition()
    sticky_note.setPosition(cursor_pos)
    sticky_note.setColor(hou.Color(0.71, 0.78, 1.0))

## SELECTION ##

def deselectAll(self):
    self.currentNode().setSelected(False)

def selectDisplayNode(self):
    self.pwd().setCurrent(True, True)

## UTILS ##

def nextGridMode(self):
    mode = int(self.getPref("gridmode"))
    self.setPref("gridmode", (mode + 1) % 3)

def renameNode(self):
    node = self.currentNode()
    name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
    if name[0] == 0:
        node.setName(name[1])

def toggleDimUnusedNodes(self):
    dim = int(self.getPref("dimunusednodes"))
    self.setPref("dimunusednodes", str(not dim))

def toggleLocating(self):
    self.setLocatingEnabled(not self.locatingEnabled())

def toggleMenu(self):
    visible = int(self.getPref("showmenu"))
    self.setPref("showmenu", str(not visible))
