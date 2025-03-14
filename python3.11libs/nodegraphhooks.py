import hou
from canvaseventtypes import *
import nodegraphdisplay as display
import nodegraphview as view

import math

from importlib import reload
import nodegraphfunctions as ngf

def createEventHandler(uievent, pending_actions):
    reload(ngf)
    if ngf.action(uievent):
        return None, True
    else:
        return None, False
