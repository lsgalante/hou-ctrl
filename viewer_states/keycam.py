import hou
# import hctl_utils as hcu # pyright: ignore

class State(object):

    HUD_TEMPLATE={
        "title": "test",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},

            # Layout
            {"id": "divider", "type":  "divider"},
            {"id": "layout", "label": "layout"},
            {"id": "layout_g", "type": "choicegraph"},
            {"id": "viewport_index", "label": "viewport_index"},
            {"id": "viewport_index_g", "type": "choicegraph"},
            {"id": "set_view", "label": "set_view"},
            {"id": "set_view_g", "type": "choicegraph"},

            # Movement
            {"id": "divider0", "type": "divider"},
            {"id": "target", "label": "target"},
            {"id": "target_g", "type": "choicegraph"},

            # Delta
            {"id": "divider1", "type": "divider"},
            {"id": "r", "label": "r_delta"},
            {"id": "t", "label": "t_delta"},
            {"id": "dist", "label": "dist_delta"},
            {"id": "ow", "label": "ow_delta"},

            # Vis
            {"id": "divider2", "type": "divider"},
            {"id": "vis", "label": "vis"},

            # Focus
            {"id": "divider3", "type": "divider"},
            # {"id": "attr", "label": "attr", "value": "partition"},
            {"id": "focus", "label": "focus", "value": 0},
            {"id": "focus_g", "type":  "choicegraph", "count": 10}
        ]
    }

    def __init__(self, state_name, scene_viewer):

        # General Variables #

        self.cam_type = None
        self.context = None
        self.modes = ("camera", "settings")
        self.mode = "camera"
        self.sceneViewer = scene_viewer
        self.state_name = state_name
        self.viewports = None
        self.viewport_index = None

        # Camera Variables #

        self.T_pvt = hou.Vector3(0, 0, 0)
        self.T_cam = hou.Vector3(0, 0, 0)
        self.r = hou.Vector3(0, 0, 0)
        self.local_x = hou.Vector3(1, 0, 0)
        self.local_y = hou.Vector3(0, 1, 0)
        self.local_z = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)

        # State dictionaries #

        self.guide_states={
            "axisSize": 1,
            "axisCam": 1,
            "axisPivot": 0,
            "bbox": 0,
            "camGeo": 1,
            "perim": 0,
            "pivot2d": 0,
            "pivot3d": 1,
            "ray": 1,
            "tie_axis_to_radius": 0
        }

        self.options={
            "center_on_geo": 1,
            "lock_cam": 1,
            "cam_reset": 1
        }

        self.units={
            "r": 7.5,
            "t": 1,
            "ow": 1,
            "dist": 1
        }

        ##############
        # HUD States #
        ##############

        self.hud_state={
            "controls": ("layout", "viewport_index", "set_view", "target", "r", "t", "ow", "dist", "vis", "focus"),
            "control": "layout",

            # layouts: DoubleSide, DoubleStack, Quad, QuadBottomSplit, QuadLeftSplit, Single, TripleBottomSplit, TripleLeftSplit
            "layouts": ("Single", "DoubleSide", "TripleLeftSplit", "Quad"),
            "layout": "Single",

            "viewport_indexs": ("0"),
            "viewport_index": "0",

            "set_views": ("top", "bottom", "left", "right", "front", "back", "persp", "none"),
            "set_view": "persp",

            "targets": ("cam", "pivot"),
            "target": "cam",

            "r": self.units["r"],
            "t": self.units["t"],
            "ow": self.units["ow"],
            "dist": self.units["dist"],

            "vis_arr": ("test1", "test2", "test3"),
            "vis": "test1",

            "focuss": ("test1", "test2", "test3"),
            "focus": "test1"
        }


    #############
    # Listeners #
    #############

    def onDraw(self, kwargs):
        handle = kwargs["draw_handle"]
        self.guideAxisCam.draw(handle, {})
        self.guideAxisPivot.draw(handle, {})
        self.guidePerim.draw(handle, {})
        self.guidePivot2d.draw(handle, {})
        self.guidePivot3d.draw(handle, {})
        self.guideRay.draw(handle, {})
        # self.guideText.draw(handle, {})


    def onExit(self, kwargs):
        for viewport in self.viewports:
            viewport.lockCameraToView(False)


    def onGenerate(self, kwargs):
        kwargs["state_flags"]["exit_on_node_select"] = False # Prevent exiting the state when current node changes
        self.kwargs = kwargs
        self.hudSwitch()
        self.viewportLayoutUpdate()
        self.camInit()
        self.parmInit()
        self.networkContextUpdate()
        self.hudUpdate()
        self.optionUpdate()
        self.camFrame()
        self.guideCreate()


    def onKeyEvent(self, kwargs):
        key = kwargs["ui_event"].device().keyString()
        self.camAspectRatioUpdate()
        self.camFrame()
        functions = ()
        keys = ()

        # HUD
        if self.mode == "settings":
            keys = (
                "m",      # cycle mode
                "h", "l"  # prev/next option
                "k", "j", # prev/next control
            )
            functions = (
                self.hudModeCycle,
                self.hudOptionPrev, self.hudOptionNext,
                self.hudControlPrev, self.hudControlNext
            )
            args = [None] * len(functions)
            index = keys.index(key)

        # Camera
        elif self.mode == "camera":
            keys = (
                "m", "o", # Cycle mode/projection
                "h", "l", # rotate about y axis neg/pos
                "k", "j", # rotate about x axis neg/pos
                "shift+h", "shift+l", # translate on x axis
                "shift+k", "shift+j", # translate on y axis
                "-", "=", # zoom in/out
                "shift+-", "shift+=", # special zoom in/out
                "f" # frame
            )
            index = keys.index(key)
            print(self.cam_type)

            if self.cam_type == "node":
                functions = (
                    self.hudModeCycle, self.camProjectionCycle,
                    self.camR, self.camR,
                    self.camR, self.camR,
                    self.camT, self.camT,
                    self.camT, self.camT
                )
                args = (
                    None, None,
                    (hou.Vector3(1, 0, 0), -15), (hou.Vector3(1, 0, 0), 15),
                    (hou.Vector3(0, 1, 0), -15), (hou.Vector3(0, 1, 0), 15),
                    hou.Vector3(0, 1, 0), hou.Vector3(0, -1, 0),
                    hou.Vector3(-1, 0, 0), hou.Vector3(1, 0, -1)
                )

                self.stateToCam()

            elif self.cam_type == "default":
                cam = self.viewport.defaultCamera()
                t = list(cam.translation())
                delta = self.units["t"]

                # Perspective/Orthographic projection
                if self.viewport.type() == hou.geometryViewportType.Perspective:
                    functions = (
                        self.camT, self.camT,
                        self.camT, self.camT,
                        self.camR, self.camR,
                        self.camR, self.camR,
                        self.camZoom, self.camZoom)
                    args = (
                        (hou.Vector3(1, 0, 0), -1), (hou.Vector3(0, 1, 0), -1),
                        (hou.Vector3(0, 1, 0), 15), (hou.Vector3(0, -1, 0), 15),
                        (hou.Vector3(-1, 0, 0), 15), (hou.Vector3(1, 0, -1), 15),
                        (hou.Vector3(0, 0, 1), 15), (hou.Vector3(0, 0, -1), 15),
                        (hou.Vector3(0, 0, 1), 15), (hou.Vector3(0, 0, -1), 15),
                    )

                # Linear projection
                else:
                    indices = [0, 0]
                    if self.viewport.type() == hou.geometryViewportType.Top: indices = [0, 1]
                    elif self.viewport.type() == hou.geometryViewportType.Bottom: indices = [2, 0]
                    elif self.viewport.type() == hou.geometryViewportType.Front: indices = [0, 1]
                    elif self.viewport.type() == hou.geometryViewportType.Back: indices = [1, 0]
                    elif self.viewport.type() == hou.geometryViewportType.Right: indices = [0, 1]
                    elif self.viewport.type() == hou.geometryViewportType.Left: indices = [1, 2]

                    functions = (
                        self.hudModeCycle, self.defaultCamProjectionCycle,
                        self.defaultcamR, self.defaultcamR,
                        self.defaultcamR, self.defaultcamR,
                        self.defaultcamT, self.defaultcamT,
                        self.defaultcamT, self.defaultcamT,
                        cam.setOrthoWidth(cam.orthoWidth() - 1),
                        cam.setOrthoWidth(cam.orthoWidth() + 1)
                    )
                    args = (
                        None, None,
                        (hou.Vector3(1, 0, 0), -15),
                        (hou.Vector3(1, 0, 0), 15),
                        (hou.Vector3(0, 1, 0), -15), (hou.Vector3(0, 1, 0), 15),
                        hou.Vector3(0, 1, 0), hou.Vector3(0, -1, 0),
                        hou.Vector3(-1, 0, 0), hou.Vector3(1, 0, -1)
                    )

                cam.setTranslation(t)

            if index != -1:
                functions[index](args[index])
                return True

        else:
            return False


    def onMenuAction(self, kwargs):
        item = kwargs["menu_item"]
        if item == "camFrame":        self.camFrame()
        elif item == "camReset":      self.camReset()
        elif item == "viewportFrame": self.viewportFrame()
        elif item == "axis_cam":      self.guide_states["axisCam"] = kwargs["axis_cam"]
        elif item == "axis_pivot":    self.guide_states["axisPivot"] = kwargs["axis_pivot"]
        elif item == "perim":         self.guide_states["perim"] = kwargs["perim"]
        elif item == "pivot_2d":      self.guide_states["pivot2d"] = kwargs["pivot_2d"]
        elif item == "pivot_3d":      self.guide_states["pivot3d"] = kwargs["pivot_3d"]
        elif item == "ray":           self.guide_states["ray"] = kwargs["ray"]
        self.guideUpdate()


    def onParmChangeEvent(self, kwargs):
        self.guideUpdate()
        self.stateToCam()


    ###################
    # Array Traversal #
    ###################

    def arrNext(self, arr, cur):
        index = arr.index(cur)
        index = (index + 1) % len(arr)
        return index


    def arrPrev(self, arr, cur):
        index = arr.index(cur)
        index = (index - 1) % len(arr)
        return index


    ##########
    # Camera #
    ##########

    def camAspectRatioUpdate(self):
        self.cam.parm("resx").set(1000)
        self.cam.parm("resy").set(1000)
        viewport = self.sceneViewer.findViewport("persp1")
        ratio = viewport.size()[2] / viewport.size()[3]
        self.cam.parm("aspect").set(ratio)


    def camFrame(self):
        centroid = self.geoCentroidGet()
        self.T_pvt = centroid
        self.T_cam = centroid
        self.ow = 10
        self.camZoom(6)
        self.stateToCam()


    def camInit(self):
        self.viewports = list( self.sceneViewer.viewports() )
        self.viewports.reverse() # I guess they get listed backward
        self.viewport = self.viewports[0]

        # Create keycam node if nonexistant
        children = hou.node("/obj").children()
        children_names = [ node.name() for node in children ]
        if "keycam" not in children_names:
            cam = hou.node("/obj").createNode("cam")
            cam.setName("keycam")
            cam.parm("xOrd").set(0)
        cam = self.viewport.camera()

        self.cam = hou.node("/obj/keycam")
        self.viewport.setCamera(self.cam)
        self.viewport.lockCameraToView(self.options["lock_cam"])

    def camMovePivot(self):
        # state_parms = self.kwargs["state_parms"]
        target = self.nav_state["target"]
        # if target == "cam": t = list(state_parms["t"]["value"])
        # elif target == "centroid": centroid = self.geoCentroidGet()
        if target == "origin":
            dist = self.parm_state["dist"]["value"]
            self.t = [0, 0, dist]
            self.r = hou.Vector3(45, 45, 0)
            self.p = [0, 0, -dist]
            self.pr = [0, 0, 0]
            self.ow = 10
        elif target == "ray":
            return
        self.stateToCam()
        self.updateGuides()


    def camProjectionCycle(self):
        cam = self.cam
        projParm = cam.parm("projection")
        proj = projParm.evalAsString()
        if proj == "ortho": projParm.set("perspective")
        elif proj == "perspective": projParm.set("ortho")


    def camToState(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")


    def camReset(self):
        self.T_cam = hou.Vector3(0, 0, 0)
        self.T_pvt = hou.Vector3(0, 0, 0)
        self.r = hou.Vector3(0, 0, 0)
        self.local_x = hou.Vector3(1, 0, 0)
        self.local_y = hou.Vector3(0, 1, 0)
        self.local_z = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)
        self.stateToCam()


    def camR(self, axis_name, deg):
        axis = None
        if axis_name == "x": axis = self.local_x; self.r[0] += deg
        elif axis_name == "y": axis = self.global_y; self.r[1] += deg
        m = hou.hmath.buildRotateAboutAxis(axis, deg)
        self.T_cam -= self.T_pvt
        self.T_cam *= m
        self.T_cam += self.T_pvt
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m
        self.stateToCam()


    def camT(self, axis_name, amt):
        axis = None
        if axis_name == "x": axis = self.local_x
        elif axis_name == "y": axis = self.local_y
        move = axis * amt
        self.T_pvt += move
        self.T_cam += move
        self.stateToCam()


    def camZoom(self, amt):
        move = self.local_z * amt
        self.T_cam += move
        self.stateToCam()


    ###############
    # Default Cam #
    ###############

    def defaultCamFrame(self):
        viewports = self.sceneViewer.viewports()
        for viewport in viewports:
            cam = viewport.camera()
            # Is cam default or node.
            if cam == None:
                viewport.frameAll()
        self.camToState()


    ############
    # Geometry #
    ############

    def geoBboxGet(self):
        geo = self.geoGet()
        bbox = geo.boundingBox()
        return bbox


    def geoCentroidGet(self):
        geo_in = self.geoGet()
        geo_out = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(geo_out, [geo_in])
        pt = geo_out.point(0)
        centroid = pt.position()
        return centroid


    def geoGet(self):
        self.displayNode = None
        pwd = self.sceneViewer.pwd()
        self.context = pwd.childTypeCategory().label()

        if self.context == "dop": displayNode = pwd.displayNode()
        elif self.context == "lop": return None
        elif self.context == "Objects": displayNode = pwd.children()[0].displayNode()
        elif self.context == "Geometry": displayNode = pwd.displayNode()
        return displayNode.geometry()


    def geoHome(self):
        self.displayNode = None
        pwd = self.sceneViewer.pwd()
        self.context = pwd.childTypeCategory().label()
        # print(self.context)


    #########
    # Guide #
    #########

    def guideCreate(self):

        if not hasattr(self, "guideAxisCam"):
            self.guideAxisCam = hou.GeometryDrawable(
                scene_viewer=self.sceneViewer,
                geo_type=hou.drawableGeometryType.Line,
                name="axisCam")
        if not hasattr(self, "guideAxisPivot"):
            self.guideAxisPivot = hou.GeometryDrawable(
                scene_viewer=self.sceneViewer,
                geo_type=hou.drawableGeometryType.Line,
                name="axisPivot",
                params={"color1": hou.Vector4((1, 1, 1, 0.5))})
        if not hasattr(self, "guideBbox"):
            self.guideBbox = hou.GeometryDrawable(
                scene_viewer=self.sceneViewer,
                geo_type=hou.drawableGeometryType.Line,
                name="bbox",
                params={"color1": hou.Vector4((1, 1, 1, 0.3))})
        if not hasattr(self, "guidePerim"):
            self.guidePerim = hou.GeometryDrawable(
                scene_viewer=self.sceneViewer,
                geo_type=hou.drawableGeometryType.Line,
                name="perim")
        if not hasattr(self, "guidePivot2d"):
            self.guidePivot2d = hou.GeometryDrawable(
                scene_viewer=self.sceneViewer,
                geo_type=hou.drawableGeometryType.Line,
                name="pivot2d")
        if not hasattr(self, "guidePivot3d"):
            self.guidePivot3d = hou.GeometryDrawable(
                scene_viewer=self.sceneViewer,
                geo_type=hou.drawableGeometryType.Face,
                name="pivot3d")
            self.guidePivot3d.setParams({
                "color1": hou.Vector4(0.8, 0.8, 0.4, 0.7),
                "fade_factor": 0.5})
        if not hasattr(self, "ray"):
            self.guideRay = hou.GeometryDrawable(
                scene_viewer=self.sceneViewer,
                geo_type=hou.drawableGeometryType.Line,
                name="ray",
                params={"color1": hou.Vector4((1, 0.8, 1, 0.5))})


    def guideToggle(self, kwargs, guide):
        kwargs[guide] = not kwargs[guide]
        self.update_bbox()


    def guideUpdate(self):
        if self.guide_states["axisCam"]: self.guideAxisCamUpdate()
        else: self.guideAxisCam.show(0)

        if self.guide_states["axisPivot"]: self.guideAxisPivotUpdate()
        else: self.guideAxisPivot.show(0)

        if self.guide_states["bbox"]: self.guideBboxUpdate()
        else: self.guideBbox.show(0)

        if self.guide_states["perim"]: self.guidePerimUpdate()
        else: self.guidePerim.show(0)

        if self.guide_states["pivot2d"]: self.guidePivot2dUpdate()
        else: self.guidePivot2d.show(0)

        if self.guide_states["pivot3d"]: self.guidePivot3dUpdate()
        else: self.guidePivot3d.show(0)

        if self.guide_states["ray"]: self.guideRayUpdate()
        else: self.guideRay.show(0)

        # if self.guide_states["text"]:
        #     self.guideTextUpdate()
        # if not guideText:
        #     self.guideText = hou.TextDrawable(
        #         scene_viewer=self.sceneViewer,
        #         name="text",
        #         label="test")


    def guideAxisCamUpdate(self):
        axes = (self.local_x, self.local_y, self.local_z)
        geo = hou.Geometry()
        for i in range(3):
            P0 = axes[i] * 1 + self.T_cam
            P1 = axes[i] * -1 + self.T_cam
            pt_arr = geo.createPoints((P0, P1))
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
        self.guideAxisCam.setGeometry(geo)
        self.guideAxisCam.show(1)


    def guideAxisPivotUpdate(self):
        T_pvt = hou.Vector3(self.T_pvt)
        axes = (hou.Vector3(1, 0, 0), hou.Vector3(0, 1, 0), hou.Vector3(0, 0, 1))
        colors = ([1.0, 0.7, 0.7], [0.7, 1.0, 0.7], [0.7, 0.7, 1.0])
        geo = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, "Cd", (0.1, 0.1, 0.1))

        for i in range(3):
            P0 = axes[i] *  1 + T_pvt
            P1 = axes[i] * -1 + T_pvt
            pt_arr = geo.createPoints((P0, P1))
            pt_arr[0].setAttribValue("Cd", colors[i])
            pt_arr[1].setAttribValue("Cd", colors[i])
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
        self.guideAxisPivot.setGeometry(geo)
        self.guideAxisPivot.setParams({"fade_factor": 0.0})
        self.guideAxisPivot.show(1)


    def guideBboxUpdate(self):
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
        self.guideBbox.setGeometry(geo)
        self.guideBbox.show(1)


    def guidePerimUpdate(self):
        rad  = self.T_pvt.distanceTo(self.T_cam)
        self.log(str(rad) + "x")
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({
            "divs": 128,
            "type": 1,
            "t": self.T_pvt,
            #"r": self.r,
            "scale": rad,
            "orient": 2 })
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.guide_perim.setParams({
            "color1": hou.Vector4(1.0, 1.0, 1.0, 0.25),
            "fade_factor": 1.0 })
        self.guidePerim.setGeometry(geo)
        self.guidePerim.show(1)


    def guidePivot2dUpdate(self):
        r = list(self.r)
        t = list(self.t)
        p = list(self.p)
        ow = self.ow
        P = hou.Vector3(p) + hou.Vector3(t)
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({
            "type": 1,
            "r": r,
            "t": P,
            "scale": ow * 0.0075 })
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.guide_pivot_2d.setParams({
            "color1":  hou.Vector4(0.0, 0.0, 1, 1),
            "fade_factor": 1.0 })
        self.guidePivot2d.setGeometry(geo)
        self.guidePivot2d.show(1)


    def guidePivot3dUpdate(self):
            verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
            verb.setParms({
                "type": 1,
                "t": self.T_pvt,
                "scale": self.T_cam.distanceTo(self.T_pvt) * 0.002 })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guidePivot3d.setGeometry(geo)
            self.guidePivot3d.show(1)


    def guideRayUpdate (self):
            T_pvt = self.T_pvt
            T_cam = self.T_cam
            geo = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
            pt_arr = geo.createPoints((T_pvt, T_cam))
            poly = geo.createPolygon()
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
            self.guideRay.setGeometry(geo)
            self.guideRay.show(1)


    def guideTextUpdate (self):
        return


    #################
    # HUD Functions #
    #################

    def hudControlNext(self):
        self.hude_state["huds"] = self.hud_names
        self.hud_state["hud"] = self.hud_name
        controls = self.hud_state["controls"]
        control = self.hud_state["control"]
        control_index = controls.index(control)
        control_index += 1
        control_index %= len(controls)
        new_control = controls[control_index]
        self.hud_state["control"] = new_control
        self.hud_name = self.hud_state["hud"]
        self.hudUpdate()


    def hudControlPrev(self):
        self.hud_state["huds"] = self.hud_names
        self.hud_state["hud"] = self.hud_name
        controls = self.hud_state["controls"]
        control = self.hud_state["control"]
        control_index = controls.index(control)
        control_index -= 1
        control_index %= len(controls)
        new_control = controls[control_index]
        self.hud_state["control"] = new_control
        self.hud_name = self.hud_state["hud"]
        self.hudUpdate()


    def hudGraphUpdate(self):
        # Calculate the number of bars in a graph based on the length of the appropriate array
        for i, row in enumerate(self.HUD_TEMPLATE["rows"]):
            # If row ID indicates it is a graph
            if row["id"][-2:] == "_g":
                arr = None
                # Count the number of items in the array
                if row["id"] == "hud_g":
                    arr = self.hud_names
                else:
                    arr = self.hud_state[row["id"][0:-2] + "s"]
                # Set the number of bars in the graph.
                self.HUD_TEMPLATE["rows"][i]["count"] = len(arr)


    def hudModeCycle(self):
        index = self.arrNext(self.modes, self.mode)
        self.mode = self.modes[index]
        self.hudUpdate()


    def hudOptionNext(self):
        control = self.hud_state["control"]
        values = self.hud_state[control + "s"]
        value = self.hud_state[control]
        index = values.index(value)
        if control == "attr":
            self.setFocusAttr()
        else:
            index += 1
            index %= len(values)
            new_value = values[index]
            self.hud_state[control] = new_value
        # Extra handling
        if control == "layout": self.viewportLayoutSet()
        elif control == "viewport_index": self.viewportFocus()
        elif control == "set_view": self.setView()
        self.hudUpdate()


    def hudOptionPrev(self):
        control = self.hud_state["control"]
        values = self.hud_state[control + "s"]
        value = self.hud_state[control]
        index = values.index(value)
        if control == "attr":
            self.setFocusAttr()
        else:
            index -= 1
            index %= len(values)
            new_value = values[index]
            self.hud_state[control] = new_value
        # Extra handling
        if control == "layout": self.viewportLayoutSet()
        elif control == "viewport_index": self.viewportFocus()
        elif control == "set_view": self.setView()
        self.hudUpdate()


    def hudUpdate(self):
        # Update graph bar count
        self.hudGraphUpdate()

        # Find the new update values.
        updates = {}

        for row in self.HUD_TEMPLATE["rows"]:
            # Skip processing dividers.
            if "divider" not in row["id"]:

                # First three are common to all huds.
                if row["id"] == "mode": updates["mode"] = {"value": self.mode}
                elif row["id"] == "hud": updates["hud"] = {"value": self.hud_name}
                elif row["id"] == "hud_g": updates["hud_g"] = {"value": self.hud_names.index(self.hud_name)}

                # Graph
                elif row["id"][-2:] == "_g":
                    control_name = row["id"][0:-2]
                    control_value = self.hud_state[control_name]
                    control_values = self.hud_state[control_name + "s"]

                    updates[row["id"]] = {"value": control_values.index(control_value)}

                # Other
                else:
                    control_name = row["id"]
                    control_value = self.hud_state[control_name]
                    updates[row["id"]] = {"value": control_value}

        # Add selection indicator in setting mode
        if self.mode == "settings":
            updates[self.hud_state["control"]]["value"] = "[" + updates[self.hud_state["control"]]["value"] + "]"

        # Apply
        self.sceneViewer.hudInfo(hud_values=updates)


    ##################
    # Init Functions #
    ##################

    def optionUpdate(self):
        # Reset cam, or else set state from cam.
        if self.options["cam_reset"]:
            self.camReset()
        else:
            self.camToState()
        # keycam node display flag.
        self.cam.setDisplayFlag(self.guide_states["camGeo"])


    def setView(self):
        set_view = self.hud_state["set_view"]
        r = None
        if set_view == "top":     r = (270, 0, 0)
        elif set_view == "bottom":r = (90, 0, 0)
        elif set_view == "front": r = (0, 180, 0)
        elif set_view == "back":  r = (0, 0, 0)
        elif set_view == "right": r = (0, 90, 0)
        elif set_view == "left":  r = (0, 270, 0)
        self.r = hou.Vector3(r)
        self.stateToCam()


    def setFocusAttr(self):
        attr = hou.ui.readInput(
            "focus_attr",
            buttons=("OK", "Cancel"),
            initial_contents=self.hud_state_focus["focus_attr"])
        if attr[0] == 0:
            self.focus_state["focus_attr"] = attr[1]


    ###########
    # Network #
    ###########

    def networkContextUpdate(self):
        node = self.sceneViewer.pwd()
        self.context = node.type().name()


    ##############
    # Parameters #
    ##############

    def parmInit(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")


    def stateToCam(self):
        self.cam.parmTuple("t").set(self.T_cam)
        self.cam.parmTuple("r").set(self.r)
        self.cam.parm("orthowidth").set(self.ow)


    ############
    # Viewport #
    ############

    # Guide to layout/viewport IDs:
    #
    # DoubleSide:
    # 2 3
    #
    # DoubleStack:
    # 3
    # 0
    #
    # Quad:
    # 2 3
    # 1 0
    #
    # QuadBottomSplit:
    #   3
    # 2 1 0
    #
    # QuadLeftSplit:
    # 2
    # 1 3
    # 0
    #
    # Single:
    # setViewportLayout(layout, single=-1)
    # -1: current viewport (viewportmouse is/was over)
    # 0: top-left viewport from quad layout (default Top)
    # 1: top-right viewport from quad layout (default Perspective)
    # 2: bottom-left viewport from quad layout (default Front)
    # 3: bottom-right viewport from quad layout (default Right)
    #
    # TripleBottomSplit:
    #   3
    # 1   0
    #
    # TripleLeftSplit:
    # 2
    # 0 3
    # 1

    def viewportLayoutUpdate(self):
        self.viewport = self.sceneViewer.curViewport()
        self.viewports = self.sceneViewer.viewports()
        self.layout = self.sceneViewer.viewportLayout()

        if self.layout == hou.geometryViewportLayout.DoubleSide: self.viewport_index = (2, 3)[self.viewport_index]
        elif self.layout == hou.geometryViewportLayout.DoubleStack: self.viewport_index = (3, 0)[self.viewport_index]
        elif self.layout == hou.geometryViewportLayout.Quad: self.viewport_index = (2, 3, 1, 0)[self.viewport_index]
        elif self.layout == hou.geometryViewportLayout.QuadBottomSplit: self.viewport_index = (3, 2, 1, 0)[self.viewport_index]
        elif self.layout == hou.geometryViewportLayout.QuadLeftSplit: self.viewport_index = (2, 1, 0, 3)[self.viewport_index]
        elif self.layout == hou.geometryViewportLayout.Single: self.viewport_index = 3
        elif self.layout == hou.geometryViewportLayout.TripleBottomSplit: self.viewport_index = (3, 1, 0)[self.viewport_index]
        elif self.layout == hou.geometryViewportLayout.TripleLeftSplit: self.viewport_index = (2, 3, 1)[self.viewport_index]

        self.viewport = self.viewports[self.viewport_index]
        self.viewportType = self.viewport.type()


    def viewportFocus(self):
        return


    def viewportFrame(self):
        for viewport in self.viewports:
            cam = viewport.camera()
            # Is camera node or default.
            if cam == None: viewport.frameAll()
            else: viewport.frameAll()
        self.camToState()


    def viewportSwap(self):
        # viewport_names = [viewport.name() for viewport in self.viewports]
        self.viewports = self.viewports[1:] + [self.viewports[0]]
        # viewportTypes = viewportTypes[1:] + [viewportTypes[0]]

        for i, viewport in enumerate(self.viewports):
            viewport.changeName("v" * i)
        for i, viewport in enumerate(self.viewports):
            viewport.changeName(self.viewports[i])
            # viewport.changeType(viewportTypes[i])


    def viewportGet(self):
        viewport_indexs = self.layout_state["viewport_indexs"]
        viewport_index = self.layout_state["viewport_index"]
        viewport_index = viewport_indexs.index(viewport_index)
        viewports = list(self.sceneViewer.viewports())
        viewports.reverse()
        viewport = viewports[viewport_index]
        return viewport


    def viewportLayoutSet(self):
        layout = self.hud_state["layout"]
        self.sceneViewer.setViewportLayout(getattr(hou.geometryViewportLayout, layout))

        viewport_ct = 0
        if layout == "DoubleSide": viewport_ct = 2
        elif layout == "DoubleStack": viewport_ct = 2
        elif layout == "Quad": viewport_ct = 4
        elif layout == "QuadBottomSplit": viewport_ct = 4
        elif layout == "QuadLeftSplit": viewport_ct = 4
        elif layout == "Single": viewport_ct = 1
        elif layout == "TripleBottomSplit": viewport_ct = 3
        elif layout == "TripleLeftSplit": viewport_ct = 3

        viewport_indexs = []
        for i in range(viewport_ct):
            viewport_indexs.append(str(i))

        self.hud_state["viewport_indexs"] = viewport_indexs
        self.hud_state["viewport_index"] = viewport_indexs[0]

    def viewportTypeSet(self, viewportType):
        viewport = self.sceneViewer.findViewport(self.layout_state["viewport_index"])
        viewport.changeType(viewportType)


def createViewerStateTemplate():
    # Define template
    template = hou.ViewerStateTemplate(
        type_name="keycam",
        label="keycam",
        category=hou.sopNodeTypeCategory(),
        contexts=[hou.objNodeTypeCategory()])
    # Bind factory
    template.bindFactory(State)
    # Bind icon
    template.bindIcon("DESKTOP_application_sierra")
    # Bind parameters
    template.bindParameter(hou.parmTemplateType.Menu, name="mode", label="Mode", default_value="nav", menu_items=[("nav", "Nav"), ("settings", "Settings")])
    template.bindParameter(hou.parmTemplateType.Menu, name="hud", label="HUD", default_value="layout", menu_items=[("layout", "Layout"), ("movement", "Movement"), ("delta", "Delta"), ("vis", "Vis"), ("focus", "Focus")])
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Menu, name="layout", label="Layout", default_value="layout", menu_items=[("single", "Single"), ("doubleside", "DoubleSide"), ("tripleleftsplit", "TripleLeftSplit"), ("quad", "Quad")])
    template.bindParameter(hou.parmTemplateType.Int, name="viewport_index", label="Viewport Index", default_value=0, min_limit=0, max_limit=3)
    template.bindParameter(hou.parmTemplateType.Menu, name="view", label="View", default_value="perspective", menu_items=[("perspective", "Perspective"), ("top", "Top"), ("front", "Front"), ("side", "Side")])
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Menu, name="target", label="Target", default_value="cam", menu_items=[("cam", "Cam"), ("pivot", "Pivot")])
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Float, name="rot_amt", label="Rotation Amount", default_value=7.5, min_limit=-180.0, max_limit=180.0)
    template.bindParameter(hou.parmTemplateType.Float, name="tr_amt", label="Translation Amount", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="ow_amt", label="Ortho Width Amount", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="zoom_amt", label="Zoom Amount", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Separator)
    # Bind menu
    menu = makeMenu()
    template.bindMenu(menu)
    return template


def makeMenu():
    menu = hou.ViewerStateMenu("keycamMenu", "keycamMenu")
    # Action items
    menu.addActionItem("camFrame", "camFrame")
    menu.addActionItem("camReset", "camReset")
    menu.addActionItem("viewportFrame", "viewportFrame")
    # Toggle items
    menu.addToggleItem("axis_cam", "axis_cam", 1)
    menu.addToggleItem("axis_pivot", "axis_pivot", 1)
    menu.addToggleItem("perim", "perim", 1)
    menu.addToggleItem("pivot_2d", "pivot_2d", 0)
    menu.addToggleItem("pivot_3d", "pivot_3d", 1)
    menu.addToggleItem("ray", "ray", 1)
    return menu
