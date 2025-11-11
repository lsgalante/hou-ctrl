import hou


def createViewerStateTemplate():
    # Define template
    template = hou.ViewerStateTemplate(
        type_name="keycam",
        label="keycam",
        category=hou.sopNodeTypeCategory(),
        contexts=[hou.objNodeTypeCategory()],
    )
    template.bindFactory(State)
    template.bindIcon("DESKTOP_application_sierra")
    # Parameters
    template.bindParameter(
        hou.parmTemplateType.Menu,
        name="layout",
        label="Layout",
        default_value="single",
        menu_items=[
            ("doubleside", "DoubleSide"),
            ("doublestack", "DoubleStack"),
            ("quad", "Quad"),
            ("quadbottomsplit", "QuadBottomSplit"),
            ("quadleftsplit", "QuadLeftSplit"),
            ("single", "Single"),
            ("triplebottomsplit", "TripleBottomSplit"),
            ("tripleleftsplit", "TripleLeftSplit"),
        ],
    )
    template.bindParameter(
        hou.parmTemplateType.Menu,
        name="viewport",
        label="Viewport",
        default_value="center",
        menu_items=[("center", "Center")],
    )
    template.bindParameter(
        hou.parmTemplateType.Menu,
        name="view",
        label="View",
        default_value="persp",
        menu_items=[
            ("persp", "Perspective"),
            ("top", "Top"),
            ("front", "Front"),
            ("right", "Right"),
            ("uv", "UV"),
            ("bottom", "Bottom"),
            ("back", "Back"),
            ("left", "Left"),
        ],
    )
    template.bindParameter(
        hou.parmTemplateType.Menu,
        name="camera",
        label="Camera",
        default_value="keycam",
        menu_items=[("keycam", "Keycam"), ("default", "Default"), ("other", "Other")],
        toolbox=False,
    )
    template.bindParameter(
        hou.parmTemplateType.Menu,
        name="target",
        label="Target",
        default_value="cam",
        menu_items=[("cam", "Camera"), ("pivot", "Pivot")],
        toolbox=False,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="delta_r",
        label="Delta R",
        default_value=15.0,
        min_limit=-180.0,
        max_limit=180.0,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="delta_t",
        label="Delta T",
        default_value=1.0,
        min_limit=0,
        max_limit=10.0,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="delta_z",
        label="Delta Z",
        default_value=10.0,
        min_limit=0,
        max_limit=10.0,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="delta_ow",
        label="Delta OW",
        default_value=1.0,
        min_limit=0,
        max_limit=10.0,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="t",
        label="Translation",
        num_components=3,
        toolbox=False,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="r",
        label="Rotation",
        num_components=3,
        toolbox=False,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="p",
        label="Pivot",
        num_components=3,
        toolbox=False,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="z",
        label="Zoom",
        num_components=1,
        toolbox=False,
    )
    template.bindParameter(
        hou.parmTemplateType.Float,
        name="ow",
        label="Ortho Width",
        num_components=1,
        toolbox=False,
    )
    # Context menu
    menu = hou.ViewerStateMenu("keycamMenu", "Keycam Menu")
    menu.addActionItem("frame", "Frame")
    menu.addActionItem("reset", "Reset")
    menu.addToggleItem("bbox", "Bbox", 1)
    menu.addToggleItem("cam_axis", "Camera Axis", 1)
    menu.addToggleItem("pivot_axis", "Pivot Axis", 1)
    menu.addToggleItem("perim", "Perimeter", 0)
    menu.addToggleItem("pivot2d", "2D Pivot", 1)
    menu.addToggleItem("pivot3d", "3D Pivot", 0)
    menu.addToggleItem("ray", "Ray", 0)
    template.bindMenu(menu)
    # Ok
    return template


class State(object):
    def __init__(self, state_name, scene_viewer):
        self.sceneViewer = scene_viewer
        self.cam_type = None
        self.context = None
        self.kCam = None
        self.kGeo = None
        self.kGuides = None
        self.kHud = None
        self.kParms = None
        self.kSceneViewer = KSceneViewer(self)
        self.kwargs = None
        self.options = {
            "center_on_geo": 1,
            "lock_cam": 1,
            "reset": 1,
            "show_bbox": 1,
            "show_perim": 0,
            "show_pivot2d": 1,
            "show_pivot3d": 0,
            "show_ray": 0,
        }

    def onDraw(self, kwargs):
        handle = kwargs["draw_handle"]
        self.kGuides.camAxis.draw(handle, {})
        self.kGuides.pivotAxis.draw(handle, {})
        self.kGuides.perim.draw(handle, {})
        self.kGuides.pivot2d.draw(handle, {})
        self.kGuides.pivot3d.draw(handle, {})
        self.kGuides.ray.draw(handle, {})
        # self.kGuides.Text.draw(handle, {})

    def onExit(self, kwargs):
        for viewport in self.sceneViewer.viewports():
            viewport.lockCameraToView(False)

    def onGenerate(self, kwargs):
        # Prevent exiting the state when current node changes
        kwargs["state_flags"]["exit_on_node_select"] = False
        self.kwargs = kwargs
        self.kSceneViewer = KSceneViewer(self)
        self.kGeo = KGeo(self)
        self.kCam = KCam(self)
        self.kGuides = KGuides(self)
        self.kHud = KHud(self)
        self.kParms = KParms(self)
        self.kParms.reset()
        self.kGuides.update()
        # self.kCam.frame()
        self.kHud.update()
        self.updateNetworkContext()
        self.updateOptions()

    def onKeyEvent(self, kwargs):
        self.kCam.updateAspectRatio()
        # Node cam
        keymap = {
            "-": self.kCam.zoomOut,
            "=": self.kCam.zoomIn,
            "o": self.kCam.nextProjection,
            "h": self.kCam.rotateLeft,
            "j": self.kCam.rotateUp,
            "k": self.kCam.rotateDown,
            "l": self.kCam.rotateRight,
            "v": self.kSceneViewer.nextView,
            "Shift+-": self.kCam.orthoZoomOut,
            "Shift+=": self.kCam.orthoZoomIn,
            "Shift+h": self.kCam.translateLeft,
            "Shift+j": self.kCam.translateDown,
            "Shift+k": self.kCam.translateUp,
            "Shift+l": self.kCam.translateDown,
            "Ctrl+l": self.kSceneViewer.nextLayout
        }
        key = kwargs["ui_event"].device().keyString()
        keymap.get(key, lambda: False)()
        self.kGuides.update()

        # Default cam
        if 2 == 1:
            if self.viewport.type() == hou.geometryViewportType.Top: self.indices = (0, 1)
            elif self.viewport.type() == hou.geometryViewportType.Bottom: self.indices = (2, 0)
            elif self.viewport.type() == hou.geometryViewportType.Front: self.indices = (0, 1)
            elif self.viewport.type() == hou.geometryViewportType.Back: self.indices = (1, 0)
            elif self.viewport.type() == hou.geometryViewportType.Right: self.indices = (0, 1)
            elif self.viewport.type() == hou.geometryViewportType.Left: self.indices = (1, 2)

            keymap = {
                "-": self.kDefaultCam.zoomOut,
                "+": self.kDefaultCam.zoomIn,
                # hou.Vector3(0, 1, 0)
                "h": self.kDefaultCam.translateLeft,
                # hou.Vector3(0, -1, 0),
                "j": self.kDefaultCam.translateDown,
                # hou.Vector3(-1, 0, 0)
                "k": self.kDefaultCam.translateUp,
                # hou.Vector3(1, 0, -1)
                "l": self.kDefaultCam.translateRight,
                "v": self.kDefaultCam.nextView,
                # (hou.Vector3(1, 0, 0), -15),
                "Shift+h": self.kDefaultCam.rotateLeft,
                # (hou.Vector3(1, 0, 0), 15),
                "Shift+j": self.kDefaultCam.rotateUp,
                # (hou.Vector3(0, 1, 0), -15)
                "Shift+k": self.kDefaultCam.rotateDown,
                # (hou.Vector3(0, 1, 0), 15),
                "Shift+l": self.kDefaultCam.rotateRight,
                "Ctrl+l": self.kSceneViewer.nextLayout
            }

    def onMenuAction(self, kwargs):
        menu_item = kwargs["menu_item"]
        method = getattr(self, "_" + kwargs["menu_item"])
        return method(kwargs)
        # self.kGuides.update()
    def _frame(self, kwargs): self.kCam.frame()
    def _reset(self, kwargs): self.kParms.reset()
    def _cam_axis(self, kwargs): self.kGuides.camAxis.show(kwargs["cam_axis"])
    def _pivot_axis(self, kwargs): self.kGuides.pivotAxis.show(kwargs["pivot_axis"])
    def _perim(self, kwargs): self.kGuides.pivotAxis.show(kwargs["perim"])
    def _2d_pivot(self, kwargs): self.kGuides.pivot2d.show(kwargs["2d_pivot"])
    def _3d_pivot(self, kwargs): self.kGuides.pivot3d.show(kwargs["3d_pivot"]),
    def _ray(self, kwargs): self.kGuides.ray.show(kwargs["ray"])

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
        if self.kParms.view == "top": self.kParms.r = hou.Vector3(270, 0, 0)
        elif self.kParms.view == "bottom": self.kParms.r = hou.Vector3(90, 0, 0)
        elif self.kParms.view == "front": self.kParms.r = hou.Vector3(0, 180, 0)
        elif self.kParms.view == "back": self.kParms.r = hou.Vector3(0, 0, 0)
        elif self.kParms.view == "right": self.kParms.r = hou.Vector3(0, 90, 0)
        elif self.kParms.view == "left": self.kParms.r = hou.Vector3(0, 270, 0)

    def setFocusAttr(self):
        attr = hou.ui.readInput(
            "focus_attr",
            buttons=("OK","Cancel"),
            initial_contents=self.hud_state_focus["focus_attr"])
        if attr[0] == 0: self.focus_state["focus_attr"] = attr[1]

    def updateNetworkContext(self):
        node = self.sceneViewer.pwd()
        self.context = node.type().name()

    def updateOptions(self):
        if self.options["reset"]: self.kParms.reset()
        else:                     self.kParms.camToState()
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

    # Parameters
    template.bindParameter(hou.parmTemplateType.Menu, name="layout", label="Layout", default_value="single", menu_items=[("doubleside","DoubleSide"), ("doublestack","DoubleStack"), ("quad","Quad"), ("quadbottomsplit","QuadBottomSplit"), ("quadleftsplit","QuadLeftSplit"), ("single","Single"), ("triplebottomsplit","TripleBottomSplit"), ("tripleleftsplit","TripleLeftSplit")])
    template.bindParameter(hou.parmTemplateType.Menu, name="viewport", label="Viewport", default_value="center", menu_items=[("center","Center")])
    template.bindParameter(hou.parmTemplateType.Menu, name="view", label="View", default_value="persp", menu_items=[("persp","Perspective"), ("top","Top"), ("front","Front"), ("right","Right"), ("uv","UV"), ("bottom","Bottom"), ("back","Back"), ("left","Left")])
    template.bindParameter(hou.parmTemplateType.Menu, name="camera", label="Camera", default_value="keycam", menu_items=[("keycam","Keycam"), ("default","Default"), ("other","Other")], toolbox=False)
    template.bindParameter(hou.parmTemplateType.Menu, name="target", label="Target", default_value="cam", menu_items=[("cam","Camera"), ("pivot","Pivot")], toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_r", label="Delta R", default_value=15.0, min_limit=-180.0, max_limit=180.0)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_t", label="Delta T", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_z", label="Delta Z", default_value=10.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_ow", label="Delta OW", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="t", label="Translation", num_components=3, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="r", label="Rotation", num_components=3, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="p", label="Pivot", num_components=3, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="z", label="Zoom", num_components=1, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="ow", label="Ortho Width", num_components=1, toolbox=False)

    # Context menu
    menu = hou.ViewerStateMenu("keycamMenu", "Keycam Menu")
    menu.addActionItem("frame", "Frame")
    menu.addActionItem("reset", "Reset")
    menu.addToggleItem("cam_axis", "Camera Axis", 1)
    menu.addToggleItem("pivot_axis", "Pivot Axis", 1)
    menu.addToggleItem("perim", "Perimeter", 0)
    menu.addToggleItem("2d_pivot", "2D Pivot", 0)
    menu.addToggleItem("3d_pivot", "3D Pivot", 0)
    menu.addToggleItem("ray", "Ray", 0)
    template.bindMenu(menu)

    return template


class KCam():
    def __init__(self, state):
        self.state = state
        # self.cam = hou.node("/obj/keycam")
        self.nodeCheck()
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
        self.state.kSceneViewer.viewport().setCamera(self.cam)
        self.state.kSceneViewer.viewport().lockCameraToView(1)

    def unlock(self):
        self.state.kSceneViewer.viewport().lockCameraToView(0)

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
        self.state.kParms.r = hou.Vector3(
            self.state.kParms.r[0] + self.state.kParms.delta_r,
            self.state.kParms.r[1],
            self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(
            self.state.kParms.local_x,
            self.state.kParms.delta_r)
        self.rotate(m)

    def rotateDown(self):
        self.state.kParms.r = hou.Vector3(
            self.state.kParms.r[0] - self.state.kParms.delta_r,
            self.state.kParms.r[1],
            self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(
            self.state.kParms.local_x,
            self.state.kParms.delta_r * -1)
        self.rotate(m)

    def rotateLeft(self):
        self.state.kParms.r = hou.Vector3(
            self.state.kParms.r[0],
            self.state.kParms.r[1] - self.state.kParms.delta_r,
            self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(
            self.state.kParms.global_y,
            self.state.kParms.delta_r * -1)
        self.rotate(m)

    def rotateRight(self):
        self.state.kParms.r = hou.Vector3(
            self.state.kParms.r[0],
            self.state.kParms.r[1] + self.state.kParms.delta_r,
            self.state.kParms.r[2])
        m = hou.hmath.buildRotateAboutAxis(
            self.state.kParms.global_y,
            self.state.kParms.delta_r)
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
        move = self.state.kParms.local_z * self.state.kParms.delta_z
        self.state.kParms.t -= move

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
    def __init__(self, state):
        return

    def frame(self):
        for viewport in self.kSceneViewer.viewports():
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
        if self.context == "dop": displayNode = pwd.displayNode()
        elif self.context == "lop": return None
        elif self.context == "Objects": displayNode = pwd.children()[0].displayNode()
        elif self.context == "Geometry": displayNode = pwd.displayNode()
        return displayNode.geometry()

    def home(self):
        self.displayNode = None
        pwd = self.sceneViewer.pwd()
        self.context = pwd.childTypeCategory().label()


class KGuides():
    def __init__(self, state):
        self.state = state
        self.camAxis = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="Camera axis")
        self.pivotAxis = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="Pivot axis",
            params={"color1": hou.Vector4((1, 1, 1, 0.5))})
        self.bbox = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))})
        self.perim = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="perim")
        self.pivot2d = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="pivot2d")
        self.pivot3d = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=hou.drawableGeometryType.Face,
            name="pivot3d")
        self.pivot3d.setParams(
            {"color1": hou.Vector4(0.8, 0.8, 0.4, 0.7), "fade_factor": 0.5})
        self.ray = hou.GeometryDrawable(
            scene_viewer=self.state.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="ray",
            params={"color1": hou.Vector4((1, 0.8, 1, 0.5))})

    def toggle(self, kwargs, guide):
        kwargs[guide] = not kwargs[guide]
        self.update_bbox()

    def update(self):
        self.updatePivotAxis()
        # if self.guide_states["axis_cam"]: self.updateAxisCam()
        # else: self.Cam.show(0)

        # if self.guide_states["axis_pivot"]: self.updateAxisPivot()
        # else: self.AxisPivot.show(0)

        # if self.guide_states["bbox"]: self.updateBbox()
        # else: self.Bbox.show(0)

        # if self.guide_states["perim"]: self.updatePerim()
        # else: self.Perim.show(0)

        # if self.guide_states["pivot2d"]: self.updatePivot2d()
        # else: self.Pivot2d.show(0)

        # if self.guide_states["pivot3d"]: self.updatePivot3d()
        # else: self.Pivot3d.show(0)

        # if self.guide_states["ray"]: self.updateRay()
        # else: self.Ray.show(0)

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
        self.camAxis.setGeometry(geo)
        self.camAxis.show(1)

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
        self.pivotAxis.setGeometry(geo)
        self.pivotAxis.setParams({"fade_factor": 0.0})

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
        self.bbox.setGeometry(geo)
        self.bbox.show(1)

    def updatePerim(self):
        rad  = self.state.kParms.p.distanceTo(self.state.kParms.t)
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({
            "divs": 128,
            "type": 1,
            "t": self.state.kParms.p,
            "scale": rad,
            "orient": 2})
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.perim.setParams({
            "color1": hou.Vector4(1.0, 1.0, 1.0, 0.25),
            "fade_factor": 1.0})
        self.perim.setGeometry(geo)
        self.perim.show(1)

    def updatePivot2d(self):
        P = self.state.kParms.p + self.state.kParms.t
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({
            "type": 1,
            "r": self.state.kParms.r,
            "t": P,
            "scale": self.state.kParms.ow * 0.0075})
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.pivot2d.setParams({
            "color1": hou.Vector4(0.0, 0.0, 1, 1),
            "fade_factor": 1.0})
        self.pivot2d.setGeometry(geo)
        self.pivot2d.show(1)

    def updatePivot3d(self):
            verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
            verb.setParms({
                "type": 1,
                "t": self.state.kParms.p,
                "scale": self.self.state.kParms.t.distanceTo(self.state.kParms.p) * 0.002})
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.pivot3d.setGeometry(geo)
            self.pivot3d.show(1)

    def updateRay(self):
            geo = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
            pt_arr = geo.createPoints((self.state.kParms.p, self.state.kParms.t))
            poly = geo.createPolygon()
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
            self.ray.setGeometry(geo)
            self.ray.show(1)

    def updateText(self):
        return


class KHud():
    def __init__(self, state):
        self.state = state
        self.template = {
            "title": "test",
            "rows": [
                {"id": "layout", "type": "plain", "label": "Layout", "value": "Single", "key": "Ctrl + L"},
                {"id": "layout_g", "type": "choicegraph", "count": 8},
                {"id": "viewport", "type": "plain", "label": "Viewport", "value": "0", "key": "Ctrl + V"},
                {"id": "viewport_g", "type": "choicegraph", "count": 4},
                {"id": "view", "type": "plain", "label": "View", "value": "Perspective", "key": "V"},
                {"id": "view_g", "type": "choicegraph", "count": 8},
                {"id": "target", "type": "plain", "label": "Target", "value": "Camera", "key": "T"},
                {"id": "target_g", "type": "choicegraph", "count": 2},
                {"id": "vis", "type": "plain", "label": "Vis"},
                {"id": "focus", "type": "plain", "label": "Focus", "value": 0},
                {"id": "focus_g", "type": "choicegraph", "count": 10}
            ]
        }

    def update(self):
        if self.state.kSceneViewer.layout() == hou.geometryViewportLayout.DoubleSide: self.template["rows"][3]["count"] = 2
        elif self.state.kSceneViewer.layout() == hou.geometryViewportLayout.DoubleStack: self.template["rows"][3]["count"] = 2
        elif self.state.kSceneViewer.layout() == hou.geometryViewportLayout.Quad: self.template["rows"][3]["count"] = 4
        elif self.state.kSceneViewer.layout() == hou.geometryViewportLayout.QuadBottomSplit: self.template["rows"][3]["count"] = 4
        elif self.state.kSceneViewer.layout() == hou.geometryViewportLayout.QuadLeftSplit: self.template["rows"][3]["count"] = 4
        elif self.state.kSceneViewer.layout() == hou.geometryViewportLayout.TripleBottomSplit: self.template["rows"][3]["count"] = 3
        elif self.state.kSceneViewer.layout() == hou.geometryViewportLayout.TripleLeftSplit: self.template["rows"][3]["count"] = 3
        elif self.state.kSceneViewer.layout() == hou.geometryViewportLayout.Single: self.template["rows"][3]["count"] = 1
        self.state.sceneViewer.hudInfo(template=self.template)
        updates = {
            "layout": str(self.state.kSceneViewer.layout())[23:],
            "layout_g": self.state.kSceneViewer.layouts().index(self.state.kSceneViewer.layout())
        }
        self.state.sceneViewer.hudInfo(hud_values=updates)


class KParms():
    def __init__(self, state):
        self.state = state
        self.parms = state.kwargs["state_parms"]
        # Hidden vars
        self.local_x = hou.Vector3(0, 0, 0)
        self.local_y = hou.Vector3(0, 0, 0)
        self.local_z = hou.Vector3(0, 0, 0)
        self.global_x = hou.Vector3(0, 0, 0)
        self.global_y = hou.Vector3(0, 0, 0)
        self.global_z = hou.Vector3(0, 0, 0)
        # Parameters
        self._p = hou.Vector3(0, 0, 0)
        self._r = hou.Vector3(0, 0, 0)
        self._t = hou.Vector3(0, 0, 0)
        self._dist = 0
        self._ow = 0
        self._target = None
        self._delta_r = 0
        self._delta_t = 0
        self._delta_z = 0
        self._layout = None
        self._viewport = None
        # Guides
        self.guide_axis_size = 1
        self.guide_cam_axis = 1
        self.guide_pivot_axis = 0
        self.guide_bbox = 0
        self.guide_cam_geo = 0
        self.guide_perim = 0
        self.guide_pivot2d = 0
        self.guide_pivot3d = 1
        self.guide_ray = 0
        self.guide_tie_axis_to_radius = 0

    def reset(self):
        self._t = hou.Vector3(0, 0, 0)
        self._r = hou.Vector3(0, 0, 0)
        self._p = hou.Vector3(0, 0, 0)
        self._z = 10
        self._ow = 10
        self._delta_t = 1
        self._delta_r = 15
        self._delta_z = 1
        self.local_x = hou.Vector3(1, 0, 0)
        self.local_y = hou.Vector3(0, 1, 0)
        self.local_z = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)

    @property
    def p(self): return self._p
    @p.setter
    def p(self, val):
        self._p = val
        self.parms["p"]["value"] = val
        self.state.kCam.cam.parmTuple("p").set(val)

    @property
    def r(self): return self._r
    @r.setter
    def r(self, val):
        self._r = val
        self.parms["r"]["value"] = list(val)
        self.state.kCam.cam.parmTuple("r").set(val)
        self.state.kGuides.update()

    @property
    def t(self): return self._t
    @t.setter
    def t(self, val):
        self._t = val
        self.parms["t"]["value"] = list(val)
        self.state.kCam.cam.parmTuple("t").set(val)

    @property
    def z(self): return self._z
    @z.setter
    def z(self, val):
        self._z= val
        self.parms["z"]["value"] = val
        self.state.kCam.setZoom(10)

    @property
    def dist(self): return self._dist

    @property
    def ow(self): return self._ow
    @ow.setter
    def ow(self, val):
        self._ow = val
        self.parms["ow"]["value"] = val
        self.state.kCam.cam.parm("orthowidth").set(val)

    @property
    def target(self): return self._target
    @target.setter
    def target(self, val):
        self._target = val
        self.parms["target"]["value"] = val

    @property
    def delta_r(self): return self._delta_r
    @delta_r.setter
    def delta_r(self, val):
        self._delta_r = val
        self.parms["delta_r"]["value"] = val

    @property
    def delta_t(self): return self._delta_t
    @delta_t.setter
    def delta_t(self, val):
        self._delta_t = val
        self.parms["delta_t"]["value"] = val

    @property
    def delta_z(self): return self._delta_z
    @delta_z.setter
    def delta_z(self, val):
        self._delta_z = val
        self.parms["delta_z"]["value"] = val

    @property
    def layout(self): return self._layout
    @layout.setter
    def layout(self, val):
        self._layout = val
        self.parms["layout"]["value"] = val
        self.state.kSceneViewer.setLayout(self.state.kSceneViewer.layouts()[val])

    @property
    def viewport(self): return self._viewport
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
# Layout/viewport IDs
#
# DoubleSide:        2 3
#
# DoubleStack:       3
#                    0
#
# Quad:              2 3
#                    1 0
#
# QuadBottomSplit:     3
#                    2 1 0
#
# QuadLeftSplit:     2
#                    1 3
#                    0
#
# TripleBottomSplit:   3
#                    1   0
#
# TripleLeftSplit:   2
#                    0 3
#                    1
#
# Single:
# setViewportLayout(layout, single=-1)
# -1: current viewport (viewportmouse is/was over)
# 0: top-left quad viewport (default: Top)
# 1: top-right quad viewport (default: Perspective)
# 2: bottom-left quad viewport (default: Front)
# 3: bottom-right quad viewport (default: Right)

    def __init__(self, state):
        self.state = state
        self.sceneViewer = state.sceneViewer

    def layout(self):
        return self.sceneViewer.viewportLayout()

    def layouts(self):
        return (
            hou.geometryViewportLayout.DoubleSide,
            hou.geometryViewportLayout.DoubleStack,
            hou.geometryViewportLayout.Quad,
            hou.geometryViewportLayout.QuadBottomSplit,
            hou.geometryViewportLayout.QuadLeftSplit,
            hou.geometryViewportLayout.TripleBottomSplit,
            hou.geometryViewportLayout.TripleLeftSplit,
            hou.geometryViewportLayout.Single)

    def layoutIndices(self):
        return (
            (2,3),
            (3,0),
            (2,3,1,0),
            (3,2,1,0),
            (2,1,0,3),
            (3,1,0),
            (2,3,1),
            (3))

    def nextLayout(self):
        index = self.layouts().index(self.layout())
        new_index = (index + 1) % len(self.layouts())
        self.setLayout(self.layouts()[new_index])
        self.state.kHud.update()
        return

    def nextView(self):
        return

    def nextViewport(self):
        return

    def setLayout(self, layout):
        print(layout)
        self.sceneViewer.setViewportLayout(layout)

    def viewport(self):
        return self.sceneViewer.curViewport()

    def viewports(self):
        return self.sceneViewer.viewports()

    def setType(self, viewportType):
        viewport = self.sceneViewer.findViewport(self.layout_state["viewport"])
        viewport.changeType(viewportType)


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
