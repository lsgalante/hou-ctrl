import hou
from canvaseventtypes import *
import nodegraphdisplay as display
# import nodegraphview as view
import math
from importlib import reload
import nodegraphmain as ngm


def createEventHandler(uievent, pending_actions):
    reload(ngm)
    if ngm.action(uievent):
        return None, True
    else:
        return None, False
