import hou, math, types
from .hctab import HCTab


class HCNetworkEditor(HCTab):
    def __init__(self, tab):
        # super().__init__(hctab.tab)
        self.editor = tab
        self.step_t = 160

    """
    Appearance
    """

    def nextGridMode(self):
        modemap = {
            "0": "1",
            "1": "2",
            "2": "0"
        }
        mode = int(self.editor.getPref("gridmode"))
        self.setPref("gridmode", modemap[mode])

    def toggleDimUnusedNodes(self):
        dim = int(self.tab.getPref("dimunusednodes"))
        self.setPref("dimunusednodes", str(not dim))

    def toggleMenu(self):
        visiblemap = {
            "0": "1",
            "1": "0"
        }
        visible = self.tab.getPref("showmenu")
        self.tab.setPref("showmenu", visiblemap[visible])

    """
    Context
    """

    def pwd(self):
        return self.editor.pwd()

    """
    Cooking
    """

    def nextUpdateMode(self):
        mode = hou.updateModeSetting()
        modes = (hou.updateMode.Manual, hou.updateMode.AutoUpdate)
        idx = (modes.index(mode) + 1) % len(modes)
        hou.setUpdateMode(modes[idx])

    """
    Movement
    """

    def arrangeNodes(self):
        # node.parent().layoutChildren(horizontal_spacing=5, vertical_spacing=
        return

    def quantizeNodes(self):
        return

    def translateNodes(self, key):
        idxmap = {
            "Ctrl+UpArrow": 1,
            "Ctrl+DownArrow": 1,
            "Ctrl+LeftArrow": 0,
            "Ctrl+RightArrow": 0
        }
        rectifiermap = {
            "Ctrl+UpArrow": hou.Vector2(0, 0.85),
            "Ctrl+DownArrow": hou.Vector2(0, -0.85),
            "Ctrl+LeftArrow": hou.Vector2(0.-0.85, 0),
            "Ctrl+RightArrow": hou.Vector2(0.85, 0)
        }
        for node in self.nodes():
            p = node.position()
            print(p)
            rectifier = rectifiermap[key]
            p += rectifier
            idx = idxmap[key]
            val = p[idx]
            print(val)
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
        name = hou.ui.readInput("rename_node", buttons=("yes", "no"))
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
