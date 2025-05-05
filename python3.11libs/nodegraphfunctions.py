import hou, labutils, math, os
from canvaseventtypes import *
import hctl_utils as hcu
import nodegraphdisplay as display
import nodegraphview as view
from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QColor, QCursor, QPen, QPixmap
from PySide2.QtWidgets import QGraphicsScene, QGraphicsView

def action(uievent):
    if isinstance(uievent, ContextEvent):
        return

    if isinstance(uievent, KeyboardEvent) and uievent.eventtype == 'keyhit':
        editor = uievent.editor
        key = uievent.key

        # Move nodes
        if key in ("Ctrl+Shift+H", "Ctrl+Shift+J", "Ctrl+Shift+K", "Ctrl+Shift+L"):
            nodes = hou.selectedNodes()
            for node in nodes:
                node_x = node.position()[0]
                node_y = node.position()[1]

                if key == "Ctrl+Shift+H":
                    if round(node_x % 1, 1) <= 0.5:
                        node_x = math.floor(node_x) - 0.5
                    else:
                        node_x = math.ceil(node_x) - 0.5

                elif key == "Ctrl+Shift+J":
                    if round(node_y % 1, 2) > 0.85:
                        node_y = math.ceil(node_y) - 0.15
                    else:
                        node_y = math.floor(node_y) - 0.15

                elif key == "Ctrl+Shift+K":
                    if round(node_y % 1, 2) < 0.85:
                        node_y = math.floor(node_y) + 0.85
                    else:
                        node_y = math.ceil(node_y) + 0.85

                elif key == 'Ctrl+Shift+L':
                    if round(node_x % 1, 1) >= 0.5:
                        node_x = math.ceil(node_x) + 0.5
                    else:
                        node_x = math.floor(node_x) + 0.5

                new_pos = (node_x, node_y)
                node.setPosition(new_pos)

        # Organize nodes
        elif key == "Ctrl+Shift+A":
            node = editor.currentNode()
            node.parent().layoutChildren(horizontal_spacing=5, vertical_spacing=5), 

        # Place dot
        elif key == "Shift+D":
            selected = hou.selectedNodes()
            if len(selected) == 1:
                context = node.parent()
                dot = context.createNetworkDot()
                dot.setInput(node)
                cursor_pos = editor.cursorPosition()
                dot.setPosition(cursor_pos)

        # Grid mode
        elif key == "Shift+G":
            mode = editor.getPref("gridmode")
            modes = ("0", "1", "2")
            idx = modes.index(mode)
            idx = (idx + 1) % 3
            mode = modes[idx]
            editor.setPref("gridmode", mode) 

        # Panning
        if key in ("H", "J", "K", "L"):
            view_xform = [0, 0]
            view_step = 160
            screen_size = editor.screenBounds().size()
            visible_size = editor.visibleBounds().size()
            zoom_amt = visible_size[0] / screen_size[0]
            if   key == "H": view_xform[0] = view_step * zoom_amt * -1
            elif key == "J": view_xform[1] = view_step * zoom_amt * -1
            elif key == "K": view_xform[1] = view_step * zoom_amt
            elif key == "L": view_xform[0] = view_step * zoom_amt
            xform = hou.Vector2(view_xform[0], view_xform[1])
            visible_bounds = editor.visibleBounds()
            visible_bounds.translate(xform)
            editor.setVisibleBounds(visible_bounds)

        # Update mode
        elif key == "M":
            mode = hou.updateModeSetting()
            modes = (hou.updateMode.Manual, hou.updateMode.AutoUpdate)
            idx = (modes.index(mode) + 1) % 2
            hou.setUpdateMode(modes[idx])


def drawOutline(uievent):
    editor = uievent.editor
    image = hou.NetworkImage()
    image.setPath('$HIP/drawings/bg.png')
    image.setRect(hou.BoundingRect(0, 0, 1, 1))

    screen_space = editor.screenBounds()
    visible_items = editor.networkItemsInBox(screen_space.min(), screen_space.max(), for_select=True)
    images = []
    for item in visible_items:
        pos = item[0].position()
        pos = hou.Vector2(pos.x()-0.025, pos.y()-0.35)
        pos2 = hou.Vector2(pos.x()+1.05, pos.y()+1)
        image.setRect(hou.BoundingRect(pos, pos2))
        images.append(image)

    editor.setBackgroundImages([image])
