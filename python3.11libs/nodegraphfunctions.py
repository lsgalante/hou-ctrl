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

    if isinstance(uievent, KeyboardEvent):
        if uievent.eventtype == 'keyhit':
            test = editorBindings(uievent.editor, uievent.key)


############
# # Bindings #
############
        
        
class editorBindings:
    
    def __init__(self, editor, key):
        self.context = editor.pwd()
        self.cursorP = editor.cursorPosition()
        self.editor = editor
        self.key = key
        self.nodes = hou.selectedNodes()
        self.screenSize = editor.screenBounds().size()
        self.step_t = 160
        self.visibleBounds = editor.visibleBounds()
        self.visibleSize = editor.visibleBounds().size()
        self.xform = None
        self.zoomLevel = self.getZoomLevel()

        
        ############
        # Bindings #
        ############
        
        
        # zoom
        if key == "=": self.zoom("in")
        elif key == "-": self.zoom("out")

        # translate
        elif key == "K": self.fovTranslate("up")
        elif key == "J": self.fovTranslate("down")
        elif key == "H": self.fovTranslate("left")
        elif key == "L": self.fovTranslate("right")
        
        # move
        elif key == "Ctrl+Shift+H": self.nodesTranslateLeft()
        elif key == "Ctrl+Shift+J": self.nodesTranslateDown()
        elif key == "Ctrl+Shift+K": self.nodesTranslateUp()
        elif key == "Ctrl+Shift+L": self.nodesTranslateRight()

        # organize
        elif key == "Ctrl+Shift+A": self.nodesArrange()
        elif key == "Shift+D": self.placeDot()

        # next grid mode
        elif key == "Shift+G": self.gridCycle()

        # next update mode
        elif key == "M": self.updateModeCycle()


    #############
    # Retrieval #
    #############

    
    def getZoomLevel(self):
        zoomLevel = self.visibleSize[0] / self.screenSize[0]
        return zoomLevel
    

    ##############
    # Navigation #
    ##############
    
    
    def fovTranslate(self, direction):
        if direction == "up":
            self.xform = hou.Vector2(0, self.step_t * self.zoomLevel)
        elif direction == "down":
            self.xform = hou.Vector2(0, self.step_t * self.zoomLevel * -1)
        elif direction == "left":
            self.xform = hou.Vector2(self.step_t * self.zoomLevel * -1, 0)
        elif direction == "right":
            self.xform = hou.Vector2(self.step_t * self.zoomLevel, 0)
            
        self.visibleBounds.translate(self.xform)
        self.editor.setVisibleBounds(self.visibleBounds)

    def zoom(self, direction):
        scale = (0, 0)
        if direction == "in":
            scale = (0.5, 0.5)
        else:
            scale = (2, 2)
            
        self.visibleBounds.scale(scale)
        self.editor.setVisibleBounds(self.visibleBounds)
        print(self.zoomLevel)

        
    ################
    # Manipulation #
    ################
 
    
    def nodesTranslateLeft(self):
        for node in self.nodes:
            nodeP = node.position()
            x = nodeP[0]
            print("")
            print(x)
            print(round(x%1, 2))
            if round(x % 1, 2) < 0.85:
                x = math.floor(x)
            else:
                x = math.ceil(x)
            x -= 0.5
            nodeP[0] = x
            node.setPosition(nodeP)
            

    def nodesTranslateDown(self):
        for node in self.nodes:
            nodeP = node.position()
            y = nodeP[1]
            if round(y % 1, 2) > 0.85:
                y = math.floor(y)
            else:
                y = math.ceil(y)
            y -= 0.15
            nodeP[1] = y
            node.setPosition(nodeP)
            

    def nodesTranslateUp(self):
        for node in self.nodes:
            nodeP = node.position()
            y = nodeP[1]
            if round(y % 1, 2) <= 0.85:
                y = math.floor(y)
            else:
                y = math.ceil(y)
            y += 0.85
            nodeP[1] = y
            node.setPosition(nodeP)
            

    def nodesTranslateRight(self):
        for node in self.nodes:
            nodeP = node.position()
            x = nodeP[0]
            # print(x)
            if round(x % 1, 2) >= 0.85:
                x = math.floor(x)
            else:
                x = math.ceil(x)
            x += 0.5
            nodeP[0] = x
            node.setPosition(nodeP)
        

    #########
    # Cycle #
    #########
    
    
    def gridModeCycle(self):
        mode = self.editor.getPref("gridmode")
        modes = ("0", "1", "2")
        idx = (modes.index(mode) + 1) % len(modes)
        self.editor.setPref("gridmode", modes[idx])


    ############
    # Organize #
    ############
    
    
    def nodesArrange(self):
        # node.parent().layoutChildren(horizontal_spacing=5, vertical_spacing=
        return

    
    def nodesQuantize(self):
        return

    
    def outlineDraw(self):
        image = hou.NetworkImage()
        image.setPath('$HIP/drawings/bg.png')
        image.setRect(hou.BoundingRect(0, 0, 1, 1))

        visibleItems = editor.networkItemsInBox(self.screenBounds.min(), self.screenBounds.max(), for_select=True)
        images = []
        for item in visibleItems:
            P0 = item[0].position()
            P0 = hou.Vector2(P0.x() - 0.025, P0.y() - 0.35)
            P1 = hou.Vector2(P0.x() + 1.05, P0.y() + 1)
            image.setRect(hou.BoundingRect(pos, pos2))
            images.append(image)
        self.editor.setBackgroundImages([image])

        
    def placeDot(self):
        if len(self.nodes) == 1:
            context = self.nodes(0).parent()
            dot = context.createNetworkDot()
            dot.setInput(node)
            dot.setPosition(self.cursorP)

            
    def updateModeNext(self):
        mode = hou.updateModeSetting()
        modes = (hou.updateMode.Manual, hou.updateMode.AutoUpdate)
        idx = (modes.index(mode) + 1) % len(modes)
        hou.setUpdateMode(modes[idx])


