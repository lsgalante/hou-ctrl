import hou
from .hcgeo import HCGeo


class HCCam:
    def __init__(self, cam, viewer):
        self.cam = cam
        self.viewer = viewer
        self.parms = Parms(cam)
        self.hcgeo = HCGeo(viewer)
        self.fitAspectRatio()
        self.lock()
        self.reset()

    def center(self):
        centroid = self.hcgeo.centroid()
        self.parms.t = hou.Vector3(centroid)
        self.parms.p = hou.Vector3(centroid)

    def doZoom(self, direction):
        signmap = {'out': 1, 'in': -1}
        sign = signmap[direction]
        move = self.parms.localz * self.parms.deltazoom * sign
        self.parms.t += move

    def fitAspectRatio(self):
        self.cam.parm('resx').set(1000)
        self.cam.parm('resy').set(1000)
        ratio = self.viewport().size()[2] / self.viewport().size()[3]
        self.cam.parm('aspect').set(ratio)

    def frame(self):
        centroid = self.hcgeo.centroid()
        self.parms.t = hou.Vector3(centroid)
        self.parms.p = hou.Vector3(centroid)
        # self.parms.ow = 10
        self.setZoom(10)

    def home(self):
        centroid = self.hcgeo.centroid()
        self.parms.t = centroid
        self.parms.p = centroid
        # self.parms.ow = 10
        # self.setZoom(6)

    def lock(self):
        viewport = self.viewport()
        viewport.setCamera(self.cam)
        viewport.lockCameraToView(1)

    def movePivot(self):
        # If origin
        if self.parms.target == 0:
            self.parms.t = [0, 0, self.parms.zoom]
            self.parms.r = [45, 45, 0]
            self.parms.p = [0, 0, self.parms.zoom * -1]
            self.parms.ow = 10

    def nextProjection(self):
        projectionmap = {
            'perspective': 'ortho',
            'ortho': 'perspective'
        }
        parm = self.cam.parm('projection')
        parm.set(projectionmap[parm.evalAsString()])

    def orthoZoom(self, direction):
        signmap = {'out': 1, 'in': -1}
        sign = signmap[direction]
        self.parms.ow += self.parms.deltazoom * sign

    def reset(self):
        self.parms.localx = hou.Vector3(1, 0, 0)
        self.parms.localy = hou.Vector3(0, 1, 0)
        self.parms.localz = hou.Vector3(0, 0, 1)
        self.parms.globalx = hou.Vector3(1, 0, 0)
        self.parms.globaly = hou.Vector3(0, 1, 0)
        self.parms.globalz = hou.Vector3(0, 0, 1)
        self.parms.p = hou.Vector3(0, 0, 0)
        self.parms.r = hou.Vector3(0, 0, 0)
        self.parms.t = hou.Vector3(0, 0, 2)
        self.parms.zoom = 10
        self.parms.ow = 10
        self.parms.deltat = 1
        self.parms.deltar = 15
        self.parms.deltazoom = 1

    def rotate(self, direction):
        axismap = {
            'up': self.parms.localx,
            'down': self.parms.localx,
            'left': self.parms.globaly,
            'right': self.parms.globaly,
        }
        signmap = {'up': 1, 'down': -1, 'left': -1, 'right': 1}
        deltamap = {
            'up': hou.Vector3(self.parms.deltar, 0, 0),
            'down': hou.Vector3(self.parms.deltar, 0, 0),
            'left': hou.Vector3(0, self.parms.deltar, 0),
            'right': hou.Vector3(0, self.parms.deltar, 0),
        }
        axis = axismap[direction]
        sign = signmap[direction]
        delta = deltamap[direction] * sign
        self.parms.r += delta
        m = hou.hmath.buildRotateAboutAxis(axis, self.parms.deltar * sign)
        self.parms.t -= self.parms.p
        self.parms.t *= m
        self.parms.t += self.parms.p
        self.parms.localx *= m
        self.parms.localy *= m
        self.parms.localz *= m

    def setOrthoZoom(self, level):
        self.parms.ow = zoomlevel

    def setView(self):
        viewmap = {
            'top': hou.Vector3(270, 0, 0),
            'bottom': hou.Vector3(90, 0, 0),
            'front': hou.Vector3(0, 180, 0),
            'back': hou.Vector3(0, 0, 0),
            'right': hou.Vector3(0, 90, 0),
            'left': hou.Vector3(0, 270, 0)
        }
        self.hccam.r = viewmap[self.parms.view]

    def setZoom(self, level):
        move = self.parms.localz * level
        self.parms.t += move

    def translate(self, direction):
        axismap = {
            'up': self.parms.localy,
            'down': self.parms.localy,
            'left': self.parms.localx,
            'right': self.parms.localx,
        }
        signmap = {'up': 1, 'down': -1, 'left': -1, 'right': 1}
        axis = axismap[direction]
        sign = signmap[direction]
        move = axis * self.parms.deltat * sign
        self.parms.t += move
        self.parms.p += move

    def unlock(self):
        self.viewport().lockCameraToView(0)

    def viewport(self):
        return self.viewer.viewports()[3]


class Parms:
    def __init__(self, cam):
        self.cam = cam
        self._t = hou.Vector3(0, 0, 0)
        self._r = hou.Vector3(0, 0, 0)
        self._p = hou.Vector3(0, 0, 0)
        self._projection = 'perspective'
        self.localx = hou.Vector3(1, 0, 0)
        self.localy = hou.Vector3(0, 1, 0)
        self.localz = hou.Vector3(0, 0, 1)
        self.globalx = hou.Vector3(1, 0, 0)
        self.globaly = hou.Vector3(0, 1, 0)
        self.globalz = hou.Vector3(0, 0, 1)
        self.zoom = 10
        self.ow = 10
        self.deltat = 1
        self.deltar = 15
        self.deltazoom = 1
        self.target = None

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, val):
        self._t = val
        self.cam.parmTuple('t').set(val)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, val):
        self._r = val
        self.cam.parmTuple('r').set(val)

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, val):
        self._p = val
        self.cam.parmTuple('p').set(val)

    @property
    def projection(self):
        return self._projection

    @projection.setter
    def projection(self, val):
        self._projection = val
        self.cam.parm('projection').set(val)
