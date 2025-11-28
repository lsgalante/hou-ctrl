import hou
from hclib import HCCam, HCGeo, HCSceneViewer


def createViewerStateTemplate():
    # Define template
    template = hou.ViewerStateTemplate(type_name="keycam", label="keycam",
        category=hou.objNodeTypeCategory(), contexts=[hou.sopNodeTypeCategory()])
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
    template.bindParameter(hou.parmTemplateType.Menu, name="camera", label="Camera", default_value="keycam",
        menu_items=[("keycam", "Keycam"), ("default", "Default"), ("other", "Other")], toolbox=False)
    template.bindParameter(hou.parmTemplateType.Menu, name="target", label="Target", default_value="cam",
        menu_items=[("cam", "Camera"), ("pivot", "Pivot")], toolbox=False)
    template.bindParameter(hou.parmTemplateType.Separator, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="t", label="Translation", num_components=3,
        toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="r", label="Rotation", num_components=3,
        toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="p", label="Pivot", num_components=3,
        toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="zoom", label="Zoom", num_components=1,
        toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="ow", label="Ortho Width", num_components=1,
        toolbox=False)
    template.bindParameter(hou.parmTemplateType.Separator, toolbox=False)
    template.bindParameter(hou.parmTemplateType.Float, name="deltat", label="Delta T", default_value=1.0,
        min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="deltar", label="Delta R", default_value=15.0,
        min_limit=-180.0, max_limit=180.0)
    template.bindParameter(hou.parmTemplateType.Float, name="deltazoom", label="Delta Zoom", default_value=10.0,
        min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="deltaow", label="Delta OW", default_value=1.0,
        min_limit=0, max_limit=10.0)

    # Context menu
    menu = hou.ViewerStateMenu("keycam_menu", "Keycam Menu")
    menu.addActionItem("frame", "Frame")
    menu.addActionItem("reset", "Reset")
    setViewMenu = hou.ViewerStateMenu("set_view_menu", "Set View")
    setViewMenu.addActionItem("top", "Top")
    setViewMenu.addActionItem("bottom", "Bottom")
    setViewMenu.addActionItem("front", "Front")
    setViewMenu.addActionItem("back", "Back")
    setViewMenu.addActionItem("left", "Left")
    setViewMenu.addActionItem("right", "Right")
    menu.addMenu(setViewMenu)
    guideMenu = hou.ViewerStateMenu("guide_menu", "Guides")
    guideMenu.addToggleItem("bbox", "Bbox", 1)
    guideMenu.addToggleItem("cam_axis", "Camera Axis", 1)
    guideMenu.addToggleItem("pivot_axis", "Pivot Axis", 1)
    guideMenu.addToggleItem("perim", "Perimeter", 0)
    guideMenu.addToggleItem("pivot2d", "2D Pivot", 1)
    guideMenu.addToggleItem("pivot3d", "3D Pivot", 0)
    guideMenu.addToggleItem("ray", "Ray", 0)
    menu.addMenu(guideMenu)
    menu.addSeparator()
    template.bindMenu(menu)

    # Ok
    return template


class State(object):
    def __init__(self, state_name, scene_viewer):
        # Put options first
        self.options = {
            "center_on_geo": 1,
            "lock_cam": 1,
            "reset": 1,
            "show_bbox": 1,
            "show_perim": 0,
            "show_pivot2d": 0,
            "show_pivot3d": 1,
            "show_pivot_axis": 1,
            "show_ray": 0,
        }

        self.viewer = scene_viewer
        self.state_name = state_name
        self.cam_type = None
        self.context = None
        self.kwargs = None

        # Check for cam node
        if not hou.node("/obj/keycam"):
            cam = hou.node("/obj").createNode("cam")
            cam.setName("keycam")
            cam.parm("xOrd").set(0)
        self.cam = hou.node("/obj/keycam")
        self.hccam = HCCam(cam, self.viewer)
        # self.hcdefaultcam = HCDefaultCam(self, defaultcam)
        self.hcgeo = None
        self.guides = None
        self.hud = None
        self.parms = None
        self.hcviewer = None

    def onDraw(self, kwargs):
        self.guides.draw(kwargs)

    def onExit(self, kwargs):
        for viewport in self.viewer.viewports():
            viewport.lockCameraToView(False)

    def onGenerate(self, kwargs):
        # Prevent exiting the state when current node changes
        kwargs["state_flags"]["exit_on_node_select"] = False
        self.kwargs = kwargs
        self.hcgeo = HCGeo(self.viewer)
        self.guides = Guides(self)
        self.parms = Parms(self)
        self.hcviewer = HCSceneViewer(self.viewer)
        self.hud = Hud(self)
        self.parms.reset()
        self.hud.update()
        self.updateNetworkContext()
        self.updateOptions()
        self.guides.update()
        self.hccam.fitAspectRatio()
        # self.hccam.frame()

    def onKeyEvent(self, kwargs):
        self.hccam.fitAspectRatio()
        # Node cam
        # functions with args
        keymap1 = {
            "-": lambda: self.hccam.zoom("out"),
            "=": lambda: self.hccam.zoom("in"),
            "o": lambda: self.hccam.nextProjection(),
            "h": lambda: self.hccam.rotate("left"),
            "j": lambda: self.hccam.rotate("down"),
            "k": lambda: self.hccam.rotate("up"),
            "l": lambda: self.hccam.rotate("right"),
            "v": lambda: self.hcviewer.nextView(),
            "Shift+-": lambda: self.hccam.orthoZoom("out"),
            "Shift+=": lambda: self.hccam.orthoZoom("in"),
            "Shift+h": lambda: self.hccam.translate("left"),
            "Shift+j": lambda: self.hccam.translate("down"),
            "Shift+k": lambda: self.hccam.translate("up"),
            "Shift+l": lambda: self.hccam.translate("right"),
            "Ctrl+l": lambda: self.hcviewer.nextLayout(),
            "f": lambda: self.hccam.frame(),
            "c": lambda: self.hccam.center()
        }
        key = kwargs["ui_event"].device().keyString()
        if key in keymap:
            keymap[key]()
            self.guides.update()
            return True
        else:
            return False

        # Default cam
        # if 2 == 1:
        #     default_cam_map = {
        #         "hou.geometryViewportType.Top": (0, 1),
        #         "hou.geometryViewportType.Bottom": (2, 0),
        #         "hou.geometryViewportType.Front": (0, 1),
        #         "hou.geometryViewportType.Back": (1, 0),
        #         "hou.geometryViewportType.Right": (0, 1),
        #         "hou.geometryViewportType.Left": (1, 2),
        #     }
        #     viewport_type = self.hcviewer.viewport().type()
        #     self.indices = default_cam_map[str(viewport_type)]

        #     keymap = {
        #         "-": self.hcdefaultcam.zoomOut,
        #         "+": self.hcdefaultcam.zoomIn,
        #         "h": self.hcdefaultcam.translateLeft,
        #         "j": self.hcdefaultcam.translateDown,
        #         "k": self.hcdefaultcam.translateUp,
        #         "l": self.hcdefaultcam.translateRight,
        #         "v": self.hcdefaultcam.nextView,
        #         "Shift+h": self.hcdefaultcam.rotateLeft,
        #         "Shift+l": self.hcdefaultcam.rotateRight,
        #         "Ctrl+l": self.hcviewer.nextLayout,
        #     }

    def onMenuAction(self, kwargs):
        menumap = {
            "frame": lambda: self.hccam.frame(),
            "reset": lambda: self.parms.reset(),
            "bbox": lambda: self.guides.bbox.show(kwargs["bbox"]),
            "cam_axis": lambda: self.guides.cam_axis.show(kwargs["cam_axis"]),
            "pivot_axis": lambda: self.guides.pivot_axis.show(kwargs["pivot_axis"]),
            "perim": lambda: self.guides.perim.show(kwargs["perm"]),
            "pivot2d": lambda: self.guides.pivot2d.show(kwargs["pivot2d"]),
            "pivot3d": lambda: self.guides.pivot3d.show(kwargs["pivot3d"]),
            "ray": lambda: self.guides.ray.show(kwargs["ray"])
        }

        return functionmap[kwargs["menu_item"]]()

    def onParmChangeEvent(self, kwargs):
        parmmap = {
            "layout": self.parms.layout,
            "viewport": self.parms.viewport,
            # "view": self.parms.view,
            # "camera": self.parms.camera,
            "target": self.parms.target,
            "deltar": self.parms.deltar,
            "deltat": self.parms.deltat,
            "deltazoom": self.parms.deltazoom,
            # "deltaow": self.parms.deltaow,
            "t": self.parms.t,
            "p": self.parms.p,
            "r": self.parms.r,
            "zoom": self.parms.zoom,
            "ow": self.parms.ow,
        }
        parm_name = kwargs["parm_name"]
        parm_value = kwargs["parm_value"]
        parm = parmmap[parm_name]
        parm = parm_value
        return parm
        # self.kGuides.update()

    def setView(self):
        viewmap = {
            "top": hou.Vector3(270, 0, 0),
            "bottom": hou.Vector3(90, 0, 0),
            "front": hou.Vector3(0, 180, 0),
            "back": hou.Vector3(0, 0, 0),
            "right": hou.Vector3(0, 90, 0),
            "left": hou.Vector3(0, 270, 0)
        }
        self.hccam.r = viewmap[self.parms.view]

    # def setFocusAttr(self):
    # attr = hou.ui.readInput(
    #     "focus_attr",
    #     buttons=("OK", "Cancel"),
    #     initial_contents=self.hud_state_focus["focus_attr"],
    # )
    # if attr[0] == 0:
    #     self.focus_state["focus_attr"] = attr[1]

    def updateNetworkContext(self):
        node = self.viewer.pwd()
        self.context = node.type().name()

    def updateOptions(self):
        if self.options["reset"]:
            self.parms.reset()
        # keycam node display flag
        # self.cam.setDisplayFlag(self.guide_states["camGeo"])


class Guides:
    def __init__(self, state):
        self.state = state
        self.cam = state.cam
        self.hccam = state.hccam
        self.viewer = state.viewer
        self.options = {
            "axis_size": 1,
            "tie_axis_to_radius": 0
        }
        self.states = {
            "cam_axis": 1,
            "pivot_axis": 0,
            "bbox": 0,
            "cam": 0,
            "perim": 0,
            "pivot2d": 0,
            "pivot3d": 1,
            "ray": 0
        }
        self.active_states = ()
        self.cam_axis = hou.GeometryDrawable(scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line, name="Camera axis")
        self.pivot_axis = hou.GeometryDrawable(scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line, name="Pivot axis",
            params={"color1": hou.Vector4((1, 1, 1, 0.5))})
        self.bbox = hou.GeometryDrawable(scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line, name="bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3)), "fade_factor": 0.0})
        self.perim = hou.GeometryDrawable(scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line, name="perim")
        self.pivot2d = hou.GeometryDrawable(scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line, name="pivot2d")
        self.pivot3d = hou.GeometryDrawable(scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Face, name="pivot3d")
        self.pivot3d.setParams({"color1": hou.Vector4(0.2, 0.8, 0.2, 0.6), "fade_factor": 0.2})
        self.ray = hou.GeometryDrawable(scene_viewer=self.viewer, geo_type=hou.drawableGeometryType.Line,
            name="ray", params={"color1": hou.Vector4((1, 0.8, 1, 0.5))},)

    def draw(self, kwargs):
        funcmap = {
            "bbox": self.bbox.draw,
            "cam_axis": self.cam_axis.draw,
            "pivot_axis": self.pivot_axis.draw,
            "perim": self.perim.draw,
            "pivot2d": self.pivot2d.draw,
            "pivot3d": self.pivot3d.draw,
            "ray": self.ray.draw
        }
        for name, value in self.states.items():
            if value:
                funcmap[name](kwargs["draw_handle"], {})

    def update(self):
        funcmap = {
            "bbox": self.makeBbox,
            "cam_axis": self.makeCamAxis,
            "pivot_axis": self.makePivotAxis,
            "perim": self.makePerim,
            "pivot2d": self.makePivot2d,
            "pivot3d": self.makePivot3d,
            "ray": self.ray
        }
        for name, value in self.states.items():
            if value:
                funcmap[name]()

    def makeCamAxis(self):
        axes = (self.hccam.localx, self.hccam.localy, self.hccam.localz,)
        geo = hou.Geometry()
        for i in range(3):
            P0 = self.hccam.t + axes[i]
            P1 = self.hccam.t + axes[i] * -1
            pts = geo.createPoints((P0, P1))
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pts[0])
            poly.addVertex(pts[1])
        self.cam_axis.setGeometry(geo)

    def makePivotAxis(self):
        axes = (hou.Vector3(1, 0, 0), hou.Vector3(0, 1, 0), hou.Vector3(0, 0, 1))
        colors = ([1.0, 0.7, 0.7], [0.7, 1.0, 0.7], [0.7, 0.7, 1.0])
        geo = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, "Cd", (0.1, 0.1, 0.1))
        for i in range(3):
            P0 = self.hccam.p + axes[i]
            P1 = self.hccam.p + axes[i] * -1
            pts = geo.createPoints((P0, P1))
            pts[0].setAttribValue("Cd", colors[i])
            pts[1].setAttribValue("Cd", colors[i])
            # poly = geo.createPolygon(is_closed=False)
            # poly.addVertex(pt_arr[0])
            # poly.addVertex(pt_arr[1])
        self.pivot_axis.setGeometry(geo)
        self.pivot_axis.setParams({"fade_factor": 0.0})

    def makeBbox(self):
        geo = self.state.hcgeo.get()
        bbox = geo.boundingBox()
        verb = hou.sopNodeTypeCategory().nodeVerb("box")
        verb.setParms({"size": bbox.sizevec(), "t": bbox.center()})
        bbox_geo = hou.Geometry()
        verb.execute(bbox_geo, [])
        self.bbox.setGeometry(bbox_geo)

    def makePerim(self):
        rad = self.hccam.p.distanceTo(self.hccam.t)
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({"divs": 128, "type": 1, "t": self.hccam.p, "scale": rad, "orient": 2})
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.perim.setParams({"color1": hou.Vector4(1.0, 1.0, 1.0, 0.25), "fade_factor": 1.0})
        self.perim.setGeometry(geo)
        self.perim.show(1)

    def makePivot2d(self):
        r = self.hccam.r
        p = self.hccam.p
        scale = self.hccam.ow * 0.0075
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({"type": 1, "r": r, "t": p, "scale": scale})
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.pivot2d.setParams({"color1": hou.Vector4(0.0, 0.0, 1, 1), "fade_factor": 1.0})
        self.pivot2d.setGeometry(geo)

    def makePivot3d(self):
        verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
        # scale = self.hccam.t.distanceTo(self.hccam.p) * 0.02
        scale = 0.03
        verb.setParms({"freq": 7, "scale": scale, "type": 1, "t": self.hccam.p})
        pivot_geo = hou.Geometry()
        verb.execute(pivot_geo, [])
        self.pivot3d.setGeometry(pivot_geo)

    def makeRay(self):
        geo = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
        pt_arr = geo.createPoints((self.hccam.p, self.hccam.t))
        poly = geo.createPolygon()
        poly.addVertex(pt_arr[0])
        poly.addVertex(pt_arr[1])
        self.ray.setGeometry(geo)


class Hud:
    def __init__(self, state):
        self.state = state
        self.hcviewer = state.hcviewer
        self.viewer = state.viewer
        self.template = {
            "title": "keycam",
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
                {"id": "focus_g", "type": "choicegraph", "count": 10},
            ],
        }

    def update(self):
        layoutmap = {
            "geometryViewportLayout.DoubleSide": 2,
            "geometryViewportLayout.DoubleStack": 2,
            "geometryViewportLayout.Quad": 4,
            "geometryViewportLayout.QuadBottomSplit": 4,
            "geometryViewportLayout.QuadLeftSplit": 4,
            "geometryViewportLayout.TripleBottomSplit": 3,
            "geometryViewportLayout.TripleLeftSplit": 3,
            "geometryViewportLayout.Single": 1,
        }
        layout = self.hcviewer.layout()
        n_viewports = layoutmap[str(layout)]
        self.template["rows"][3]["count"] = n_viewports
        self.viewer.hudInfo(template=self.template)
        updates = {
            "layout": str(self.hcviewer.layout())[23:],
            "layout_g": self.hcviewer.layouts().index(self.hcviewer.layout()),
        }
        self.viewer.hudInfo(hud_values=updates)


class Parms:
    def __init__(self, state):
        self.state = state
        self.viewer = state.viewer
        self.hccam = state.hccam
        self.state_parms = state.kwargs["state_parms"]
        # Parameters
        self.p = hou.Vector3(0, 0, 0)
        self.r = hou.Vector3(0, 0, 0)
        self.t = hou.Vector3(0, 0, 0)
        self.zoom = 0
        self.ow = 0
        self.target = None
        self.deltar = 0
        self.deltat = 0
        self.deltazoom = 0
        self.layout = None
        self.viewport = None

    def update(self):
        self.state_parms["p"] = self.hccam.p
        self.state_parms["r"] = self.hccam.r
        self.state_parms["t"] = self.hccam.t
        self.state_parms["zoom"] = self.hccam.zoom
        self.state_parms["ow"] = self.hccam.ow
        self.state_parms["deltat"] = self.hccam.deltat
        self.state_parms["deltar"] = self.hccam.deltar
        self.state_parms["deltazoom"] = self.hccam.deltazoom

    def reset(self):
        self.parms = self.state.kwargs["state_parms"]
        self.hccam.p = hou.Vector3(0, 0, 0)
        self.hccam.r = hou.Vector3(0, 0, 0)
        self.hccam.t = hou.Vector3(0, 0, 0)
        self.zoom = 10
        self.ow = 10
        self.deltat = 1
        self.deltar = 15
        self.deltazoom = 1

    # @p.setter
    # def p(self, val):
        # self.hccam.p = list(val)

    # @r.setter
    # def r(self, val):
        # self.hccam.r = list(val)

    # @t.setter
    # def t(self, val):
        # self.hccam.t = list(val)

    # @zoom.setter
    # def zoom(self, val):
        # self.hccam.setZoom(10)

    # @ow.setter
    # def ow(self, val):
        # self.hccam.ow = val

    # @target.setter
    # def target(self, val):
        # self.hccam.target = val

    # @deltar.setter
    # def deltar(self, val):
        # self.hccam.deltar = val

    # @deltat.setter
    # def deltat(self, val):
        # self.hccam.deltat = val

    # @deltazoom.setter
    # def deltazoom(self, val):
        # self.hccam.deltazoom = val

    # @layout.setter
    # def layout(self, val):
        # self._layout = val
        # self.state_parms["layout"]["value"] = val
        # self.viewer.setLayout(self.viewer.layouts()[val])

    # @property
    # def viewport(self):
        # return self._viewport

    # @viewport.setter
    # def set_viewport(self, val):
        # self._viewport = val
        # self.state_parms["viewport"]["value"] = val
