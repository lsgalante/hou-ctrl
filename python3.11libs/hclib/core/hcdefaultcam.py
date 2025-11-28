import hou

class HCDefaultCam:
    def __init__(self, defaultcam):
        self.cam = defaultcam

    def frame(self):
        for viewport in self.viewports():
            cam = viewport.camera()
            # Is cam default or node.
            if not cam:
                viewport.frameAll()

    def nextView(self):
        return

    def rotate(self, key):
        return

    def translate(self, key):
        return

    def zoom(self):
        return
