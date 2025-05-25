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

        
        #######
        # FOV #
        #######
        
        
        # zoom
        if key == "-":
            zoomOut()
        elif key == "=":
            zoomIn()

        # translate
        elif key == "H":
            fovTranslateLeft(editor)
        elif key == "J":
            fovTranslateDown(editor)
        elif key == "K":
            fovTranslateUp(editor)
        elif key == "L":
            fovTranslateRight(editor)

            
        #########
        # Nodes #
        #########
        
        
        # move
        elif key == "Ctrl+Shift+H":
            nodesTranslateLeft()
        elif key == "Ctrl+Shift+J":
            nodesTranslateDown()
        elif key == "Ctrl+Shift+K":
            nodesTranslateUp()
        elif key == "Ctrl+Shift+L":
            nodesTranslateRight()

        # organize
        elif key == "Ctrl+Shift+A":
            nodesArrange()


        ###################
        # Network Objects #
        ###################
        
        
        # place dot
        elif key == "Shift+D":
            dotPlace()


        #########
        # Other #
        #########

        
        # next grid mode
        elif key == "Shift+G":
            gridModeNext(editor)

        # next update mode
        elif key == "M":
            updateModeNext()

            
def dotPlace(editor):
    selected = hou.selectedNodes()
    if len(selected) == 1:
        context = node.parent()
        dot = context.createNetworkDot()
        dot.setInput(node)
        cursor_pos = editor.cursorPosition()
        dot.setPosition(cursor_pos)

        
def fovTranslate(editor, xform):
    visible_bounds = editor.visibleBounds()
    visible_bounds.translate(xform)
    editor.setVisibleBounds(visible_bounds)

    
def fovTranslateLeft(editor):
    step = 160
    zoom_level = zoomGetLevel(editor)
    xform = hou.Vector2(step * zoom_level * -1, 0)
    fovTranslate(editor, xform)

    
def fovTranslateDown(editor):
    step = 160
    zoom_level = zoomGetLevel(editor)
    xform = hou.Vector2(0, step * zoom_level * -1)
    fovTranslate(editor, xform)

    
def fovTranslateUp(editor):
    step = 160
    zoom_level = zoomGetLevel(editor)
    xform = hou.Vector2(0, step * zoom_level)
    fovTranslate(editor, xform)

    
def fovTranslateRight(editor):
    step = 160
    zoom_level = zoomGetLevel(editor)
    xform = hou.Vector2(step * zoom_level, 0)
    fovTranslate(editor, xform)

    
def gridModeNext(editor):
    mode = editor.getPref("gridmode")
    modes = ("0", "1", "2")
    idx = (modes.index(mode) + 1) % len(modes)
    editor.setPref("gridmode", modes[idx])

        
def nodesArrange():
    nodes = hou.selectedNodes()
    # node.parent().layoutChildren(horizontal_spacing=5, vertical_spacing=5)

    
def nodesQuantize():
    nodes = hou.selectedNodex()
    

def nodesTranslateLeft():
    nodes = hou.selectedNodes()
    for node in nodes:
        x = node.position()[0]
        y = node.position()[1]
        if round(x % 1, 1) <= 0.5:
            x = math.floor(x)
        else:
            x = math.ceil(x)
        x -= 0.5
        node.setPosition(x, y)
        

def nodesTranslateDown():
    nodes = hou.selectedNodes()
    for node in nodes:
        x = node.position()[0]
        y = node.position()[1]
        if round(y % 1, 2) > 0.85:
            y = math.ceil(y)
        else:
            y = math.floor(y)
        y -= 0.15
        node.setPosition(x, y)
        

def nodesTranslateUp():
    nodes = hou.selectedNodes()
    for node in nodes:
        x = node.position()[0]
        y = node.position()[1]
        if round(y % 1, 2) < 0.85:
            y = math.floor(y)
        else:
            y = math.ceil(y)
        node.setPosition(x, y + 0.85)
        

def nodesTranslateRight():
    nodes = hou.selectedNodes()
    for node in nodes:
        x = node.position()[0]
        y = node.position()[1]
        if round(x % 1, 1) >= 0.5:
            x = math.ceil(x)
        else:
            x = math.floor(x)
        node.setPosition(x + 0.5, y)
        
    
def outlineDraw(uievent):
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

    
def updateModeNext():
    mode = hou.updateModeSetting()
    modes = (hou.updateMode.Manual, hou.updateMode.AutoUpdate)
    idx = (modes.index(mode) + 1) % len(modes)
    hou.setUpdateMode(modes[idx])

    
def zoomGetLevel(editor):
    screen_size = editor.screenBounds().size()
    visible_size = editor.visibleBounds().size()
    zoom_level = visible_size[0] / screen_size[0]
    return zoom_level


def zoomOut():
    return
    
