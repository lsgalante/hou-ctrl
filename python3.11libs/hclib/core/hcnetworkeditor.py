import hou, math, types
from .hcpathtab import HCPathTab


class HCNetworkEditor(HCPathTab):
    def __init__(self, tab):
        self.tab = tab
        self.editor = tab
        self.deltat = 2

    def showPathMessage(self):
        self.editor.flashMessage(image=None, message=self.path(), duration=1)

    """
    Nodes
    """

    def arrangeNodes(self):
        # self.context().layoutChildren(horizontal_spacing=5, vertical_spacing=
        return

    def quantizeNodes(self):
        return

    def translateNodes(self, direction):
        idxmap = {
            'up': 1,
            'down': 1,
            'left': 0,
            'right': 0
        }
        rectifiermap = {
            'up': hou.Vector2(0, 0.85),
            'down': hou.Vector2(0, -0.85),
            'left': hou.Vector2(0.-0.85, 0),
            'right': hou.Vector2(0.85, 0)
        }
        for node in self.selectedNodes():
            idx = idxmap[direction]
            p = node.position() + rectifiermap[direction]
            val = p[idx]
            if val%1 <= 0.5:
                val = math.floor(val)
            else:
                val = math.ceil(val)
            p[idx] = val
            node.setPosition(p)

    def renameNode(self):
        node = self.currentNode()
        name = hou.ui.readInput("Rename_node", buttons=("Yes", "No"))
        if name[0] == 0:
            node.setName(name[1])

    """
    Objects
    """

    def addNetworkBox(self):
        networkbox = self.context().createNetworkBox()
        networkbox.setPosition(self.currentNode().position())

    def addStickyNote(self):
        stickynote = self.context().createStickyNote()
        p = self.cursorPos()
        stickynote.setPosition(p)
        stickynote.setColor(hou.Color(0.71, 0.78, 1.0))

    def placeDot(self):
        if len(self.selectedNodes()) == 1:
            dot = self.context().createNetworkDot()
            dot.setInput(node)
            dot.setPosition(self.cursorPos())

    """
    Selection
    """

    def deselectAll(self):
        self.selectedNodes().setSelected(False)

    """
    Settings
    """

    def toggleDimUnusedNodes(self):
        map = {
            '0': '1',
            '1': '0'
        }
        mode = self.editor.getPref('dimunusednodes')
        self.editor.setPref('dimunusednodes', map[mode])

    def toggleGridMode(self):
        map = {
            '0': '1',
            '1': '2',
            '2': '0'
        }
        mode = self.editor.getPref('gridmode')
        self.editor.setPref('gridmode', map[mode])

    def toggleMenu(self):
        map = {
            '0': '1',
            '1': '0'
        }
        mode = self.editor.getPref('showmenu')
        self.editor.setPref('showmenu', map[mode])

    def toggleUpdateMode(self):
        map = {
            'updateMode.Manual': hou.updateMode.AutoUpdate,
            'updateMode.AutoUpdate': hou.updateMode.Manual
        }
        mode = str(hou.updateModeSetting())
        hou.setUpdateMode(map[mode])

    """
    Viewport
    """

    def cursorPos(self):
        return self.editor.cursorPosition()

    def bounds(self):
        return self.editor.visibleBounds()

    def frameAll(self):
        self.editor.requestZoomReset()

    def screenSize(self):
        return self.editor.screenBounds().size()

    def setBounds(self, bounds):
        self.editor.setVisibleBounds(bounds)

    def size(self):
        return self.bounds().size()

    def translateView(self, direction):
        xformmap = {
            'up': hou.Vector2(0, self.deltat * self.zoomLevel()),
            'down': hou.Vector2(0, self.deltat * self.zoomLevel() * -1),
            'left': hou.Vector2(self.deltat * self.zoomLevel() * -1, 0),
            'right': hou.Vector2(self.deltat * self.zoomLevel(), 0)
        }
        bounds = self.bounds()
        bounds.translate(xformmap[direction])
        self.setBounds(bounds)

    def zoom(self, direction):
        scalemap = {
            'in': (0.75, 0.75),
            'out': (1.25, 1.25)
        }
        bounds = self.bounds()
        bounds.scale(scalemap[direction])
        self.setBounds(bounds)

    def zoomLevel(self):
        zoomlevel = self.size()[0] / self.size()[0]
        return zoomlevel
