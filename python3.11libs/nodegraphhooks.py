import hou, math
from canvaseventtypes import *
import nodegraphdisplay as display
# import nodegraphview as view


def createEventHandler(uievent, pending_actions):
    editor = uievent.editor

    if isinstance(uievent, ContextEvent):
        # print("xx")
        return None, False

    elif isinstance(uievent, MouseEvent):
        return None, False

    elif isinstance(uievent, KeyboardEvent) and \
    uievent.eventtype == 'keyhit':
        hcEditor = HCEditor(editor)
        keys = {
            # ZOOM
            "=": hcEditor.zoomIn,
            "-": hcEditor.zoomOut,
            # MOVE VIEW
            "K": hcEditor.translateViewUp,
            "J": hcEditor.translateViewDown,
            "H": hcEditor.translateViewLeft,
            "L": hcEditor.translateViewRight,
            # MOVE NODE
            "Ctrl+Shift+K": hcEditor.translateNodesUp,
            "Ctrl+Shift+J": hcEditor.translateNodesDown,
            "Ctrl+Shift+H": hcEditor.translateNodesLeft,
            "Ctrl+Shift+L": hcEditor.translateNodesRight,
            # ORGANIZE
            "Ctrl+Shift+A": hcEditor.arrangeNodes,
            "Shift+D": hcEditor.placeDot,
            # GRID
            "Shift+G": hcEditor.nextGridMode,
            # UPDATE MODE
            "M": hcEditor.nextUpdateMode
        }

        for key in keys:
            if key == uievent.key:
                keys[key]()
                return None, True

        return None, False

    else:
        # print(uievent)
        return None, False



class HCEditor():
    def __init__(self, editor):
        self.editor = editor
        self.step_t = 160


    def arrangeNodes(self):
        # node.parent().layoutChildren(horizontal_spacing=5, vertical_spacing=
        return


    def pwd(self):
        return self.editor.pwd()


    def cursorPos(self):
        return self.editor.cursorPosition()


    def nextGridMode(self):
        mode = self.editor.getPref("gridmode")
        modes = ("0", "1", "2")
        idx = (modes.index(mode) + 1) % len(modes)
        self.editor.setPref("gridmode", modes[idx])


    def nextUpdateMode(self):
        mode = hou.updateModeSetting()
        modes = (hou.updateMode.Manual, hou.updateMode.AutoUpdate)
        idx = (modes.index(mode) + 1) % len(modes)
        hou.setUpdateMode(modes[idx])


    def nodes(self):
        return self.editor.selectedNodes()


    def placeDot(self):
        nodes = self.nodes()
        if len(nodes) == 1:
            context = nodes(0).parent()
            dot = context.createNetworkDot()
            dot.setInput(node)
            dot.setPosition(self.cursorPos())


    def quantizeNodes(self):
        return


    def screenSize(self):
        return self.editor.screenBounds().size()


    def translateNodesUp(self):
        for node in self.nodes():
            pos = node.position()
            y = pos[1]
            if round(y % 1, 2) < 0.85:
                y = math.floor(y)
            else:
                y = math.ceil(y)
            y += 0.85
            pos[1] = y
            node.setPosition(pos)


    def translateNodesDown(self):
        for node in self.nodes():
            pos = node.position()
            y = pos[1]
            if round(y % 1, 2) >= 0.85:
                y = math.floor(y)
            else:
                y = math.ceil(y)
            y -= 0.15
            pos[1] = y
            node.setPosition(pos)


    def translateNodesLeft(self):
        for node in self.nodes():
            pos = node.position()
            x = pos[0]
            if round(x % 1, 2) < 0.85:
                x = math.floor(x)
            else:
                x = math.ceil(x)
            x -= 0.5
            pos[0] = x
            node.setPosition(pos)


    def translateNodesRight(self):
        for node in self.nodes():
            pos = node.position()
            x = pos[0]
            if round(x % 1, 2) >= 0.85:
                x = math.floor(x)
            else:
                x = math.ceil(x)
            x += 0.5
            pos[0] = x
            node.setPosition(pos)


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
