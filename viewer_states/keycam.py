import hou


class State(object):

    def __init__(self, state_name, scene_viewer):
        # General Variables #
        self.sceneViewer = scene_viewer
        self.cam_type = None
        self.context = None
        self.state_name = state_name

        self.options = {
            "center_on_geo": 1,
            "lock_cam": 1,
            "cam_reset": 1
        }

        self.units = {
            "r": 7.5,
            "t": 1,
            "ow": 1,
            "dist": 1
        }


    def onDraw(self, kwargs):
        handle = kwargs["draw_handle"]
        self.kGuides.CamAxis.draw(handle, {})
        self.kGuides.PivotAxis.draw(handle, {})
        self.kGuides.Perim.draw(handle, {})
        self.kGuides.Pivot2d.draw(handle, {})
        self.kGuides.Pivot3d.draw(handle, {})
        self.kGuides.Ray.draw(handle, {})
        # self.kGuides.Text.draw(handle, {})


    def onExit(self, kwargs):
        for viewport in self.sceneViewer.viewports():
            viewport.lockCameraToView(False)


    def onGenerate(self, kwargs):
        # Prevent exiting the state when current node changes
        kwargs["state_flags"]["exit_on_node_select"] = False
        self.kwargs = kwargs
        self.kUtils =       KUtils()
        self.kSceneViewer = KSceneViewer(self)
        self.kCam =         KCam(self)
        self.kParms =       KParms(self)
        self.kGeo =         KGeo(self)
        self.kGuides =      KGuides(self)
        self.kHud =         KHud(self)
        self.updateNetworkContext()
        self.updateOptions()
        self.kCam.frame()


    def onKeyEvent(self, kwargs):
        self.kCam.updateAspectRatio()

        # Persp cam
        keymap = {
            "-": self.kCam.zoomOut,
            "+": self.kCam.zoomIn,
            "o": self.kCam.nextProjection,
            "h": self.kCam.rotateLeft,
            "j": self.kCam.rotateDown,
            "k": self.kCam.rotateUp,
            "l": self.kCam.rotateRight,
            "Shift+_": self.kCam.orthoZoomOut,
            "Shift++": self.kCam.orthoZoomIn,
            "Shift+h": self.kCam.translateLeft,
            "Shift+j": self.kCam.translateDown,
            "Shift+k": self.kCam.translateUp,
            "Shift+l": self.kCam.translateDown
        }

        key = kwargs["ui_event"].device().keyString()
        keymap.get(key, lambda: False)()

        # Default cam
        # elif kwargs["state_parms"]["camera"]["value"] == 1:
        #     indices = (0, 0)
        #     if self.viewport.type() ==   hou.geometryViewportType.Top:    indices = (0, 1)
        #     elif self.viewport.type() == hou.geometryViewportType.Bottom: indices = (2, 0)
        #     elif self.viewport.type() == hou.geometryViewportType.Front:  indices = (0, 1)
        #     elif self.viewport.type() == hou.geometryViewportType.Back:   indices = (1, 0)
        #     elif self.viewport.type() == hou.geometryViewportType.Right:  indices = (0, 1)
        #     elif self.viewport.type() == hou.geometryViewportType.Left:   indices = (1, 2)
            # functions = (
            #     self.defaultcamR, self.defaultcamR,
            #     self.defaultcamR, self.defaultcamR,
            #     self.defaultcamT(indices), self.defaultcamT(indices),
            #     self.defaultcamT(indices), self.defaultcamT(indices),
            #     cam.setOrthoWidth(cam.orthoWidth() - 1),
            #     cam.setOrthoWidth(cam.orthoWidth() + 1)
            # )
            # args = (
            #     None, None,
            #     (hou.Vector3(1, 0, 0), -15),
            #     (hou.Vector3(1, 0, 0), 15),
            #     (hou.Vector3(0, 1, 0), -15), (hou.Vector3(0, 1, 0), 15),
            #     hou.Vector3(0, 1, 0), hou.Vector3(0, -1, 0),
            #     hou.Vector3(-1, 0, 0), hou.Vector3(1, 0, -1)
            # )


    def onMenuAction(self, kwargs):
        map = {
            "kCam.frame": self.kCam.frame,
            "kCam.reset": self.kCam.reset,
            "kViewport.frame": self.kViewport.frame,
            "kGuides.camAxis": self.kGuides.camAxis.toggle,
            "kGuides.pivotAxis": self.kGuides.pivotAxis.toggle,
            "kGuides.perim": self.kGuides.perim.toggle,
            "kGuides.pivot2d": self.kGuides.pivot2d.toggle,
            "kGuides.ray": self.kGuides.ray.toggle
        }
        map.get(kwargs["menu_item"], lambda: False)
        self.kGuides.update()


    def onParmChangeEvent(self, kwargs):
        if kwargs["parm_name"] == "t":
            self.kParms._t = self.kParms.parms["t"]["value"]
            self.kCam.cam.parmTuple("t").set(self.kParms.t)
        elif kwargs["parm_name"] == "p":
            self.kParms._p = self.kParms.parms["p"]["value"]
            self.kCam.cam.parmTuple("t").set(self.kParms.p)
        elif kwargs["parm_name"] == "r":
            self.kParms._r = self.kParms.parms["r"]["value"]
            self.kCam.cam.parmTuple("r").set(self.kParms.r)
        # self.kGuides.update()


    def setView(self):
        if self.kParms.view == "top":      self.kParms.r = hou.Vector3(270, 0, 0)
        elif self.kParms.view == "bottom": self.kParms.r = hou.Vector3(90, 0, 0)
        elif self.kParms.view == "front":  self.kParms.r = hou.Vector3(0, 180, 0)
        elif self.kParms.view == "back":   self.kParms.r = hou.Vector3(0, 0, 0)
        elif self.kParms.view == "right":  self.kParms.r = hou.Vector3(0, 90, 0)
        elif self.kParms.view == "left":   self.kParms.r = hou.Vector3(0, 270, 0)


    def setFocusAttr(self):
        attr = hou.ui.readInput("focus_attr", buttons=("OK","Cancel"), initial_contents=self.hud_state_focus["focus_attr"])
        if attr[0] == 0: self.focus_state["focus_attr"] = attr[1]


    def updateNetworkContext(self):
        node = self.sceneViewer.pwd()
        self.context = node.type().name()


    def updateOptions(self):
        # Reset cam, or else set state from cam.
        if self.options["cam_reset"]: self.kParms.reset()
        else:                         self.kParms.camToState()
        # keycam node display flag
        # self.cam.setDisplayFlag(self.guide_states["camGeo"])


def createViewerStateTemplate():
    template = hou.ViewerStateTemplate(
        type_name="keycam",
        label="keycam",
        category=hou.sopNodeTypeCategory(),
        contexts=[hou.objNodeTypeCategory()]
    )

    template.bindFactory(State)
    template.bindIcon("DESKTOP_application_sierra")

    # State parameters
    template.bindParameter(hou.parmTemplateType.Menu,      name="layout",   label="Layout",         default_value="single", menu_items=[("doubleside","DoubleSide"), ("doublestack","DoubleStack"), ("quad","Quad"), ("quadbottomsplit","QuadBottomSplit"), ("quadleftsplit","QuadLeftSplit"), ("single","Single"), ("triplebottomsplit","TripleBottomSplit"), ("tripleleftsplit","TripleLeftSplit")])
    template.bindParameter(hou.parmTemplateType.Menu,      name="viewport", label="Viewport",       default_value="center", menu_items=[("center","Center")])
    template.bindParameter(hou.parmTemplateType.Menu,      name="view",     label="View",           default_value="persp",  menu_items=[("persp","Persp"), ("top","Top"), ("front","Front"), ("right","Right"), ("uv","UV"), ("bottom","Bottom"), ("back","Back"), ("left","Left")])
    template.bindParameter(hou.parmTemplateType.Menu,      name="camera",   label="Camera",         default_value="keycam", menu_items=[("keycam","Keycam"), ("default","Default"), ("other","Other")], toolbox=False)
    template.bindParameter(hou.parmTemplateType.Separator, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Menu,      name="target",   label="Target",         default_value="cam",    menu_items=[("cam","Cam"), ("pivot","Pivot")], toolbox=False)
    template.bindParameter(hou.parmTemplateType.Separator, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float,     name="delta_r",  label="Delta R",        default_value=7.5,      min_limit=-180.0, max_limit=180.0)
    template.bindParameter(hou.parmTemplateType.Float,     name="delta_t",  label="Delta T",        default_value=1.0,      min_limit=0,      max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float,     name="delta_z",  label="Delta Z",        default_value=1.0,      min_limit=0,      max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float,     name="delta_ow", label="Delta OW",       default_value=1.0,      min_limit=0,      max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Separator, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float,     name="t",        label="Translation",    num_components=3, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float,     name="r",        label="Rotation",       num_components=3, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float,     name="p",        label="Pivot",          num_components=3, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float,     name="pr",       label="Pivot Rotation", num_components=3, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float,     name="ow",       label="Ortho Width",    num_components=1, toolbox=False)

    # State menu
    menu = hou.ViewerStateMenu("keycamMenu", "Keycam Menu")
    menu.addActionItem("camFrame", "camFrame")
    menu.addActionItem("camReset", "camReset")
    menu.addActionItem("viewportFrame", "viewportFrame")
    menu.addToggleItem("axis_cam", "axis_cam", 1)
    menu.addToggleItem("axis_pivot", "axis_pivot", 1)
    menu.addToggleItem("perim", "perim", 1)
    menu.addToggleItem("pivot_2d", "pivot_2d", 0)
    menu.addToggleItem("pivot_3d", "pivot_3d", 1)
    menu.addToggleItem("ray", "ray", 1)
    template.bindMenu(menu)
    return template



class KCam():

    def __init__(self, state):
        self.state = state
        self.cam = hou.node("/obj/keycam")
        # self.nodeCheck()
        self.lock()


    def frame(self):
        centroid = self.state.kGeo.centroid()
        self.state.kParms.t = centroid
        self.state.kParms.p = centroid
        # self.state.kParms.ow = 10
        self.setZoom(6)


    def home(self):
        centroid = self.state.kGeo.centroid()
        self.state.kParms.t = centroid
        self.state.kParms.p = centroid
        # self.state.kParms.ow = 10
        # self.setZoom(6)


    def lock(self):
        self.state.kSceneViewer.viewport.setCamera(self.cam)
        self.state.kSceneViewer.viewport.lockCameraToView(1)


    def unlock(self):
        self.state.kSceneViewer.viewport.lockCameraToView(0)


    def movePivot(self):
        # If origin
        if self.kParms.target == 0:
            self.kParms.t = [0, 0, self.kParms.dist]
            self.kParms.r = [45, 45, 0]
            self.kParms.p = [0, 0, self.kParms.dist * -1]
            self.kParms.ow = 10


    def nextProjection(self):
        parm = self.cam.parm("projection")
        proj = parm.evalAsString()
        if proj == "ortho": parm.set("perspective")
        elif proj == "perspective": parm.set("ortho")


    # Create keycam node if nonexistant
    def nodeCheck(self):
        children = hou.node("/obj").children()
        names = [node.name() for node in children]
        if "keycam" not in names:
            cam = hou.node("/obj").createNode("cam")
            cam.setName("keycam")
            cam.parm("xOrd").set(0)
        self.cam = hou.node("/obj/keycam")


    def rotate(self, m):
        self.state.kParms.t -= self.state.kParms.p
        self.state.kParms.t *= m
        self.state.kParms.t += self.state.kParms.p
        self.state.kParms.local_x *= m
        self.state.kParms.local_y *= m
        self.state.kParms.local_z *= m


    def rotateUp(self):
        self.state.kParms.r = hou.Vector3(self.state.kParms.r[0] + self.state.kParms.delta_r, self.state.kParms.r[1], self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(self.state.kParms.local_x, self.state.kParms.delta_r)
        self.rotate(m)


    def rotateDown(self):
        self.state.kParms.r = hou.Vector3(self.state.kParms.r[0] - self.state.kParms.delta_r, self.state.kParms.r[1], self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(self.state.kParms.local_x, self.state.kParms.delta_r * -1)
        self.rotate(m)


    def rotateLeft(self):
        self.state.kParms.r = hou.Vector3(self.state.kParms.r[0], self.state.kParms.r[1] - self.state.kParms.delta_r, self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(self.state.kParms.global_y, self.state.kParms.delta_r * -1)
        self.rotate(m)


    def rotateRight(self):
        self.state.kParms.r = hou.Vector3(self.state.kParms.r[0], self.state.kParms.r[1] + self.state.kParms.delta_r, self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(self.state.kParms.global_y, self.state.kParms.delta_r)
        self.rotate(m)


    def translateUp(self):
        move = self.state.kParms.local_y * self.state.kParms.delta_t * -1
        self.state.kParms.t += move


    def translateDown(self):
        move = self.state.kParms.local_y * self.state.kParms.delta_t
        self.state.kParms.t += move


    def translateLeft(self):
        move = self.state.kParms.local_x * self.state.kParms.delta_t * -1
        self.state.kParms.t += move


    def translateRight(self):
        move = self.state.kParms.local_x * self.state.kParms.delta_t
        self.state.kParms.t += move


    def update(self):
        self.cam.parmTuple("t").set(self.state.kParms.t)
        self.cam.parmTuple("r").set(self.state.kParms.r)
        self.cam.parm("orthowidth").set(self.state.kParms.ow)


    def updateAspectRatio(self):
        self.cam.parm("resx").set(1000)
        self.cam.parm("resy").set(1000)
        viewport = self.state.sceneViewer.findViewport("persp1")
        ratio = viewport.size()[2] / viewport.size()[3]
        self.cam.parm("aspect").set(ratio)


    def setZoom(self, zoom):
        move = self.state.kParms.local_z * zoom
        self.state.kParms.t += move


    def zoomIn(self):
        move = self.state.kParms.local_z * self.state.kParms.delta_z * -1
        self.state.kParms.t += move


    def zoomOut(self):
        move = self.state.kParms.local_z * self.state.kParms.delta_z
        self.state.kParms.t += move


    def setOrthoZoom(self, zoom_level):
        self.state.kParms.ow = zoom_level


    def orthoZoomIn(self):
        self.state.kParms.ow += self.state.kParms.delta_z * -1


    def orthoZoomOut(self):
        self.state.kParms.ow += self.state.kParms.delta_z



class KDefaultCam():

    def __init__(self):
        return


    def frame(self):
        viewports = self.sceneViewer.viewports()
        for viewport in viewports:
            cam = viewport.camera()
            # Is cam default or node.
            if cam == None:
                viewport.frameAll()
        self.camToState()


    def up(self, indices):
        return


    def down(self, indices):
        return


    def left(self, indices):
        return


    def right(self, indices):
        return



class KGeo():

    def __init__(self, state):
        self.state = state
        self.geo = hou.Geometry()
        self.geo_type = hou.drawableGeometryType.Line
        self.name = "geo"
        self.color = hou.Vector4((1, 1, 1, 0.5))
        self.geo_parms = {"color1":self.color}
        self.geo_drawable = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=self.geo_type,
            name=self.name,
            params=self.geo_parms)


    def bbox(self):
        geo = self.get()
        bbox = geo.boundingBox()
        return bbox


    def centroid(self):
        geo_in = self.get()
        geo_out = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(geo_out, [geo_in])
        pt = geo_out.point(0)
        centroid = pt.position()
        return centroid


    def get(self):
        self.displayNode = None
        pwd = self.state.sceneViewer.pwd()
        self.context = pwd.childTypeCategory().label()
        if self.context == "dop":        displayNode = pwd.displayNode()
        elif self.context == "lop":      return None
        elif self.context == "Objects":  displayNode = pwd.children()[0].displayNode()
        elif self.context == "Geometry": displayNode = pwd.displayNode()
        return displayNode.geometry()


    def home(self):
        self.displayNode = None
        pwd = self.sceneViewer.pwd()
        self.context = pwd.childTypeCategory().label()



class KGuides():
    def __init__(self, state):
        self.state = state
        self.guides = []
        self.axis_size = 1
        self.camAxis= 1
        self.pivotAxis = 0
        self.bbox = 0
        self.camGeo = 1
        self.perim = 0
        self.pivot2d = 0
        self.pivot3d = 1
        self.ray = 1
        self.tie_axis_to_radius = 0

        self.CamAxis =   hou.GeometryDrawable(scene_viewer=self.state.sceneViewer, geo_type=hou.drawableGeometryType.Line, name="Cam axis")
        self.PivotAxis = hou.GeometryDrawable(scene_viewer=self.state.sceneViewer, geo_type=hou.drawableGeometryType.Line, name="Pivot axis", params={"color1":hou.Vector4((1, 1, 1, 0.5))})
        self.Bbox =      hou.GeometryDrawable(scene_viewer=self.state.sceneViewer, geo_type=hou.drawableGeometryType.Line, name="bbox",       params={"color1":hou.Vector4((1, 1, 1, 0.3))})
        self.Perim =     hou.GeometryDrawable(scene_viewer=self.state.sceneViewer, geo_type=hou.drawableGeometryType.Line, name="perim")
        self.Pivot2d =   hou.GeometryDrawable(scene_viewer=self.state.sceneViewer, geo_type=hou.drawableGeometryType.Line, name="pivot2d")
        self.Pivot3d =   hou.GeometryDrawable(scene_viewer=self.state.sceneViewer, geo_type=hou.drawableGeometryType.Face, name="pivot3d")
        self.Pivot3d.setParams({"color1":hou.Vector4(0.8, 0.8, 0.4, 0.7), "fade_factor":0.5})
        self.Ray =       hou.GeometryDrawable(scene_viewer=self.state.sceneViewer, geo_type=hou.drawableGeometryType.Line, name="ray",        params={"color1":hou.Vector4((1, 0.8, 1, 0.5))})


    def toggle(self, kwargs, guide):
        kwargs[guide] = not kwargs[guide]
        self.update_bbox()


    def update(self):
        if self.guide_states["axis_cam"]: self.updateAxisCam()
        else: self.Cam.show(0)

        if self.guide_states["axis_pivot"]: self.updateAxisPivot()
        else: self.AxisPivot.show(0)

        if self.guide_states["bbox"]: self.updateBbox()
        else: self.Bbox.show(0)

        if self.guide_states["perim"]: self.updatePerim()
        else: self.Perim.show(0)

        if self.guide_states["pivot2d"]: self.updatePivot2d()
        else: self.Pivot2d.show(0)

        if self.guide_states["pivot3d"]: self.updatePivot3d()
        else: self.Pivot3d.show(0)

        if self.guide_states["ray"]: self.updateRay()
        else: self.Ray.show(0)

        # if self.guide_states["text"]:
        #     self.updateText()
        # if not Text:
        #     self.Text = hou.TextDrawable(
        #         scene_viewer=self.sceneViewer,
        #         name="text",
        #         label="test")


    def updateCamAxis(self):
        axes = (self.state.kParms.local_x, self.state.kParms.local_y, self.state.kParms.local_z)
        geo = hou.Geometry()
        for i in range(3):
            P0 = self.state.kParms.t + axes[i]
            P1 = self.state.kParms.t + axes[i] * -1
            pts = geo.createPoints((P0, P1))
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pts[0])
            poly.addVertex(pts[1])
        self.CamAxis.setGeometry(geo)
        self.CamAxis.show(1)


    def updatePivotAxis(self):
        axes = (hou.Vector3(1, 0, 0), hou.Vector3(0, 1, 0), hou.Vector3(0, 0, 1))
        colors = ([1.0, 0.7, 0.7], [0.7, 1.0, 0.7], [0.7, 0.7, 1.0])
        geo = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, "Cd", (0.1, 0.1, 0.1))
        for i in range(3):
            P0 = self.state.kParms.p + axes[i]
            P1 = self.state.kParms.p + axes[i] * -1
            pt_arr = geo.createPoints((P0, P1))
            pt_arr[0].setAttribValue("Cd", colors[i])
            pt_arr[1].setAttribValue("Cd", colors[i])
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
        self.AxisPivot.setGeometry(geo)
        self.AxisPivot.setParams({"fade_factor": 0.0})
        self.AxisPivot.show(1)


    def updateBbox(self):
        geo  = self.get_get()
        # bbox = geo.boundingBox()
        # P0 = (bbox[0], bbox[1], bbox[2])
        # P1 = (bbox[0], bbox[1], bbox[5])
        # P2 = (bbox[3], bbox[1], bbox[5])
        # P3 = (bbox[3], bbox[1], bbox[2])
        # P4 = (bbox[0], bbox[4], bbox[2])
        # P5 = (bbox[0], bbox[4], bbox[5])
        # P6 = (bbox[3], bbox[4], bbox[5])
        # P7 = (bbox[3], bbox[4], bbox[2])
        #print(bbox)
        self.Bbox.setGeometry(geo)
        self.Bbox.show(1)


    def updatePerim(self):
        rad  = self.state.kParms.p.distanceTo(self.state.kParms.t)
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({"divs":128, "type":1, "t":self.state.kParms.p, "scale":rad, "orient":2})
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.perim.setParams({"color1":hou.Vector4(1.0, 1.0, 1.0, 0.25), "fade_factor":1.0})
        self.Perim.setGeometry(geo)
        self.Perim.show(1)


    def updatePivot2d(self):
        P = self.state.kParms.p + self.state.kParms.t
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({"type":1, "r":self.state.kParms.r, "t":P, "scale":self.state.kParms.ow * 0.0075})
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.pivot2d.setParams({"color1":hou.Vector4(0.0, 0.0, 1, 1), "fade_factor":1.0})
        self.Pivot2d.setGeometry(geo)
        self.Pivot2d.show(1)


    def updatePivot3d(self):
            verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
            verb.setParms({"type":1, "t":self.state.kParms.p, "scale":self.self.state.kParms.t.distanceTo(self.state.kParms.p) * 0.002})
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.Pivot3d.setGeometry(geo)
            self.Pivot3d.show(1)


    def updateRay(self):
            geo = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
            pt_arr = geo.createPoints((self.state.kParms.p, self.state.kParms.t))
            poly = geo.createPolygon()
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
            self.Ray.setGeometry(geo)
            self.Ray.show(1)


    def updateText(self):
        return



class KHud():

    def __init__(self, state):
        self.state = state

        self.template = {
            "title": "test",
            "rows": [
                {"id":"layout",     "type":"plain",       "label":"Layout",   "value":"Single", "key":"Ctl+l"},
                {"id":"layout_g",   "type":"choicegraph", "count":8},
                {"id":"viewport",   "type":"plain",       "label":"Viewport", "value":"0",      "key":"Ctl+v"},
                {"id":"viewport_g", "type":"choicegraph", "count":4},
                {"id":"view"   ,    "type":"plain",       "label":"View",     "value":"Persp",  "key":"v"},
                {"id":"view_g",     "type":"choicegraph", "count":8},
                {"id":"divider0",   "type":"divider"},
                {"id":"target",     "type":"plain",       "label":"Target",   "value":"Cam",    "key":"t"},
                {"id":"target_g",   "type":"choicegraph", "count":2},
                # Delta
                {"id":"divider1",   "type":"divider"},
                {"id":"r",          "type":"plain",       "label":"Delta r"},
                {"id":"t",          "type":"plain",       "label":"Delta t"},
                {"id":"z",          "type":"plain",       "label":"Delta z"},
                {"id":"ow",         "type":"plain",       "label":"Delta ow"},
                # Vis
                {"id":"divider2",   "type":"divider"},
                {"id":"vis",        "type":"plain",       "label":"Vis"},
                # Focus
                {"id":"divider3",   "type":"divider"},
                {"id":"focus",      "type":"plain",       "label":"Focus", "value":0},
                {"id":"focus_g",    "type":"choicegraph", "count":10}
            ]
        }

        self.hud_state = {
            "controls":  ("layout", "viewport", "set_view", "target", "r", "t", "ow", "dist", "vis", "focus"),
            "control":   "layout",
            "layouts":   ("DoubleSide", "DoubleStack", "Quad", "QuadBottomSplit", "QuadLeftSplit", "Single", "TripleBottomSplit", "TripleLeftSplit"),
            "layout":    "Single",
            "viewports": ("0"),
            "viewport":  "0",
            "views":     ("top", "bottom", "left", "right", "front", "back", "persp", "none"),
            "view":      "persp",
            "targets":   ("cam", "pivot"),
            "target":    "cam",
            "r":         self.state.kParms.delta_r,
            "t":         self.state.kParms.delta_t,
            "ow":        self.state.kParms.delta_z,
            "z":      self.state.kParms.delta_z,
            "vis_arr":   ("test1", "test2", "test3"),
            "vis":       "test1",
            "focuss":    ("test1", "test2", "test3"),
            "focus":     "test1"
        }

        self.state.sceneViewer.hudInfo(template=self.template)
        self.update()


    def update(self):
        # Update graph bar count
        # self.updateGraph()

        updates = {
            "r": self.state.kParms.delta_r,
            "t": self.state.kParms.delta_t,
            "z": self.state.kParms.delta_z,
            "ow": self.state.kParms.delta_z
        }

        self.template["rows"][3]["count"] = 3 # layout_g

        # for row in self.template["rows"]:
            # Skip processing dividers.
        #     if "divider" not in row["id"]:

        #         # Graph
        #         elif row["id"][-2:] == "_g":
        #             control_name = row["id"][0:-2]
        #             control_value = self.hud_state[control_name]
        #             control_values = self.hud_state[control_name + "s"]

        #             updates[row["id"]] = {"value": control_values.index(control_value)}

        #         # Other
        #         else:
        #             control_name = row["id"]
        #             control_value = self.hud_state[control_name]
        #             updates[row["id"]] = {"value": control_value}

        #     updates[self.hud_state["control"]]["value"] = "[" + updates[self.hud_state["control"]]["value"] + "]"
        # Apply
        self.state.sceneViewer.hudInfo(hud_values=updates)


    def updateGraph(self):
        # Calculate the number of bars in a graph based on the length of the appropriate array
        for i, row in enumerate(self.template["rows"]):
            # If row ID indicates it is a graph
            if row["id"][-2:] == "_g":
                arr = None
                # Count the number of items in the array
                if row["id"] == "hud_g":
                    arr = self.hud_names
                else:
                    arr = self.hud_state[row["id"][0:-2] + "s"]
                # Set the number of bars in the graph.
                self.template["rows"][i]["count"] = len(arr)



class KParms():

    def __init__(self, state):
        self.state = state
        self.parms = state.kwargs["state_parms"]

        self.local_x = hou.Vector3(0, 0, 0)
        self.local_y = hou.Vector3(0, 0, 0)
        self.local_z = hou.Vector3(0, 0, 0)
        self.global_x = hou.Vector3(0, 0, 0)
        self.global_y = hou.Vector3(0, 0, 0)
        self.global_z = hou.Vector3(0, 0, 0)

        self._p = None
        self._r = None
        self._t = None
        self._dist = None
        self._ow = None
        self._target = None
        self._delta_r = None
        self._delta_t = None
        self._delta_z = None
        self._layout = None
        self._viewport = None

        self.reset()


    def reset(self):
        self.t = hou.Vector3(0, 0, 0)
        self.r = hou.Vector3(0, 0, 0)
        self.p = hou.Vector3(0, 0, 0)
        self.ow = 10
        self.delta_t = 1
        self.delta_r = 15
        self.delta_z = 1
        self.local_x = hou.Vector3(1, 0, 0)
        self.local_y = hou.Vector3(0, 1, 0)
        self.local_z = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)


    @property
    def p(self): return self._p
    @property
    def r(self): return self._r
    @property
    def t(self): return self._t
    @property
    def dist(self): return self._dist
    @property
    def ow(self): return self._ow
    @property
    def target(self): return self._target
    @property
    def delta_r(self): return self._delta_r
    @property
    def delta_t(self): return self._delta_t
    @property
    def delta_z(self): return self._delta_z
    @property
    def layout(self): return self._layout
    @property
    def viewport(self): return self._viewport

    @p.setter
    def p(self, val):
        self._p = val
        self.parms["p"]["value"] = val
        self.state.kCam.cam.parmTuple("p").set(val)
    @r.setter
    def r(self, val):
        self._r = val
        self.parms["r"]["value"] = list(val)
        self.state.kCam.cam.parmTuple("r").set(val)
    @t.setter
    def t(self, val):
        self._t = val
        self.parms["t"]["value"] = list(val)
        self.state.kCam.cam.parmTuple("t").set(val)
    @dist.setter
    def dist(self, val):
        self._dist = val
        self.parms["dist"]["value"] = val
    @ow.setter
    def ow(self, val):
        self._ow = val
        self.parms["ow"]["value"] = val
        self.state.kCam.cam.parm("orthowidth").set(val)
    @target.setter
    def target(self, val):
        self._target = val
        self.parms["target"]["value"] = val
    @delta_r.setter
    def delta_r(self, val):
        self._delta_r = val
        self.parms["delta_r"]["value"] = val
    @delta_t.setter
    def delta_t(self, val):
        self._delta_t = val
        self.parms["delta_t"]["value"] = val
    @delta_z.setter
    def delta_z(self, val):
        self._delta_z = val
        self.parms["delta_z"]["value"] = val
    @layout.setter
    def layout(self, val):
        self._layout = val
        self.parms["layout"]["value"] = val
        indices = (0, 0)
        if val == 0:   self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleSide);        indices = (2, 3)
        elif val == 1: self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.DoubleStack);       indices = (3, 0)
        elif val == 2: self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.Quad);              indices = (2, 3, 1, 0)
        elif val == 3: self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadBottomSplit);   indices = (3, 2, 1, 0)
        elif val == 4: self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.QuadLeftSplit);     indices = (2, 1, 0, 3)
        elif val == 5: self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.Single);            indices = (3)
        elif val == 6: self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleBottomSplit); indices = (3, 1, 0)
        elif val == 7: self.state.kSceneViewer.setViewportLayout(hou.geometryViewportLayout.TripleLeftSplit);   indices = (2, 3, 1)
    @viewport.setter
    def set_viewport(self, val):
        self._viewport = val
        self.parms["viewport"]["value"] = val


    def camToState(self):
        self.t = self.cam.evalParmTuple("t")
        self.p = self.cam.evalParmTuple("p")
        self.r = self.cam.evalParmTuple("r")
        self.pr = self.cam.evalParmTuple("pr")
        self.ow = self.cam.evalParm("orthowidth")



class KSceneViewer():
# Guide to layout/viewport IDs:
# DoubleSide:        2 3
# DoubleStack:       3
#                    0
# Quad:              2 3
#                    1 0
# QuadBottomSplit:     3
#                    2 1 0
# QuadLeftSplit:     2
#                    1 3
#                    0
# TripleBottomSplit:   3
#                    1   0
# TripleLeftSplit:   2
#                    0 3
#                    1
# Single:
# setViewportLayout(layout, single=-1)
# -1: current viewport (viewportmouse is/was over)
# 0: top-left viewport from quad layout (default Top)
# 1: top-right viewport from quad layout (default Perspective)
# 2: bottom-left viewport from quad layout (default Front)
# 3: bottom-right viewport from quad layout (default Right)

    def __init__(self, state):
        self.state = state
        self.sceneViewer = state.sceneViewer
        self.viewport = self.curViewport()
        self.viewports = self.viewports()
        self.viewports = self.viewports[::-1]
        self.curLayout = self.viewportLayout()


    def curViewport(self):
        return self.sceneViewer.curViewport()

    def nextViewport(self):
        return

    def setViewportLayout(self, layout):
        self.sceneViewer.setViewportLayout(layout)


    def viewportLayout(self):
        return self.sceneViewer.viewportLayout()


    def viewports(self):
        return self.sceneViewer.viewports()


    def setType(self, viewportType):
        viewport = self.sceneViewer.findViewport(self.layout_state["viewport"])
        viewport.changeType(viewportType)



class KUtils():

    def __init__(self):
        return


    def arrNext(self, arr, cur):
        index = arr.index(cur)
        index = (index + 1) % len(arr)
        return index


    def arrPrev(self, arr, cur):
        index = arr.index(cur)
        index = (index - 1) % len(arr)
        return index



class KViewport():

    def __init__(self):
        return


    def focus(self):
        return


    def frame(self):
        for viewport in self.viewports:
            cam = viewport.camera()
            # Is camera node or default.
            if cam == None: viewport.frameAll()
            else: viewport.frameAll()
        self.camToState()


    # def swap(self):
        # viewport_names = [viewport.name() for viewport in self.viewports]
        # self.viewports = self.viewports[1:] + [self.viewports[0]]
        # viewportTypes = viewportTypes[1:] + [viewportTypes[0]]
        # for i, viewport in enumerate(self.viewports):
            # viewport.changeName("v" * i)
        # for i, viewport in enumerate(self.viewports):
            # viewport.changeName(self.viewports[i])
            # viewport.changeType(viewportTypes[i])
