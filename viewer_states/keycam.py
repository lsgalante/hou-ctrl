# from sys import version
import hou
# import hctl_utils as hcu # pyright: ignore

class kCam():
    def __init__(self, state):
        self.state = state
        self.params = state.params
        self.kwargs = state.kwargs
        self.parms = state.kwargs["state_parms"]
        self.nodeCheck()
        self.lock()

        self.params.set_t([0, 0, 0])
        self.params.set_r([0, 0, 0])
        self.params.set_p([0, 0, 0])
        self.params.set_orthowidth(10)
        self.params.set_local_x([1, 0, 0])
        self.params.set_local_y([0, 1, 0])
        self.params.set_local_z([0, 0, 1])
        self.params.set_global_x([1, 0, 0])
        self.params.set_global_y([0, 1, 0])
        self.params.set_global_z([0, 0, 1])

    def frame(self):
        centroid = self.state.geo.centroid()
        self.params.set_t(centroid)
        self.params.set_p(centroid)
        # self.params.set_orthowidth(10)
        self.zoomSet(6)
        self.update()

    def home(self):
        centroid = self.state.geo.centroid()
        self.params.set_t(centroid)
        self.params.set_p(centroid)
        # self.params.set_orthowidth(10)
        # self.zoom(6)
        self.update()

    def lock(self):
        self.state.layout.viewport.setCamera(self.cam)
        self.state.layout.viewport.lockCameraToView(1)

    def unlock(self):
        self.state.layout.viewport.lockCameraToView(0)

    def movePivot(self):
        # if origin
        if self.params.target() == 0:
            dist = self.params.dist()
            self.set_t([0, 0, dist])
            self.set_r([45, 45, 0])
            self.set_p([0, 0, -dist])
            self.set_orthowidth(10)
            # self.parms["orthowidth"]["value"] = 10
        self.update()
        self.Guides.update()

    def nextProjection(self):
        projParm = self.cam.parm("projection")
        proj = projParm.evalAsString()
        if proj == "ortho": projParm.set("perspective")
        elif proj == "perspective": projParm.set("ortho")

    def nodeCheck(self):
        # Create keycam node if nonexistant
        children = hou.node("/obj").children()
        children_names = [ node.name() for node in children ]
        if "keycam" not in children_names:
            cam = hou.node("/obj").createNode("cam")
            cam.setName("keycam")
            cam.parm("xOrd").set(0)
        self.cam = hou.node("/obj/keycam")

    def reset(self):
        self.params.set_t(hou.Vector3(0, 0, 0))
        self.params.set_r(hou.Vector3(0, 0, 0))
        self.params.set_local_x(hou.Vector3(1, 0, 0))
        self.params.set_local_y(hou.Vector3(0, 1, 0))
        self.params.set_local_z(hou.Vector3(0, 0, 1))
        self.params.set_global_x(hou.Vector3(1, 0, 0))
        self.params.set_global_y(hou.Vector3(0, 1, 0))
        self.params.set_global_z(hou.Vector3(0, 0, 1))
        self.update()

    def rotateUp(self):
        self.params.set_r([self.params.r()[0] + self.params.delta_r(), self.params.r()[1], self.params.r()[2]])
        m = hou.hmath.buildRotateAboutAxis(self.params.local_x(), self.params.delta_r())
        self.params.set_t(self.params.t() - self.params.p())
        self.params.set_t(self.params.t() * m)
        self.params.set_t(self.params.t() + self.params.p())
        self.params.set_local_x(self.params.local_x() * m)
        self.params.set_local_y(self.params.local_y() * m)
        self.params.set_local_z(self.params.local_z() * m)
        self.update()

    def rotateDown(self):
        self.params.set_r([self.params.r()[0] - self.params.delta_r(), self.params.r()[1], self.params.r()[2]])
        m = hou.hmath.buildRotateAboutAxis(self.params.local_x(), self.params.delta_r() * -1)
        self.params.set_t(self.params.t() - self.params.p())
        self.params.set_t(self.params.t() * m)
        self.params.set_t(self.params.t() + self.params.p())
        self.params.set_local_x(self.params.local_x() * m)
        self.params.set_local_y(self.params.local_y() * m)
        self.params.set_local_z(self.params.local_z() * m)
        self.update()

    def rotateLeft(self):
        self.params.set_r([self.params.r()[0], self.params.r()[1] - self.params.delta_r(), self.params.r()[2]])
        m = hou.hmath.buildRotateAboutAxis(self.params.global_y(), self.params.delta_r() * -1)
        self.params.set_t(self.params.t() - self.params.p())
        self.params.set_t(self.params.t() * m)
        self.params.set_t(self.params.t() + self.params.p())
        self.params.set_local_x(self.params.local_x() * m)
        self.params.set_local_y(self.params.local_y() * m)
        self.params.set_local_z(self.params.local_z() * m)
        self.update()

    def rotateRight(self):
        self.params.set_r([self.params.r()[0], self.params.r()[1] + self.params.delta_r(), self.params.r()[2]])
        m = hou.hmath.buildRotateAboutAxis(self.params.global_y(), self.params.delta_r())
        self.params.set_t(self.params.t() - self.params.p())
        self.params.set_t(self.params.t() * m)
        self.params.set_t(self.params.t() + self.params.p())
        self.params.set_local_x(self.params.local_x() * m)
        self.params.set_local_y(self.params.local_y() * m)
        self.params.set_local_z(self.params.local_z() * m)
        self.update()

    def translateUp(self):
        move = self.params.local_y() * self.params.delta_t() * -1
        self.params.set_t(self.params.t() + move)
        self.update()

    def translateDown(self):
        move = self.params.local_y() * self.params.delta_t()
        self.params.set_t(self.params.t() + move)
        self.update()

    def translateLeft(self):
        move = self.params.local_x() * self.params.delta_t() * -1
        self.params.set_t(self.params.t() + move)
        self.update()

    def translateRight(self):
        move = self.params.local_x() * self.params.delta_t()
        self.params.set_t(self.params.t() + move)
        self.update()

    def update(self):
        self.cam.parmTuple("t").set(list(self.params.t()))
        self.cam.parmTuple("r").set(list(self.parms["r"]["value"]))
        self.cam.parm("orthowidth").set(self.parms["orthowidth"]["value"])

    def updateAspectRatio(self):
        self.cam.parm("resx").set(1000)
        self.cam.parm("resy").set(1000)
        viewport = self.state.scene_viewer.findViewport("persp1")
        ratio = viewport.size()[2] / viewport.size()[3]
        self.cam.parm("aspect").set(ratio)

    def zoomSet(self, zoom):
        move = self.params.local_z() * zoom
        self.params.set_t(self.params.t() + move)
        self.update()

    def zoomIn(self):
        print(self.params.t())
        move = self.params.local_z() * self.params.delta_z() * -1
        self.params.set_t(self.params.t() + move)
        print(self.params.t())
        self.update()

    def zoomOut(self):
        move = self.params.local_z() * self.params.delta_z()
        self.params.set_t(self.params.t() + move)
        self.update()

    def orthoZoomSet(self, zoom):
        self.params.set_orthowidth(zoom)
        self.update()

    def orthoZoomIn(self):
        self.params.set_orthowidth(self.params.orthowidth() + self.params.delta_z() * -1)
        self.update()

    def orthoZoomOut(self):
        self.params.set_orthowidth(self.params.orthowidth() + self.params.delta_z())
        self.update()


class kGeo():
    def __init__(self, state):
        self.state = state
        self.geo = hou.Geometry()
        self.scene_viewer = state.scene_viewer
        self.geo_type = hou.drawableGeometryType.Line
        self.name = "geo"
        self.color = hou.Vector4((1, 1, 1, 0.5))
        self.geo_params = {"color1": self.color}
        self.geo_drawable = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=self.geo_type,
            name=self.name,
            params=self.geo_params
        )

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
        pwd = self.scene_viewer.pwd()
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


class kGuides():
    def __init__(self, state):
        self.state = state
        self.scene_viewer = state.scene_viewer
        self.guides = []
        self.axis_size = 1
        self.axis_cam = 1
        self.axis_pivot = 0
        self.bbox = 0
        self.cam_geo = 1
        self.perim = 0
        self.pivot_2d = 0
        self.pivot_3d = 1
        self.ray = 1
        self.tie_axis_to_radius = 0

        self.AxisCam = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axis_cam"
        )
        self.AxisPivot = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axis_pivot",
            params={"color1": hou.Vector4((1, 1, 1, 0.5))}
        )
        self.Bbox = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))}
        )
        self.Perim = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="perim"
        )
        self.Pivot2d = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="pivot2d"
        )
        self.Pivot3d = hou.GeometryDrawable(
                scene_viewer=self.scene_viewer,
                geo_type=hou.drawableGeometryType.Face,
                name="pivot3d"
        )
        self.Pivot3d.setParams({
            "color1": hou.Vector4(0.8, 0.8, 0.4, 0.7),
            "fade_factor": 0.5}
        )
        self.Ray = hou.GeometryDrawable(
            scene_viewer=self.scene_viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="ray",
            params={"color1": hou.Vector4((1, 0.8, 1, 0.5))}
        )


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


    def updateAxisCam(self):
        axes = (self.params.local_x(), self.params.local_y(), self.params.local_z())
        geo = hou.Geometry()
        for i in range(3):
            P0 = axes[i] * 1 + self.T_cam
            P1 = axes[i] * -1 + self.T_cam
            pt_arr = geo.createPoints((P0, P1))
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
        self.AxisCam.setGeometry(geo)
        self.AxisCam.show(1)


    def updateAxisPivot(self):
        t = self.params.p()
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
        rad  = self.T_pvt.distanceTo(self.T_cam)
        self.log(str(rad) + "x")
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({
            "divs": 128,
            "type": 1,
            "t": self.T_pvt,
            #"r": self.r,
            "scale": rad,
            "orient": 2 }
        )
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.perim.setParams({
            "color1": hou.Vector4(1.0, 1.0, 1.0, 0.25),
            "fade_factor": 1.0 }
        )
        self.Perim.setGeometry(geo)
        self.Perim.show(1)


    def updatePivot2d(self):
        r = self.params.r()
        t = self.params.t()
        p = self.params.p()
        ow = self.params.orthowidth()
        P = hou.Vector3(p) + hou.Vector3(t)
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({
            "type": 1,
            "r": r,
            "t": P,
            "scale": ow * 0.0075 }
        )
        geo = hou.Geometry()
        verb.execute(geo, [])
        self.pivot2d.setParams({
            "color1":  hou.Vector4(0.0, 0.0, 1, 1),
            "fade_factor": 1.0 }
        )
        self.Pivot2d.setGeometry(geo)
        self.Pivot2d.show(1)


    def updatePivot3d(self):
            verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
            verb.setParms({
                "type": 1,
                "t": self.T_pvt,
                "scale": self.T_cam.distanceTo(self.T_pvt) * 0.002 }
            )
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.Pivot3d.setGeometry(geo)
            self.Pivot3d.show(1)


    def updateRay(self):
            T_pvt = self.T_pvt
            T_cam = self.T_cam
            geo = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
            pt_arr = geo.createPoints((T_pvt, T_cam))
            poly = geo.createPolygon()
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
            self.Ray.setGeometry(geo)
            self.Ray.show(1)


    def updateText(self):
        return



class kHud():
    def update(self):
        # Update graph bar count
        self.updateGraph()
        # Find the new update values.
        updates = {}
        for row in self.HUD_TEMPLATE["rows"]:
            # Skip processing dividers.
            if "divider" not in row["id"]:
                if row["id"] == "mode": updates["mode"] = {"value": self.mode}

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
        self.scene_viewer.hudInfo(hud_values=updates)


    def updateGraph(self):
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
        self.updateHud()


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
        self.updateHud()


    def nextMode(self):
        index = self.arrNext(self.modes, self.mode)
        self.mode = self.modes[index]
        self.updateHud()


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
        self.updateHud()



class kLayout():

    def __init__(self, state):
        self.state = state
        self.parms = state.parms
        self.viewports = state.scene_viewer.viewports()
        self.viewports = self.viewports[::-1]
        self.layout = state.scene_viewer.viewportLayout()
        self.update()


    def update(self):
        indices = (0, 0)
        if self.layout == hou.geometryViewportLayout.DoubleSide:
            indices = (2, 3)
        elif self.layout == hou.geometryViewportLayout.DoubleStack:
            indices = (3, 0)
        elif self.layout == hou.geometryViewportLayout.Quad:
            indices = (2, 3, 1, 0)
        elif self.layout == hou.geometryViewportLayout.QuadBottomSplit:
            indices = (3, 2, 1, 0)
        elif self.layout == hou.geometryViewportLayout.QuadLeftSplit:
            indices = (2, 1, 0, 3)
        elif self.layout == hou.geometryViewportLayout.Single:
            indices = (3)
        elif self.layout == hou.geometryViewportLayout.TripleBottomSplit:
            indices = (3, 1, 0)
        elif self.layout == hou.geometryViewportLayout.TripleLeftSplit:
            indices = (2, 3, 1)

        self.viewport = self.viewports[0]
        self.viewportType = self.viewport.type()

    # Guide to layout/viewport IDs:
    # DoubleSide:
    # 2 3
    # DoubleStack:
    # 3
    # 0
    # Quad:
    # 2 3
    # 1 0
    # QuadBottomSplit:
    #   3
    # 2 1 0
    # QuadLeftSplit:
    # 2
    # 1 3
    # 0
    # Single:
    # setViewportLayout(layout, single=-1)
    # -1: current viewport (viewportmouse is/was over)
    # 0: top-left viewport from quad layout (default Top)
    # 1: top-right viewport from quad layout (default Perspective)
    # 2: bottom-left viewport from quad layout (default Front)
    # 3: bottom-right viewport from quad layout (default Right)
    # TripleBottomSplit:
    #   3
    # 1   0
    # TripleLeftSplit:
    # 2
    # 0 3
    # 1


    def viewportFocus(self):
        return


    def viewportFrame(self):
        for viewport in self.viewports:
            cam = viewport.camera()
            # Is camera node or default.
            if cam == None: viewport.frameAll()
            else: viewport.frameAll()
        self.camToState()


    # def viewportSwap(self):
        # viewport_names = [viewport.name() for viewport in self.viewports]
        # self.viewports = self.viewports[1:] + [self.viewports[0]]
        # viewportTypes = viewportTypes[1:] + [viewportTypes[0]]
        # for i, viewport in enumerate(self.viewports):
            # viewport.changeName("v" * i)
        # for i, viewport in enumerate(self.viewports):
            # viewport.changeName(self.viewports[i])
            # viewport.changeType(viewportTypes[i])


    def currentViewport(self):
        viewports = self.params.viewports()
        viewport_index = self.parms.viewport_index()
        viewport = viewports[viewport_index]
        return viewport


    def setLayout(self):
        layout = self.params.layout()
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

    def setType(self, viewportType):
        viewport = self.sceneViewer.findViewport(self.layout_state["viewport_index"])
        viewport.changeType(viewportType)



class kParms():

    def __init__(self, parms):
        self.parms = parms

    def set_p(self, val):
        self.parms["p"]["value"] = val
    def set_r(self, val):
        self.parms["r"]["value"] = val
    def set_t(self, val):
        print(self.parms)
        self.parms["t"]["value"] = val
    #
    def set_dist(self, val):
        self.parms["dist"]["value"] = val
    def set_orthowidth(self, val):
        self.parms["orthowidth"]["value"] = val
    def set_target(self, val):
        self.parms["target"]["value"] = val
    #
    def set_global_x(self, val):
        self.parms["global_x"]["value"] = val
    def set_global_y(self, val):
        self.parms["global_y"]["value"] = val
    def set_global_z(self, val):
        self.parms["global_z"]["value"] = val
    #
    def set_local_x(self, val):
        self.parms["local_x"]["value"] = val
    def set_local_y(self, val):
        self.parms["local_y"]["value"] = val
    def set_local_z(self, val):
        self.parms["local_z"]["value"] = val
    #
    def set_delta_r(self, val):
        self.parms["delta_r"]["value"] = val
    def set_delta_t(self, val):
        self.parms["delta_t"]["value"] = val
    #
    def set_layout(self, val):
        self.parms["layout"]["value"] = val
    def set_viewports(self, val):
        self.parms["viewports"]["value"] = val

    #############

    def p(self):
        return self.parms["p"]["value"]
    def r(self):
        return self.parms["r"]["value"]
    def t(self):
        return self.parms["t"]["value"]
    #
    def dist(self):
        return self.parms["dist"]["value"]
    def orthowidth(self):
        return self.parms["orthowidth"]["value"]
    def target(self):
        return self.parms["target"]["value"]
    #
    def global_x(self):
        return self.parms["global_x"]["value"]
    def global_y(self):
        return self.parms["global_y"]["value"]
    def global_z(self):
        return self.parms["global_z"]["value"]
    #
    def local_x(self):
        return self.parms["local_x"]["value"]
    def local_y(self):
        return self.parms["local_y"]["value"]
    def local_z(self):
        return self.parms["local_z"]["value"]
    #
    def delta_r(self):
        return self.parms["delta_r"]["value"]
    def delta_t(self):
        return self.parms["delta_t"]["value"]
    def delta_z(self):
        return self.parms["delta_z"]["value"]
    #
    def layout(self):
        return self.parms["layout"]["value"]
    def viewport_index(self):
        return self.parms["viewports"]["value"]
    def viewports(self):
        return self.parms["viewports"]["value"]



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
            {"id": "r", "label": "delta_r"},
            {"id": "t", "label": "delta_t"},
            {"id": "dist", "label": "delta_d"},
            {"id": "ow", "label": "delta_ow"},

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
        self.scene_viewer = scene_viewer
        self.state_name = state_name


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
        self.guides.AxisCam.draw(handle, {})
        self.guides.AxisPivot.draw(handle, {})
        self.guides.Perim.draw(handle, {})
        self.guides.Pivot2d.draw(handle, {})
        self.guides.Pivot3d.draw(handle, {})
        self.guides.Ray.draw(handle, {})
        # self.guides.Text.draw(handle, {})


    def onExit(self, kwargs):
        for viewport in self.scene_viewer.viewports():
            viewport.lockCameraToView(False)


    def onGenerate(self, kwargs):
        # Prevent exiting the state when current node changes
        kwargs["state_flags"]["exit_on_node_select"] = False
        self.kwargs = kwargs
        self.params = kParms(kwargs["state_parms"])
        self.parms = kwargs["state_parms"]
        self.layout = kLayout(self)
        self.cam = kCam(self)
        self.geo = kGeo(self)
        self.guides = kGuides(self)
        self.hud = kHud()
        self.updateNetworkContext()
        self.updateOptions()
        self.cam.frame()


    def onKeyEvent(self, kwargs):
        self.cam.updateAspectRatio()

        key = kwargs["ui_event"].device().keyString()
        functions = ()
        keys = ()

        mode = kwargs["state_parms"]["mode"]["value"]
        # mode: 0 = Camera, 1 = Settings

        if mode == 0:
            cam_type = kwargs["state_parms"]["camera"]["value"]
            # cam_type: 0 = Keycam, 1 = Default Perspective, 2 = Default Linear, 3 = Other

            if cam_type == 0:
                if key == "m": self.hud.nextMode(); return True
                elif key == "o": self.cam.nextProjection(); return True
                elif key == "h": self.cam.rotateLeft(); return True
                elif key == "l": self.cam.rotateRight(); return True
                elif key == "k": self.cam.rotateUp(); return True
                elif key == "j": self.cam.rotateDown(); return True
                elif key == "Shift+h": self.cam.translateLeft(); return True
                elif key == "Shift+l": self.cam.translateRight(); return True
                elif key == "Shift+k": self.cam.translateUp(); return True
                elif key == "Shift+j": self.cam.translateDown(); return True
                # elif key == "Shift+-": self.cam.orthoZoomOut(); return True
                # elif key == "Shift+=": self.cam.orthoZoomIn(); return True
                elif key == "Shift+_": self.cam.orthoZoomOut(); return True
                elif key == "Shift++": self.cam.orthoZoomIn(); return True
                elif key == "-": self.cam.zoomOut(); return True
                elif key == "=": self.cam.zoomIn(); return True
                self.cam.update()

            elif cam_type == 1:
                cam = self.viewport.defaultCamera()

                if self.viewport.type() == hou.geometryViewportType.Perspective:
                    if key == "m": self.hud.nextMode(); return True
                    elif key == "o": self.cam.nextProjection(); return True
                    elif key == "h": self.defaultCam.rotateLeft(); return True
                    elif key == "l": self.defaultCam.rotateRight(); return True
                    elif key == "j": self.defaultCam.rotateUp(); return True
                    elif key == "k": self.defaultCam.rotateDown(); return True
                    elif key == "-": self.defaultCam.zoomOut(); return True
                    elif key == "=": self.defaultCam.zoomIn(); return True
                    elif key == "f": self.defaultCam.frame()

            elif cam_type == 2:
                indices = (0, 0)
                if self.viewport.type() == hou.geometryViewportType.Top: indices = (0, 1)
                elif self.viewport.type() == hou.geometryViewportType.Bottom: indices = (2, 0)
                elif self.viewport.type() == hou.geometryViewportType.Front: indices = (0, 1)
                elif self.viewport.type() == hou.geometryViewportType.Back: indices = (1, 0)
                elif self.viewport.type() == hou.geometryViewportType.Right: indices = (0, 1)
                elif self.viewport.type() == hou.geometryViewportType.Left: indices = (1, 2)

                functions = (
                    self.hudModeCycle, self.defaultCamProjectionCycle,
                    self.defaultcamR, self.defaultcamR,
                    self.defaultcamR, self.defaultcamR,
                    self.defaultcamT(indices), self.defaultcamT(indices),
                    self.defaultcamT(indices), self.defaultcamT(indices),
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

            elif cam_type == 3:
                return

                cam.setTranslation(t)

        elif mode == 1:
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
            # args = [None] * len(functions)
            # index = keys.index(key)

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
        self.updateGuides()


    def onParmChangeEvent(self, kwargs):
        # self.updateGuides()
        self.cam.update()
        self.parm = kwargs["parm_name"]
        if self.parm == "mode":
            return
        elif self.parm == "layout":
            return
        elif self.parm == "viewport_index":
            return
        elif self.parm == "view":
            return


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

    def camToState(self):
        self.parms["t"]["value"] = list(self.cam.evalParmTuple("t"))
        self.parms["p"]["value"] = list(self.cam.evalParmTuple("p"))
        self.parms["r"]["value"] = hou.Vector3(self.cam.evalParmTuple("r"))
        self.parms["pr"]["value"] = list(self.cam.evalParmTuple("pr"))
        self.parms["orthowidth"]["value"] = self.cam.evalParm("orthowidth")


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


    def defaultCamUp(self, indices):
        return


    def defaultCamDown(self, indices):
        return


    def defaultCamLeft(self, indices):
        return


    def defaultCamRight(self, indices):
        return


    ##################
    # Init Functions #
    ##################

    def setView(self):
        set_view = self.hud_state["set_view"]
        r = None
        if set_view == "top":     r = (270, 0, 0)
        elif set_view == "bottom":r = (90, 0, 0)
        elif set_view == "front": r = (0, 180, 0)
        elif set_view == "back":  r = (0, 0, 0)
        elif set_view == "right": r = (0, 90, 0)
        elif set_view == "left":  r = (0, 270, 0)
        self.parms["r"]["value"] = list(r)
        self.updateCam()


    def setFocusAttr(self):
        attr = hou.ui.readInput(
            "focus_attr",
            buttons=("OK", "Cancel"),
            initial_contents=self.hud_state_focus["focus_attr"])
        if attr[0] == 0:
            self.focus_state["focus_attr"] = attr[1]


    ##############
    # Parameters #
    ##############

    def parmInit(self):
        self.parms["t"]["value"] = list(self.cam.evalParmTuple("t"))
        self.parms["r"]["value"] = hou.Vector3(self.cam.evalParmTuple("r"))
        self.parms["p"]["value"] = list(self.cam.evalParmTuple("p"))
        self.parms["pr"]["value"] = list(self.cam.evalParmTuple("pr"))
        self.parms["orthowidth"]["value"] = self.cam.evalParm("orthowidth")


    ###########
    # Updates #
    ###########

    def updateNetworkContext(self):
        node = self.scene_viewer.pwd()
        self.context = node.type().name()


    def updateOptions(self):
        # Reset cam, or else set state from cam.
        if self.options["cam_reset"]:
            self.cam.reset()
        else:
            self.camToState()
        # keycam node display flag.
        # self.cam.setDisplayFlag(self.guide_states["camGeo"])


def createViewerStateTemplate():
    # Define template
    template = hou.ViewerStateTemplate(
        type_name="keycam",
        label="keycam",
        category=hou.sopNodeTypeCategory(),
        contexts=[hou.objNodeTypeCategory()]
    )
    # Bind factory
    template.bindFactory(State)
    # Bind icon
    template.bindIcon("DESKTOP_application_sierra")

    # Bind parameters
    template.bindParameter(hou.parmTemplateType.Menu, name="mode", label="Mode", default_value="camera", menu_items=[("camera", "Camera"), ("settings", "Settings")])
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Menu, name="layout", label="Layout", default_value="layout", menu_items=[("single", "Single"), ("doubleside", "DoubleSide"), ("tripleleftsplit", "TripleLeftSplit"), ("quad", "Quad")])
    template.bindParameter(hou.parmTemplateType.Int, name="viewport_index", label="Viewport Index", default_value=0, min_limit=0, max_limit=3)
    template.bindParameter(hou.parmTemplateType.Menu, name="view", label="View", default_value="perspective", menu_items=[("perspective", "Perspective"), ("top", "Top"), ("front", "Front"), ("right", "Right"), ("uv", "UV"), ("bottom", "Bottom"), ("back", "Back"), ("left", "Left")])
    template.bindParameter(hou.parmTemplateType.Menu, name="camera", label="Camera", menu_items=[("keycam", "Keycam"), ("default", "Default"), ("other", "Other")])
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Menu, name="target", label="Target", default_value="cam", menu_items=[("cam", "Cam"), ("pivot", "Pivot")])
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_r", label="Rotation Delta", default_value=7.5, min_limit=-180.0, max_limit=180.0)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_t", label="Translation Delta", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_ow", label="Ortho Width Delta", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Float, name="delta_z", label="Zoom Delta", default_value=1.0, min_limit=0, max_limit=10.0)
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Float, name="t", label="Translation", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="r", label="Rotation", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="p", label="Pivot", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="pr", label="Pivot Rotation", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="orthowidth", label="Ortho Width")
    template.bindParameter(hou.parmTemplateType.Separator)
    template.bindParameter(hou.parmTemplateType.Float, name="local_x", label="Local X", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="local_y", label="Local Y", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="local_z", label="Local Z", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="global_x", label="Global X", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="global_y", label="Global Y", num_components=3)
    template.bindParameter(hou.parmTemplateType.Float, name="global_z", label="Global Z", num_components=3)

    # Bind menu
    template.bindMenu(makeMenu())
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
