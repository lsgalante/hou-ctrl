import hou

class Printer():
    def __init__(self):
        self.message = ""
    __init__.interactive = False

    def layout(self):
        message = "Layout:"
        desktop = hou.ui.curDesktop()
        panes = desktop.panes()
        ct = 0
        for pane in panes:
            message += " Pane" + str(ct) + " -"
            if pane.isSplit():
                message += " split"
            else:
                message += " whole"
                message += "    "
            ct += 1
        message = message[0:-1]
        hou.ui.setStatusMessage(message)
    layout.interactive = True
