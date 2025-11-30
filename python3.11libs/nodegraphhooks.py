import hou
from canvaseventtypes import *
import nodegraphdisplay as display
from hclib import HCTab, HCNetworkEditor
# import nodegraphview as view


def createEventHandler(uievent, pending_actions):

    if isinstance(uievent, ContextEvent):
        return None, False

    elif isinstance(uievent, MouseEvent):
        return None, False

    elif isinstance(uievent, KeyboardEvent) and \
    uievent.eventtype == 'keyhit':
        tab = uievent.editor
        hctab = HCTab(tab)
        hceditor = HCNetworkEditor(hctab)
        keymap = {
            ## Zoom
            '=': hceditor.zoomIn,
            '-': hceditor.zoomOut,
            ## Move view
            'K': hceditor.translateViewUp,
            'J': hceditor.translateViewDown,
            'H': hceditor.translateViewLeft,
            'L': hceditor.translateViewRight,
            ## Move node
            'Ctrl+K': lambda: hceditor.translateNodes('up'),
            'Ctrl+J': lambda: hceditor.translateNodes('down'),
            'Ctrl+H': lambda: hceditor.translateNodes('left'),
            'Ctrl+L': lambda: hceditor.translateNodes('right'),
            ## Organize
            'Ctrl+Shift+A': hceditor.arrangeNodes,
            'Shift+D': hceditor.placeDot,
            ## Grid
            'Shift+G': hceditor.nextGridMode,
            ## Update mode
            'M': hceditor.nextUpdateMode
        }

        key = uievent.key
        if key in keymap:
            func = keymap[key](key)
            return None, True
        else:
            return None, False

    else:
        return None, False
