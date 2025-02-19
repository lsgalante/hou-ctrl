import hou
import pprint
import time
import viewerstate.utils as su

class State(object):
    HUD_LAYOUT={
        "title": "layout",
        "rows": [
            {"id": "mode",        "label": "mode", "key": "M"},
            {"id": "divider",     "type":  "divider"},
            {"id": "hud",         "label": "hud"},
            {"id": "hud_g",       "type":  "choicegraph"},
            {"id": "layout",      "label": "layout"},
            {"id": "layout_g",    "type":  "choicegraph"},
            {"id": "vp_idx",      "label": "vp_idx"},
            {"id": "vp_idx_g",    "type":  "choicegraph"},
            {"id": "set_view",    "label": "set_view"},
            {"id": "set_view_g",  "type":  "choicegraph"}
        ]
    }

    HUD_MOVEMENT={
        "title": "movement",
        "rows": [
            {"id": "mode",     "label": "mode", "key": "M"},
            {"id": "divider",  "type":  "divider"},
            {"id": "hud",      "label": "hud"},
            {"id": "hud_g",    "type":  "choicegraph"},
            {"id": "target",   "label": "target"},
            {"id": "target_g", "type":  "choicegraph"}
        ]
    }

    HUD_DELTA={
        "title": "delta",
        "rows": [
            {"id": "mode" ,     "label": "mode", "key": "M"},
            {"id": "divider",   "type":  "divider"},
            {"id": "hud",       "label": "hud"},
            {"id": "hud_g",     "type" : "choicegraph"},
            {"id": "r",         "label": "r_delta"},
            {"id": "t",         "label": "t_delta"},
            {"id": "dist",      "label": "dist_delta"},
            {"id": "ow",        "label": "ow_delta"}
        ]
    }

    HUD_VIS={
        "title": "vis",
        "rows": [
            {"id": "mode",    "label": "mode", "key": "M"},
            {"id": "divider", "type":  "divider"},
            {"id": "hud",     "label": "hud"},          
            {"id": "hud_g",   "type":  "choicegraph"},
            {"id": "vis",     "label": "vis"}
        ]
    }

    HUD_FOCUS={
        "title": "focus",
        "rows": [
            {"id": "mode",    "label": "mode",        "key": "M"},
            {"id": "divider", "type":  "divider"},
            {"id": "hud",     "label": "hud"},
            {"id": "hud_g",   "type":  "choicegraph"}, 
            #{"id": "attr",    "label": "attr",        "value": "partition"},
            {"id": "focus",   "label": "focus",       "value": 0},
            {"id": "focus_g", "type":  "choicegraph", "count": 10}
        ]
    }

    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.hud_arr  = ("layout", "movement", "delta", "vis", "focus")
        self.hud      = "layout"
        self.mode_arr = ("camera", "settings")
        self.mode     = "camera"
        self.viewer   = scene_viewer

        self.P_pivot  = hou.Vector3(0, 0, 0)
        self.P_cam    = hou.Vector3(0, 0, 0)
        self.r        = hou.Vector3(0, 0, 0)
        self.local_x  = hou.Vector3(1, 0, 0)
        self.local_y  = hou.Vector3(0, 1, 0)
        self.local_z  = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)
        
        # util dicts
        self.guides={
            "axis_size":          1,
            "axis_cam":           1,
            "axis_pivot":         0,
            "bbox":               0,
            "cam_geo":            1,
            "perim":              0,
            "pivot_2d":           0,
            "pivot_3d":           1,
            "ray":                1,
            "tie_axis_to_radius": 0
        }

        self.startup_dict={
            "center_on_geo": 1,
            "lock_cam":      1,
            "cam_reset":    1
        }

        self.unit_dict={
            "r":    7.5,
            "t":    1,
            "ow":   1,
            "dist": 1
        }

        # hud dicts
        self.layout_dict={
            "ctl_arr":      ("hud", "layout", "vp_idx", "set_view"),
            "ctl":          "hud",
            # layouts: DoubleSide, DoubleStack, Quad, QuadBottomSplit, QuadLeftSplit, Single, TripleBottomSplit, TripleLeftSplit
            "layout_arr":   ("Single", "DoubleSide", "TripleLeftSplit", "Quad"),
            "layout":       "Single",
            "vp_idx_arr":   ("0"),
            "vp_idx":       "0",
            "set_view_arr": ("top", "bottom", "left", "right", "front", "back", "persp", "none"),
            "set_view":     "persp"

        }
    
        self.movement_dict={
            "ctl_arr":    ("hud", "target"),
            "ctl":        "hud",
            "target_arr": ("cam", "pivot"),
            "target":     "cam"
        }

        self.delta_dict={
            "ctl_arr": ("hud", "rot", "tr", "dist", "ow"),
            "ctl":     "hud",
            "r":       self.unit_dict["r"],
            "t":       self.unit_dict["t"],
            "ow":      self.unit_dict["ow"],
            "dist":    self.unit_dict["dist"]
        }

        self.vis_dict={
            "ctl_arr": ("hud"),
            "ctl":     "hud",
            "vis_arr": ("test1", "test2", "test3"),
            "vis":     "test1"
        }

        self.focus_dict={
            "ctl_arr":   ("hud", "attr", "focus"),
            "ctl":       "hud",
            "focus_arr": ("test1", "test2", "test3"),
            "focus":     "test1"
        }
        self.initGuides()
    
    ##
    ##

    def arrNext(self, arr, sel):
        idx = arr.index(sel)
        idx = (idx + 1) % len(arr)
        return idx

    def arrPrev(self, arr, sel):
        idx = arr.index(sel)
        idx = (idx - 1) % len(arr)
        return idx

    def camFrame(self):
        centroid = self.getGeoCentroid()
        bbox = self.getGeoBbox()

        self.P_pivot = centroid
        P_cam = centroid
        #P_cam[2] = 6
        self.P_cam = P_cam
        self.ow = 10

        self.camZoom(6)
        self.stateToCam()

    def camMovePivot(self):
        target = self.nav_dict["target"]
        if target == "cam":
            t = list(self.parms["t"]["value"])
        elif target == "centroid":
            centroid = self.getGeoCentroid()
        elif target == "origin":
            dist    = self.parm_dict["dist"]["value"]
            self.t  = [0, 0, dist]
            self.r  = hou.Vector3(45, 45, 0)
            self.p  = [0, 0, -dist]
            self.pr = [0, 0, 0]
            self.ow = 10
        elif target == "ray":
            return
        self.stateToCam()
        self.updateGuides()

    def camToState(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")

    def camReset(self):
        self.P_cam    = hou.Vector3(0, 0, 0)
        self.P_pivot  = hou.Vector3(0, 0, 0)
        self.r        = hou.Vector3(0, 0, 0)
        self.local_x  = hou.Vector3(1, 0, 0)
        self.local_y  = hou.Vector3(0, 1, 0)
        self.local_z  = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)
        self.stateToCam()
        self.updateGuides()

    def camRotate(self, axis_name, deg):
        axis = None
        if   axis_name == "x":
            axis = self.local_x
            self.r[0] += deg
        elif axis_name == "y":
            axis = self.global_y
            self.r[1] += deg

        m = hou.hmath.buildRotateAboutAxis(axis, deg)

        self.P_cam   -= self.P_pivot
        self.P_cam   *= m
        self.P_cam   += self.P_pivot
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m
        self.stateToCam()

    def camTranslate(self, axis_name, amt):
        axis = None
        if   axis_name == "x": axis = self.local_x
        elif axis_name == "y": axis = self.local_y

        move = axis * amt
        self.P_pivot += move
        self.P_cam += move
        self.stateToCam()

    def camZoom(self, amt):
        move  = hou.Vector3(0, 0, 0)
        move  = self.local_z * amt
        self.P_cam += move
        self.stateToCam()

    def frameDefault(self):
        vp_arr = self.viewer.viewports()
        for vp in vp_arr:
            cam = vp.camera()
            # is cam default or node
            if cam == None: vp.frameAll()
        self.camToState()

    def getGeo(self):
        display_node = self.viewer.pwd().displayNode()
        geo = display_node.geometry()
        return geo

    def getGeoCentroid(self):
        geo_in = self.getGeo()
        geo_out = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(geo_out, [geo_in])
        pt = geo_out.point(0)
        centroid = pt.position()
        return centroid

    def getGeoBbox(self):
        geo = self.getGeo()
        bbox = geo.boundingBox()
        return bbox

    def getVp(self):
        vp_idx_arr = self.layout_dict["vp_idx_arr"]
        vp_idx     = self.layout_dict["vp_idx"]
        vp_idx     = vp_idx_arr.index(vp_idx)
        vp_arr     = list(self.viewer.viewports())
        vp_arr.reverse()
        vp          = vp_arr[vp_idx]
        return vp

    def hudNav(self, key):
        # source common variables
        ctl_dict            = getattr(self, self.hud + "_dict")
        ctl_dict["hud_arr"] = self.hud_arr
        ctl_dict["hud"]     = self.hud
        ctl                 = ctl_dict["ctl"]

        # select control        
        if key in ("j", "k"):
            ctl_arr = ctl_dict["ctl_arr"]
            idx     = ctl_arr.index(ctl)

            if   key == "j": idx += 1
            elif key == "k": idx -= 1

            idx             %= len(ctl_arr)
            ctl             = ctl_arr[idx]
            ctl_dict["ctl"] = ctl

        # change control value
        elif key in ("h", "l"):
            if ctl == "attr": self.setFocusAttr() 

            else:
                val_arr = ctl_dict[ctl + "_arr"] 
                val     = ctl_dict[ctl]
                idx     = val_arr.index(val)

                if   key == "h": idx -= 1
                elif key == "l": idx += 1 

                idx           %= len(val_arr)
                val           = val_arr[idx]
                ctl_dict[ctl] = val

        # update dict 
        if   ctl == "layout":   self.setVpLayout()
        #elif ctl == "vp_idx":   self.set_vp()
        elif ctl == "set_view": self.setView()

        self.hud = ctl_dict["hud"]
        self.updateHud()

    def initCam(self):
        vp_arr = list(self.viewer.viewports())
        vp_arr.reverse()
        vp = vp_arr[0]
        # check if keycam exists. if not, make it
        child_arr = [node.name() for node in hou.node("/obj").children()]
        if "keycam" not in child_arr:
            cam = hou.node("/obj").createNode("cam")
            cam.setName("keycam")
            cam.parm("xOrd").set(0)
        # define vars
        t = [0, 0, 0]
        r = [0, 0, 0]
        p = [0, 0, 0]
        ow = 1
        cam = vp.camera()
        # cam is default
        if cam == None:
            cam = vp.defaultCamera()
            t   = cam.translation()
            r   = cam.rotation()
            p   = cam.pivot()
            ow  = cam.orthoWidth()
        # cam is node
        else:
            t  = cam.evalParmTuple("t")
            r  = cam.evalParmTuple("r")
            p  = cam.evalParmTuple("p")
            ow = cam.evalParm("orthowidth")
        self.cam = hou.node("/obj/keycam")
        vp.setCamera(self.cam)
        vp.lockCameraToView(self.startup_dict["lock_cam"])

    def initGuides(self):
        # axis_cam
        self.guide_axis_cam = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axis_cam")
        # axis_pivot
        self.guide_axis_pivot = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axis_pivot",
            params={"color1": hou.Vector4((1, 1, 1, 0.5))})
        # bbox
        self.guide_bbox = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))})
        # pivot_2d
        self.guide_pivot_2d = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="pivot_2d")
        # perim
        self.guide_perim = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="perim")
        # pivot_3d
        self.guide_pivot_3d = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Face,
            name="pivot_3d")
        self.guide_pivot_3d.setParams({
            "color1": hou.Vector4(0.8, 0.8, 0.4, 0.7),
            "fade_factor": 0.5
        })
        # ray
        self.guide_ray = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="ray",
            params={"color1": hou.Vector4((1, 0.8, 1, 0.5))})
        # text
        self.guide_text = hou.TextDrawable(
            scene_viewer=self.viewer,
            name="text",
            label="test")

    def initParms(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")

    def initSettings(self):
        # reset cam or else set state from cam
        if self.startup_dict["cam_reset"]: self.camReset()
        else: self.camToState()
        # keycam node display flag
        self.cam.setDisplayFlag(self.guides["cam_geo"])

    def setView(self):
        set_view = self.layout_dict["set_view"]
        r = None
        if   set_view == "top":    r = (270, 0, 0)
        elif set_view == "bottom": r = (90, 0, 0)
        elif set_view == "front":  r = (0, 180, 0)
        elif set_view == "back":   r = (0, 0, 0)
        elif set_view == "right":  r = (0, 90, 0)
        elif set_view == "left":   r = (0, 270, 0)
        #self.r = hou.Vector3(r)
        self.stateToCam()

    def setFocusAttr(self):
        attr = hou.ui.readInput(
            "focus_attr",
            buttons=("OK", "Cancel"),
            initial_contents=self.hud_dict_focus["focus_attr"]
        )
        if attr[0] == 0:
            self.focus_dict["focus_attr"] = attr[1]

    def setVpLayout(self):
        layout = self.layout_dict["layout"]
        self.viewer.setViewportLayout(getattr(hou.geometryViewportLayout, layout))

    

        vp_ct = 0
        if   layout == "DoubleSide":        vp_ct = 2
        elif layout == "DoubleStack":       vp_ct = 2
        elif layout == "Quad":              vp_ct = 4
        elif layout == "QuadBottomSplit":   vp_ct = 4
        elif layout == "QuadLeftSplit":     vp_ct = 4
        elif layout == "Single":            vp_ct = 1
        elif layout == "TripleBottomSplit": vp_ct = 3
        elif layout == "TripleLeftSplit":   vp_ct = 3
        vp_idx_arr = []
        for i in range(vp_ct):
            vp_idx_arr.append(str(i))
        self.layout_dict["vp_idx_arr"] = vp_idx_arr
        self.layout_dict["vp_idx"]     = vp_idx_arr[0]
        
    def setVpType(self, vp_type_name):
        vp_type = eval("hou.geometryViewportType." + vp_type_name.capitalize())
        vp = self.viewer.findViewport(self.layout_dict["vp_idx"])
        vp.changeType(vp_type)
    
    def stateToCam(self):
        self.cam.parmTuple("t").set(self.P_cam)
        self.cam.parmTuple("r").set(self.r)
        self.cam.parm("orthowidth").set(self.ow)
        self.updateGuides()

    def toggleBbox(self, kwargs, action):
        enabled = kwargs["toggle_bbx"]
        self.update_bbox()

    def toggleMode(self):
        idx = self.mode_arr.index(self.mode)
        idx = (idx + 1) % 2
        self.mode = self.mode_arr[idx]
        self.updateHud()
        self.updateAspectRatio()

    def toggleProjection(self):
        cam = self.cam
        proj_parm = cam.parm("projection")
        proj = proj_parm.evalAsString() 
        if proj == "ortho": proj_parm.set("perspective")
        elif proj == "perspective": proj_parm.set("ortho")

    def updateAspectRatio(self):
        self.cam.parm("resx").set(1000)
        self.cam.parm("resy").set(1000)
        vp = self.viewer.findViewport("persp1")
        ratio = vp.size()[2] / vp.size()[3]
        self.cam.parm("aspect").set(ratio)

    def updateGuides(self):
        self.updateGuideAxisCam()
        self.updateGuideAxisPvt()
        self.updateGuideBbox()
        self.updateGuidePerim()
        self.updateGuidePvt2d()
        self.updateGuidePvt3d()
        self.updateGuideRay()
        self.updateGuideText()

    def updateGuideAxisCam(self):
        self.guide_axis_cam.show(self.guides["axis_cam"])

        if self.guides["axis_cam"]:
            axes = (self.local_x, self.local_y, self.local_z)
            geo  = hou.Geometry()
            for i in range(3):
                P0 = axes[i] *  1 + self.P_cam
                P1 = axes[i] * -1 + self.P_cam
                pt_arr = geo.createPoints((P0, P1))
                poly   = geo.createPolygon(is_closed=False)
                poly.addVertex(pt_arr[0])
                poly.addVertex(pt_arr[1])
            self.guide_axis_cam.setGeometry(geo)

    def updateGuideAxisPvt(self):
        self.guide_axis_pivot.show(self.guides["axis_pivot"])
        if self.guides["axis_pivot"]:
            P_pivot = hou.Vector3(self.P_pivot)
            axes    = (hou.Vector3(1, 0, 0), hou.Vector3(0, 1, 0), hou.Vector3(0, 0, 1))
            colors  = ([1.0, 0.7, 0.7], [0.7, 1.0, 0.7], [0.7, 0.7, 1.0])
            geo     = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (0.1, 0.1, 0.1))
            for i in range(3):
                P0     = axes[i] *  1 + P_pivot
                P1     = axes[i] * -1 + P_pivot
                pt_arr = geo.createPoints((P0, P1))
                pt_arr[0].setAttribValue("Cd", colors[i])
                pt_arr[1].setAttribValue("Cd", colors[i])
                poly = geo.createPolygon(is_closed=False)
                poly.addVertex(pt_arr[0])
                poly.addVertex(pt_arr[1])
            self.guide_axis_pivot.setGeometry(geo)
            self.guide_axis_pivot.setParams({"fade_factor": 0.0})

    def updateGuideBbox(self):
        self.guide_bbox.show(self.guides["bbox"])
        if self.guides["bbox"]:
            geo  = self.get_get()
            bbox = geo.boundingBox()
            P0   = (bbox[0], bbox[1], bbox[2])
            P1   = (bbox[0], bbox[1], bbox[5])
            P2   = (bbox[3], bbox[1], bbox[5])
            P3   = (bbox[3], bbox[1], bbox[2])
            P4   = (bbox[0], bbox[4], bbox[2])
            P5   = (bbox[0], bbox[4], bbox[5])
            P6   = (bbox[3], bbox[4], bbox[5])
            P7   = (bbox[3], bbox[4], bbox[2])
            print(bbox)
    
    def updateGuidePerim(self):
        self.guide_perim.show(self.guides["perim"])
        if self.guides["perim"]:
            rad  = self.P_pivot.distanceTo(self.P_cam)
            self.log(str(rad) + "x")
            verb = hou.sopNodeTypeCategory().nodeVerb("circle")
            verb.setParms({
                "divs":   128,
                "type":   1,
                "t":      self.P_pivot,
                #"r":      self.r,
                "scale":  rad,
                "orient": 2
            })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guide_perim.setGeometry(geo)
            self.guide_perim.setParams({
                "color1":      hou.Vector4(1.0, 1.0, 1.0, 0.25),
                "fade_factor": 1.0
            })

    def updateGuidePvt2d(self):
        self.guide_pivot_2d.show(self.guides["pivot_2d"])
        if self.guides["pivot_2d"]:
            r    = list(self.r)
            t    = list(self.t)
            p    = list(self.p)
            ow   = self.ow
            P    = hou.Vector3(p) + hou.Vector3(t)
            verb = hou.sopNodeTypeCategory().nodeVerb("circle")
            verb.setParms({
                "type":  1,
                "r":     r,
                "t":     P,
                "scale": ow * 0.0075
            })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guide_pivot_2d.setGeometry(geo)
            self.guide_pivot_2d.setParams({
                "color1":      hou.Vector4(0.0, 0.0, 1, 1),
                "fade_factor": 1.0
            })

    def updateGuidePvt3d(self):
        self.guide_pivot_3d.show(self.guides["pivot_3d"])
        if self.guides["pivot_3d"]:
            verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
            verb.setParms({
                "type":  1,
                "t":     self.P_pivot,
                "scale": self.P_cam.distanceTo(self.P_pivot) * 0.002
            })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guide_pivot_3d.setGeometry(geo)

    def updateGuideText(self):
        return

    def updateGuideRay(self):
        self.guide_ray.show(self.guides["ray"])
        if self.guides["ray"]:
            P_pivot = self.P_pivot
            P_cam = self.P_cam
            geo   = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
            pt_arr = geo.createPoints((P_pivot, P_cam))
            poly   = geo.createPolygon()
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
            self.guide_ray.setGeometry(geo)

    def updateHud(self):
        # update graph counts
        self.updateHudGCt()
        # find and apply to appropriate hud dictionary
        hud_dict = getattr(self, "HUD_" + self.hud.upper())
        self.viewer.hudInfo(template=hud_dict)
        # find new update values
        val_dict    = getattr(self, self.hud + "_dict")
        update_dict = {}
        for row in hud_dict["rows"]:
            if row["id"] != "divider":
                # first three are common to all huds
                if   row["id"] == "mode":  update_dict["mode"]  = {"value": self.mode}
                elif row["id"] == "hud":   update_dict["hud"]   = {"value": self.hud}
                elif row["id"] == "hud_g": update_dict["hud_g"] = {"value": self.hud_arr.index(self.hud)}
                # if it is a graph
                elif row["id"][-2:] == "_g":
                    val_name               = row["id"][0:-2]
                    val                    = val_dict[val_name]
                    val_arr                = val_dict[val_name + "_arr"]
                    update_dict[row["id"]] = {"value": val_arr.index(val)}
                # for other controls
                else:
                    val_name               = row["id"]
                    val                    = val_dict[val_name]
                    update_dict[row["id"]] = {"value": val}
        # add brackets in setting mode
        if self.mode == "settings":
            update_dict[val_dict["ctl"]]["value"] = "[" + update_dict[val_dict["ctl"]]["value"] + "]"
        # apply the updates
        self.viewer.hudInfo(hud_values=update_dict)

    def updateHudGCt(self):
        # calculate number of bars in a graph based on the length of the corresponding array
        hud_name = self.hud
        d        = getattr(self, hud_name + "_dict")
        hud_dict = getattr(self, "HUD_" + hud_name.upper())
        # counter keeps track of the index of the row within the hud
        ct = 0
        for row in hud_dict["rows"]:
            # if row id indicates it is a graph
            if row["id"][-2:] == "_g":
                arr = None
                # count number of items in array
                if row["id"] == "hud_g": arr = self.hud_arr
                else:                    arr = d[row["id"][0:-2] + "_arr"]
                # set the number of bars in the graph
                hud_dict["rows"][ct]["count"] = len(arr)
            ct += 1

    def vpFrame(self):
        for vp in self.viewer.viewports():
            cam = vp.camera()
            # check if camera is default or node
            if cam == None: vp.frameAll()
            else:           vp.frameAll()
        self.camToState()

    def vpSwap(self):
        vp_arr      = self.viewer.viewports()
        vp_name_arr = [vp.name() for vp in vp_arr]
        vp_arr      = vp_arr[1:] + [vp_arr[0]]
        vp_type_arr = vp_type_arr[1:] + [vp_type_arr[0]]
        for i, vp in enumerate(vp_arr):
            vp.changeName("v" * i)
        for i, vp in enumerate(vp_arr):
            vp.changeName(vp_arr[i])
            vp.changeType(vp_type_arr[i])

    # #   #   #   #   #
    #  # # # # # # #  #
    #   #   #   #   # #

    def onDraw(self, kwargs):
        handle = kwargs["draw_handle"]
        self.guide_axis_cam.draw(handle, {})
        self.guide_axis_pivot.draw(handle, {})
        self.guide_perim.draw(handle, {})
        self.guide_pivot_2d.draw(handle, {})
        self.guide_pivot_3d.draw(handle, {})
        self.guide_ray.draw(handle, {})
        self.guide_text.draw(handle, {})

    def onGenerate(self, kwargs):
        # prevent exiting state when selecting nodes
        kwargs["state_flags"]["exit_on_node_select"] = False
        self.parms = kwargs["state_parms"]
        #self.update_dict_layout()
        self.initCam()
        self.initParms()
        self.updateHud()
        self.initSettings()
        self.camFrame()

    def onKeyEvent(self, kwargs):
        key = kwargs["ui_event"].device().keyString()
        self.log(key)
    
        if   key == "m": self.toggleMode()                        # toggle hud mode
        elif key == "o": self.toggleProjection()                   # toggleProjection
        elif self.mode == "settings": self.hudNav(key)            # hudNav
    
        elif self.mode == "camera":                                # camera manipulation
            vp_idx = self.layout_dict["vp_idx"]
            layout = self.layout_dict["layout"]
            if   layout == "DoubleSide":        vp_idx = (2, 3)[int(vp_idx)]
            #   2 3
            elif layout == "DoubleStack":       vp_idx = (3, 0)[int(vp_idx)]
            #   3
            #   0
            elif layout == "Quad":              vp_idx = (2, 3, 1, 0)[int(vp_idx)]
            #   2 3
            #   1 0
            elif layout == "QuadBottomSplit":   vp_idx = (3, 2, 1, 0)[int(vp_idx)]
            #     3
            #   2 1 0
            elif layout == "QuadLeftSplit":     vp_idx = (2, 1, 0, 3)[int(vp_idx)]
            #   2
            #   1 3
            #   0
            elif layout == "Single":            vp_idx = 3
            #   setViewportLayout(layout, single=-1)
            #   -1: current      vp (vp mouse is/was over)
            #   0:  top left     vp from quad layout (default Top)
            #   1:  top-right    vp from quad layout (default Perspective)
            #   2:  bottom-left  vp from quad layout (default Front)
            #   3:  bottom-right vp from quad layout (default Right) 
            elif layout == "TripleBottomSplit": vp_idx = (3, 1, 0)[int(vp_idx)]
            #     3
            #   1   0
            elif layout == "TripleLeftSplit":   vp_idx = (2, 3, 1)[int(vp_idx)]
            #   2
            #   0 3
            #   1
            #

            vps = list(self.viewer.viewports())
            self.log(vp_idx)
            print([vp.type() for vp in vps])
            vp = vps[vp_idx]
            #vp = self.getVp()
            vp_type = vp.type()
            self.log(vp_type)
            
            if vp_type == hou.geometryViewportType.Perspective:    # cam is node
                if   key == "Shift+h": self.camTranslate("x", -1)  # translate x down
                elif key == "Shift+j": self.camTranslate("y", -1)  # translate y down
                elif key == "Shift+k": self.camTranslate("y", 1)   # translate y up
                elif key == "Shift+l": self.camTranslate("x", 1)   # translate x up
                elif key == "h":       self.camRotate("y", -15)    # rotate y down
                elif key == "j":       self.camRotate("x", 15)     # rotate x up
                elif key == "k":       self.camRotate("x", -15)    # rotate x down
                elif key == "l":       self.camRotate("y", 15)     # rotate y up
                elif key == "-":       self.camZoom(1)             # zoom out
                elif key == "=":       self.camZoom(-1)            # zoom in
                elif key == "Shift+-": self.ow += 1                # orthowidth up
                elif key == "Shift+=": self.ow -= 1                # orthowidth down
                elif key == "f":       self.camFrame()            # frame
                self.stateToCam()
                
            else:                                                  # cam is default
                cam = vp.defaultCamera()
                t       = list(cam.translation())
                delta   = self.unit_dict["t"]
                idx_arr = [0, 0]

                if   vp_type == hou.geometryViewportType.Top:    idx_arr = [0, 1]
                elif vp_type == hou.geometryViewportType.Bottom: idx_arr = [2, 0]
                elif vp_type == hou.geometryViewportType.Front:  idx_arr = [0, 1]
                elif vp_type == hou.geometryViewportType.Back:   idx_arr = [1, 0]
                elif vp_type == hou.geometryViewportType.Right:  idx_arr = [0, 1]
                elif vp_type == hou.geometryViewportType.Left:   idx_arr = [1, 2]

                if   key == "h": t[idx_arr[0]] += delta
                elif key == "j": t[idx_arr[1]] += delta
                elif key == "k": t[idx_arr[1]] -= delta
                elif key == "l": t[idx_arr[0]] -= delta
                elif key == "-": cam.setOrthoWidth(cam.orthoWidth() + 1)
                elif key == "=": cam.setOrthoWidth(cam.orthoWidth() - 1)
                cam.setTranslation(t)

        if key in ("m", "o", "h", "j", "k", "l", "-", "=", "Shift+h", "Shift+j", "Shift+k", "Shift+l", "Shift+-", "Shift+=", "f"): return True
        else: return False

    def onMenuAction(self, kwargs):
        item = kwargs["menu_item"]
        if   item == "cam_frame": self.camFrame()
        elif item == "cam_reset": self.camReset()
        elif item == "vp_frame":  self.vpFrame()

        elif item == "axis_cam":  self.guides["axis_cam"]  = kwargs["axis_cam"]
        elif item == "axis_pivot":  self.guides["axis_pivot"]  = kwargs["axis_pivot"]
        elif item == "perim":     self.guides["perim"]     = kwargs["perim"]
        elif item == "pivot_2d":    self.guides["pivot_2d"]    = kwargs["pivot_2d"]
        elif item == "pivot_3d":    self.guides["pivot_3d"]    = kwargs["pivot_3d"]
        elif item == "ray":       self.guides["ray"]       = kwargs["ray"]
        self.updateGuides()

    def onParmChangeEvent(self, kwargs):
        self.updateGuides()
        self.stateToCam()

def createViewerStateTemplate():
    template = hou.ViewerStateTemplate(
        type_name="keycam",
        label="keycam",
        category=hou.sopNodeTypeCategory(),
        contexts=[hou.objNodeTypeCategory()])
    template.bindIcon("DESKTOP_application_sierra")
    template.bindFactory(State)
    menu = makeMenu()
    template.bindMenu(menu)
    return template

def makeMenu():
    menu = hou.ViewerStateMenu("keycam_menu", "keycam_menu")
    menu.addActionItem("cam_frame", "cam_frame")
    menu.addActionItem("cam_reset", "cam_reset") 
    menu.addActionItem("vp_frame",  "vp_frame") 

    menu.addToggleItem("axis_cam",  "axis_cam", 1)
    menu.addToggleItem("axis_pivot",  "axis_pivot", 1)
    menu.addToggleItem("perim",     "perim",    1)
    menu.addToggleItem("pivot_2d",    "pivot_2d",   0)
    menu.addToggleItem("pivot_3d",    "pivot_3d",   1)
    menu.addToggleItem("ray",       "ray",      1)
    return menu
