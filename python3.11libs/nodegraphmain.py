import hou, math
from canvaseventtypes import *
# import hctl_utils as hcu
# import nodegraphdisplay as display
# import nodegraphview as view


def action(uievent):
    if isinstance(uievent, ContextEvent):
        return

    if isinstance(uievent, KeyboardEvent):
        if uievent.eventtype == 'keyhit':
            test = editorBindings(uievent.editor, uievent.key)


############
# Bindings #
############

class editorBindings:

    def __init__(self, editor, key):
        self.context = editor.pwd()
        self.cursor_pos = editor.cursorPosition()
        self.editor = editor
        self.key = key
        self.nodes = hou.selectedNodes()
        self.screen_size = editor.screenBounds().size()
        self.step_t = 160
        self.visible_bounds = editor.visibleBounds()
        self.visible_size = editor.visibleBounds().size()
        self.xform = None
        self.zoom_level = self.zoomLevel()


        ############
        # Bindings #
        ############

        # Zoom
        if key == "=": self.zoomIn()
        elif key == "-": self.zoomOut()

        # Translate
        elif key == "K": self.translateViewUp()
        elif key == "J": self.translateViewDown()
        elif key == "H": self.translateViewLeft()
        elif key == "L": self.translateViewRight()

        # Move
        elif key == "Ctrl+Shift+K": self.translateNodesUp()
        elif key == "Ctrl+Shift+J": self.translateNodesDown()
        elif key == "Ctrl+Shift+H": self.translateNodesLeft()
        elif key == "Ctrl+Shift+L": self.translateNodesRight()

        # Organize
        elif key == "Ctrl+Shift+A": self.arrangeNodes()
        elif key == "Shift+D": self.placeDot()

        # Next grid mode
        elif key == "Shift+G": self.cycleGrid()

        # Next update mode
        elif key == "M": self.cycleUpdateMode()


    #############
    # Functions #
    #############

    def ArrangeNodes(self):
        # node.parent().layoutChildren(horizontal_spacing=5, vertical_spacing=
        return


    def cycleGridMode(self):
        mode = self.editor.getPref("gridmode")
        modes = ("0", "1", "2")
        idx = (modes.index(mode) + 1) % len(modes)
        self.editor.setPref("gridmode", modes[idx])


    def cycleUpdateMode(self):
        mode = hou.updateModeSetting()
        modes = (hou.updateMode.Manual, hou.updateMode.AutoUpdate)
        idx = (modes.index(mode) + 1) % len(modes)
        hou.setUpdateMode(modes[idx])


    def placeDot(self):
        if len(self.nodes) == 1:
            context = self.nodes(0).parent()
            dot = context.createNetworkDot()
            dot.setInput(node)
            dot.setPosition(self.cursor_pos)


    def quantizeNodes(self):
        return


    def translateNodesUp(self):
        for node in self.nodes:
            node_pos = node.position()
            y = node_pos[1]
            if round(y % 1, 2) < 0.85:
                y = math.floor(y)
            else:
                y = math.ceil(y)
            y += 0.85
            node_pos[1] = y
            node.setPosition(node_pos)


    def translateNodesDown(self):
        for node in self.nodes:
            node_pos = node.position()
            y = node_pos[1]
            if round(y % 1, 2) >= 0.85:
                y = math.floor(y)
            else:
                y = math.ceil(y)
            y -= 0.15
            node_pos[1] = y
            node.setPosition(node_pos)


    def translateNodesLeft(self):
        for node in self.nodes:
            node_pos = node.position()
            x = node_pos[0]
            if round(x % 1, 2) < 0.85:
                x = math.floor(x)
            else:
                x = math.ceil(x)
            x -= 0.5
            node_pos[0] = x
            node.setPosition(node_pos)


    def translateNodesRight(self):
        for node in self.nodes:
            node_pos = node.position()
            x = node_pos[0]
            if round(x % 1, 2) >= 0.85:
                x = math.floor(x)
            else:
                x = math.ceil(x)
            x += 0.5
            node_pos[0] = x
            node.setPosition(node_pos)


    def translateViewUp(self):
        self.xform = hou.Vector2(0, self.step_t * self.zoom_level)
        self.visible_bounds.translate(self.xform)
        self.editor.setVisibleBounds(self.visible_bounds)


    def translateViewDown(self):
        self.xform = hou.Vector2(0, self.step_t * self.zoom_level * -1)
        self.visible_bounds.translate(self.xform)
        self.editor.setVisibleBounds(self.visible_bounds)


    def translateViewLeft(self):
        self.xform = hou.Vector2(self.step_t * self.zoom_level * -1, 0)
        self.visible_bounds.translate(self.xform)
        self.editor.setVisibleBounds(self.visible_bounds)


    def translateViewRight(self):
        self.xform = hou.Vector2(self.step_t * self.zoom_level, 0)
        self.visible_bounds.translate(self.xform)
        self.editor.setVisibleBounds(self.visible_bounds)


    def zoomIn(self):
        scale = (0.75, 0.75)
        self.visible_bounds.scale(scale)
        self.editor.setVisibleBounds(self.visible_bounds)
        print(self.zoom_level)


    def zoomLevel(self):
        zoom_level = self.visible_size[0] / self.screen_size[0]
        return zoom_level


    def zoomOut(self):
        scale = (1.25, 1.25)
        self.visible_bounds.scale(scale)
        self.editor.setVisibleBounds(self.visible_bounds)
