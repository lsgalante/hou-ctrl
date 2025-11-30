import hou, math, types
from .hctab import HCTab


class HCNetworkEditor(HCTab):
    def __init__(self, tab):
        self.editor = tab
        self.step_t = 160

    """
    Appearance
    """

    def nextGridMode(self):
        modemap = {
            '0': '1',
            '1': '2',
            '2': '0'
        }
        mode = int(self.editor.getPref('gridmode'))
        self.setPref('gridmode', modemap[mode])

    def toggleDimUnusedNodes(self):
        dim = int(self.editor.getPref('dimunusednodes'))
        self.setPref('dimunusednodes', str(not dim))

    def toggleMenu(self):
        visiblemap = {
            '0': '1',
            '1': '0'
        }
        visible = self.editor.getPref('showmenu')
        self.editor.setPref('showmenu', visiblemap[visible])

    """
    Context
    """

    def pwd(self):
        return self.editor.pwd()

    """
    Cooking
    """

    def nextUpdateMode(self):
        map = {
            'updateMode.Manual': hou.updateMode.AutoUpdate,
            'updateMode.AutoUpdate': hou.updateMode.Manual
        }
        mode = hou.updateModeSetting()
        hou.setUpdateMode(map[str(hou.updateModeSetting())])

    """
    Movement
    """

    def arrangeNodes(self):
        # node.parent().layoutChildren(horizontal_spacing=5, vertical_spacing=
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
        for node in self.nodes():
            p = node.position()
            rectifier = rectifiermap[direction]
            p += rectifier
            idx = idxmap[direction]
            val = p[idx]
            if val%1 <= 0.5:
                val = math.floor(val)
            else:
                val = math.ceil(val)
            p[idx] = val
            node.setPosition(p)

    """
    Nodes
    """

    def nodes(self):
        return self.pwd().selectedChildren()

    def renameNode(self):
        node = self.currentNode()
        name = hou.ui.readInput("Rename_node", buttons=("Yes", "No"))
        if name[0] == 0:
            node.setName(name[1])

    """
    Objects
    """

    def addNetworkBox(self):
        networkbox = self.pwd().createNetworkBox()
        networkbox.setPosition(self.currentNode().position())

    def addStickyNote(self):
        stickynote = self.pwd().createStickyNote()
        p = self.cursorPosition()
        stickynote.setPosition(p)
        stickynote.setColor(hou.Color(0.71, 0.78, 1.0))

    def placeDot(self):
        nodes = self.nodes()
        if len(nodes) == 1:
            context = nodes(0).parent()
            dot = context.createNetworkDot()
            dot.setInput(node)
            dot.setPosition(self.cursorPos())

    """
    Options
    """

    def getPref(self, pref):
        return self.editor.getPref(pref)

    def setPref(self, pref):
        return self.editor.setPref(pref)

    def toggleLocating(self):
        self.setLocatingEnabled(not self.locatingEnabled())

    """
    Selection
    """

    def deselectAll(self):
        self.currentNode().setSelected(False)

    def selectDisplayNode(self):
        self.pwd().setCurrent(True, True)

    """
    Viewport
    """

    def cursorPos(self):
        return self.editor.cursorPosition()

    def screenSize(self):
        return self.editor.screenBounds().size()

    def translateViewUp(self):
        xform = hou.Vector2(0, self.step_t * self.zoomLevel())
        bounds = self.visibleBounds()
        bounds.translate(xform)
        self.editor.setVisibleBounds(bounds)

    def translateViewDown(self):
        xform = hou.Vector2(0, self.step_t * self.zoomLevel() * -1)
        bounds = self.visibleBounds()
        bounds.translate(xform)
        self.editor.setVisibleBounds(bounds)

    def translateViewLeft(self):
        xform = hou.Vector2(self.step_t * self.zoomLevel() * -1, 0)
        bounds = self.visibleBounds()
        bounds.translate(xform)
        self.editor.setVisibleBounds(bounds)

    def translateViewRight(self):
        xform = hou.Vector2(self.step_t * self.zoomLevel(), 0)
        bounds = self.visibleBounds()
        bounds.translate(xform)
        self.editor.setVisibleBounds(bounds)

    def visibleBounds(self):
        return self.editor.visibleBounds()

    def visibleSize(self):
        return self.editor.visibleBounds().size()

    def zoomIn(self):
        scale = (0.75, 0.75)
        bounds = self.visibleBounds()
        bounds.scale(scale)
        self.editor.setVisibleBounds(bounds)

    def zoomLevel(self):
        zoom_level = self.visibleSize()[0] / self.screenSize()[0]
        return zoom_level

    def zoomOut(self):
        scale = (1.25, 1.25)
        bounds = self.visibleBounds()
        bounds.scale(scale)
        self.editor.setVisibleBounds(bounds)
