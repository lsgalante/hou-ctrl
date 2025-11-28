import hou
from .hcgeo import HCGeo


class HCCam:
    def __init__(self, cam, viewer):
        self.cam = cam
        self.viewer = viewer
        self.hcgeo = HCGeo(viewer)
        self.lock()

        self.localx = hou.Vector3(0, 0, 0)
        self.localy = hou.Vector3(0, 0, 0)
        self.localz = hou.Vector3(0, 0, 0)
        self.globalx = hou.Vector3(0, 0, 0)
        self.globaly = hou.Vector3(0, 0, 0)
        self.globalz = hou.Vector3(0, 0, 0)
        self._p = hou.Vector3(0, 0, 0)
        self._r = hou.Vector3(0, 0, 0)
        self._t = hou.Vector3(0, 0, 0)
        self._zoom = 0
        self._ow = 0
        self._target = None
        self._deltar = 0
        self._deltat = 0
        self._deltazoom = 0

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, val):
        self._p = val
        self.cam.parmTuple("p").set(list(val))

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, val):
        self._r = val
        self.cam.parmTuple("r").set(list(val))

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, val):
        self._t = val
        self.cam.parmTuple("t").set(list(val))

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, val):
        self._zoom = val
        self.setZoom(10)

    @property
    def dist(self):
        return self._dist

    @property
    def ow(self):
        return self._ow

    @ow.setter
    def ow(self, val):
        self._ow = val
        self.cam.parm("orthowidth").set(val)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, val):
        self._target = val

    @property
    def deltar(self):
        return self._deltar

    @deltar.setter
    def deltar(self, val):
        self._deltar = val

    @property
    def deltat(self):
        return self._deltat

    @deltat.setter
    def deltat(self, val):
        self._deltat = val

    @property
    def deltazoom(self):
        return self._deltazoom

    @deltazoom.setter
    def deltazoom(self, val):
        self._deltazoom = val

    @property
    def layout(self):
        return self._layout


    def center(self):
        centroid = self.hcgeo.centroid()
        self.t = hou.Vector3(centroid)
        self.p = hou.Vector3(centroid)

    def fitAspectRatio(self):
        self.cam.parm("resx").set(1000)
        self.cam.parm("resy").set(1000)
        ratio = self.viewport().size()[2] / self.viewport().size()[3]
        self.cam.parm("aspect").set(ratio)

    def frame(self):
        centroid = self.hcgeo.centroid()
        self.t = hou.Vector3(centroid)
        self.p = hou.Vector3(centroid)
        # self.ow = 10
        self.setZoom(10)

    def home(self):
        centroid = self.hcgeo.centroid()
        self.t = centroid
        self.p = centroid
        # self.ow = 10
        # self.setZoom(6)

    def lock(self):
        viewport = self.viewport()
        viewport.setCamera(self.cam)
        viewport.lockCameraToView(1)

    def unlock(self):
        self.viewport().lockCameraToView(0)

    def movePivot(self):
        # If origin
        if self.target == 0:
            self.t = [0, 0, self.zoom]
            self.r = [45, 45, 0]
            self.p = [0, 0, self.zoom * -1]
            self.ow = 10

    def nextProjection(self, key):
        projectionmap = {
            "perspective": "ortho",
            "ortho": "perspective"
        }
        parm = self.cam.parm("projection")
        parm.set(projectionmap[parm.evalAsString])

    def rotate(self, key):
        axismap = {
            "h": self.globaly,
            "j": self.localx,
            "k": self.localx,
            "l": self.globaly,
        }
        signmap = {"h": -1, "j": -1, "k": 1, "l": 1}
        deltamap = {
            "h": hou.Vector3(0, self.deltar, 0),
            "j": hou.Vector3(self.deltar, 0, 0),
            "k": hou.Vector3(self.deltar, 0, 0),
            "l": hou.Vector3(0, self.deltar, 0),
        }
        axis = axismap[key]
        sign = signmap[key]
        delta = deltamap[key] * sign
        self.r += delta
        m = hou.hmath.buildRotateAboutAxis(axis, self.deltar * sign)
        self.t -= self.p
        self.t *= m
        self.t += self.p
        self.localx *= m
        self.localy *= m
        self.localz *= m

    def translate(self, direction):
        axismap = {
            "up": self.localy,
            "down": self.localy,
            "left": self.localx,
            "right": self.localx,
        }
        signmap = {"up": 1, "down": -1, "left": -1, "right": 1}
        axis = axismap[key]
        sign = signmap[key]
        move = axis * self.deltat * sign
        self.t += move
        self.p += move

    def setZoom(self, level):
        move = self.localz * level
        self.t += move

    def zoom(self, key):
        signmap = {"-": 1, "=": -1}
        sign = signmap[key]
        move = self.localz * self.deltazoom * sign
        self.t += move

    def setOrthoZoom(self, level):
        self.ow = zoomlevel

    def orthoZoom(self, key):
        signmap = {"Shift+-": 1, "Shift+=": -1}
        sign = signmap[key]
        self.ow += self.deltazoom * sign

    # Vector variables are stored as Vector3 and converted when settings
    # parameters

    def reset(self):
        self.localx = hou.Vector3(1, 0, 0)
        self.localy = hou.Vector3(0, 1, 0)
        self.localz = hou.Vector3(0, 0, 1)
        self.globalx = hou.Vector3(1, 0, 0)
        self.globaly = hou.Vector3(0, 1, 0)
        self.globalz = hou.Vector3(0, 0, 1)
        self.p = hou.Vector3(0, 0, 0)
        self.r = hou.Vector3(0, 0, 0)
        self.t = hou.Vector3(0, 0, 0)
        self.zoom = 10
        self.ow = 10
        self.deltat = 1
        self.deltar = 15
        self.deltazoom = 1

    def viewport(self):
        return self.viewer.viewports()[0]
