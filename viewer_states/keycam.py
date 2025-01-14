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
            {"id": "vp_idx",      "label": "vp_idx"},
            {"id": "vp_idx_g",    "type":  "choicegraph"},
            {"id": "set_view",    "label": "set_view"},
            {"id": "set_view_g",  "type":  "choicegraph"},
            {"id": "layout",      "label": "layout"},
            {"id": "layout_g",    "type":  "choicegraph"}
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

        self.P_pvt    = hou.Vector3(0, 0, 0)
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
            "axis_pvt":           1,
            "bbox":               0,
            "cam_geo":            1,
            "perim":              0,
            "pvt_2d":             0,
            "pvt_3d":             1,
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
            "ctl_arr":      ("hud", "vp_idx", "set_view", "layout"),
            "ctl":          "hud",
            "vp_idx_arr":   (),
            "vp_idx":       "0",
            "set_view_arr": ("top", "bottom", "left", "right", "front", "back", "persp", "none"),
            "set_view":     "persp",
            #"layout_arr":   ("DoubleSide", "DoubleStack", "Quad", "QuadBottomSplit", "QuadLeftSplit", "Single", "TripleBottomSplit", "TripleLeftSplit"),
            "layout_arr":   ("Quad", "Single"),
            "layout":       "Single"

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
        self.init_guides()
    
    ##
    ##

    def arr_next(self, arr, sel):
        idx = arr.index(sel)
        idx = (idx + 1) % len(arr)
        return idx

    def arr_prev(self, arr, sel):
        idx = arr.index(sel)
        idx = (idx - 1) % len(arr)
        return idx

    def cam_frame(self):
        centroid = self.get_geo_centroid()
        bbox = self.get_geo_bbox()

        self.P_pvt = centroid
        P_cam = centroid
        #P_cam[2] = 6
        self.P_cam = P_cam
        self.ow = 10

        self.cam_zoom(6)
        self.state_to_cam()

    def cam_move_pivot(self):
        target = self.nav_dict["target"]
        if target == "cam":
            t = list(self.parms["t"]["value"])
        elif target == "centroid":
            centroid = self.get_geo_centroid()
        elif target == "origin":
            dist    = self.parm_dict["dist"]["value"]
            self.t  = [0, 0, dist]
            self.r  = hou.Vector3(45, 45, 0)
            self.p  = [0, 0, -dist]
            self.pr = [0, 0, 0]
            self.ow = 10
        elif target == "ray":
            return
        self.state_to_cam()
        self.update_guides()

    def cam_to_state(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")

    def cam_reset(self):
        self.P_ext    = hou.Vector3(0, 0, 0)
        self.P_pvt    = hou.Vector3(0, 0, 0)
        self.r        = hou.Vector3(0, 0, 0)
        self.local_x  = hou.Vector3(1, 0, 0)
        self.local_y  = hou.Vector3(0, 1, 0)
        self.local_z  = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)
        self.state_to_cam()
        self.update_guides()

    def cam_rotate(self, axis_name, deg):
        axis = None
        if   axis_name == "x":
            axis = self.local_x
            self.r[0] += deg
        elif axis_name == "y":
            axis = self.global_y
            self.r[1] += deg

        m = hou.hmath.buildRotateAboutAxis(axis, deg)

        self.P_cam   -= self.P_pvt
        self.P_cam   *= m
        self.P_cam   += self.P_pvt
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m
        self.state_to_cam()

    def cam_translate(self, axis_name, amt):
        axis = None
        if   axis_name == "x": axis = self.local_x
        elif axis_name == "y": axis = self.local_y

        move = axis * amt
        self.P_pvt += move
        self.P_cam += move
        self.state_to_cam()

    def cam_zoom(self, amt):
        move  = hou.Vector3(0, 0, 0)
        move  = self.local_z * amt
        self.P_cam += move
        self.state_to_cam()

    def frame_default(self):
        vp_arr = self.viewer.viewports()
        for vp in vp_arr:
            cam = vp.camera()
            # is cam default or node
            if cam == None: vp.frameAll()
        self.cam_to_state()

    def get_geo(self):
        display_node = self.viewer.pwd().displayNode()
        geo = display_node.geometry()
        return geo

    def get_geo_centroid(self):
        geo_in = self.get_geo()
        geo_out = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(geo_out, [geo_in])
        pt = geo_out.point(0)
        centroid = pt.position()
        return centroid

    def get_geo_bbox(self):
        geo = self.get_geo()
        bbox = geo.boundingBox()
        return bbox

    def get_vp(self):
        vp_idx_arr = self.layout_dict["vp_idx_arr"]
        vp_idx     = self.layout_dict["vp_idx"]
        vp_idx     = vp_idx_arr.index(vp_idx)
        vp_arr     = list(self.viewer.viewports())
        vp_arr.reverse()
        vp          = vp_arr[vp_idx]
        return vp

    def hud_nav(self, key):
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
            if ctl == "attr": self.set_focus_attr() 

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
        if   ctl == "layout":   self.set_vp_layout()
        #elif ctl == "vp_idx":   self.set_vp()
        elif ctl == "set_view": self.set_view()

        self.hud = ctl_dict["hud"]
        self.update_hud()

    def init_cam(self):
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

    def init_guides(self):
        # axis_cam
        self.guide_axis_cam = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axis_cam")
        # axis_pvt
        self.guide_axis_pvt = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axis_pvt",
            params={"color1": hou.Vector4((1, 1, 1, 0.5))})
        # bbox
        self.guide_bbox = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))})
        # pvt_2d
        self.guide_pvt_2d = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="pvt_2d")
        # perim
        self.guide_perim = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="perim")
        # pvt_3d
        self.guide_pvt_3d = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Face,
            name="pvt_3d")
        self.guide_pvt_3d.setParams({
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

    def init_parms(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")

    def init_settings(self):
        # reset cam or else set state from cam
        if self.startup_dict["cam_reset"]: self.cam_reset()
        else: self.cam_to_state()
        # keycam node display flag
        self.cam.setDisplayFlag(self.guides["cam_geo"])

    def set_view(self):
        set_view = self.layout_dict["set_view"]
        r = None
        if   "top" in set_view: r = (270, 0, 0)
        elif "bot" in set_view: r = (90, 0, 0)
        elif "fro" in set_view: r = (0, 180, 0)
        elif "bac" in set_view: r = (0, 0, 0)
        elif "rig" in set_view: r = (0, 90, 0)
        elif "lef" in set_view: r = (0, 270, 0)
        #self.r = hou.Vector3(r)
        self.state_to_cam()

    def set_focus_attr(self):
        attr = hou.ui.readInput(
            "focus_attr",
            buttons=("OK", "Cancel"),
            initial_contents=self.hud_dict_focus["focus_attr"]
        )
        if attr[0] == 0:
            self.focus_dict["focus_attr"] = attr[1]

    def set_vp_layout(self):
        layout = self.layout_dict["layout"]
        self.viewer.setViewportLayout(getattr(hou.geometryViewportLayout, layout))

    def set_vp_type(self, vp_type_name):
        vp_type = eval("hou.geometryViewportType." + vp_type_name.capitalize())
        vp = self.viewer.findViewport(self.layout_dict["vp_idx"])
        vp.changeType(vp_type)
    
    def state_to_cam(self):
        self.cam.parmTuple("t").set(self.P_cam)
        self.cam.parmTuple("r").set(self.r)
        self.cam.parm("orthowidth").set(self.ow)
        self.update_guides()

    def toggle_bbox(self, kwargs, action):
        enabled = kwargs["toggle_bbx"]
        self.update_bbox()

    def toggle_mode(self):
        idx = self.mode_arr.index(self.mode)
        idx = (idx + 1) % 2
        self.mode = self.mode_arr[idx]
        self.update_hud()
        self.update_aspect_ratio()

    def toggle_projection(self):
        cam = self.cam
        proj_parm = cam.parm("projection")
        proj = proj_parm.evalAsString() 
        if proj == "ortho": proj_parm.set("perspective")
        elif proj == "perspective": proj_parm.set("ortho")

    def update_aspect_ratio(self):
        self.cam.parm("resx").set(1000)
        self.cam.parm("resy").set(1000)
        vp = self.viewer.findViewport("persp1")
        ratio = vp.size()[2] / vp.size()[3]
        self.cam.parm("aspect").set(ratio)

    def update_guides(self):
        self.update_guide_axis_cam()
        self.update_guide_axis_pvt()
        self.update_guide_bbox()
        self.update_guide_perim()
        self.update_guide_pvt_2d()
        self.update_guide_pvt_3d()
        self.update_guide_ray()
        self.update_guide_text()

    def update_guide_axis_cam(self):
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

    def update_guide_axis_pvt(self):
        self.guide_axis_pvt.show(self.guides["axis_pvt"])
        if self.guides["axis_pvt"]:
            P_pvt  = hou.Vector3(self.P_pvt)
            axes   = (hou.Vector3(1, 0, 0), hou.Vector3(0, 1, 0), hou.Vector3(0, 0, 1))
            colors = ([1.0, 0.7, 0.7], [0.7, 1.0, 0.7], [0.7, 0.7, 1.0])
            geo    = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (0.1, 0.1, 0.1))
            for i in range(3):
                P0     = axes[i] *  1 + P_pvt
                P1     = axes[i] * -1 + P_pvt
                pt_arr = geo.createPoints((P0, P1))
                pt_arr[0].setAttribValue("Cd", colors[i])
                pt_arr[1].setAttribValue("Cd", colors[i])
                poly = geo.createPolygon(is_closed=False)
                poly.addVertex(pt_arr[0])
                poly.addVertex(pt_arr[1])
            self.guide_axis_pvt.setGeometry(geo)
            self.guide_axis_pvt.setParams({"fade_factor": 0.0})

    def update_guide_bbox(self):
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
    
    def update_guide_perim(self):
        self.guide_perim.show(self.guides["perim"])
        if self.guides["perim"]:
            rad  = self.P_pvt.distanceTo(self.P_cam)
            self.log(str(rad) + "x")
            verb = hou.sopNodeTypeCategory().nodeVerb("circle")
            verb.setParms({
                "divs":   128,
                "type":   1,
                "t":      self.P_pvt,
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

    def update_guide_pvt_2d(self):
        self.guide_pvt_2d.show(self.guides["pvt_2d"])
        if self.guides["pvt_2d"]:
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
            self.guide_pvt_2d.setGeometry(geo)
            self.guide_pvt_2d.setParams({
                "color1":      hou.Vector4(0.0, 0.0, 1, 1),
                "fade_factor": 1.0
            })

    def update_guide_pvt_3d(self):
        self.guide_pvt_3d.show(self.guides["pvt_3d"])
        if self.guides["pvt_3d"]:
            verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
            verb.setParms({
                "type":  1,
                "t":     self.P_pvt,
                "scale": self.P_cam.distanceTo(self.P_pvt) * 0.002
            })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guide_pvt_3d.setGeometry(geo)

    def update_guide_text(self):
        return

    def update_guide_ray(self):
        self.guide_ray.show(self.guides["ray"])
        if self.guides["ray"]:
            P_pvt = self.P_pvt
            P_cam = self.P_cam
            geo   = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
            pt_arr = geo.createPoints((P_pvt, P_cam))
            poly   = geo.createPolygon()
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
            self.guide_ray.setGeometry(geo)

    def update_hud(self):
        # update graph counts
        self.update_hud_g_ct()
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

    def update_hud_g_ct(self):
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

    def update_dict_layout(self):
        layout = self.viewer.viewportLayout()
        vp_ct = 0
        if   layout == hou.geometryViewportLayout.DoubleSide:        vp_ct = 2
        elif layout == hou.geometryViewportLayout.DoubleStack:       vp_ct = 2
        elif layout == hou.geometryViewportLayout.Quad:              vp_ct = 4
        elif layout == hou.geometryViewportLayout.QuadBottomSplit:   vp_ct = 4
        elif layout == hou.geometryViewportLayout.QuadLeftSplit:     vp_ct = 4
        elif layout == hou.geometryViewportLayout.Single:            vp_ct = 1
        elif layout == hou.geometryViewportLayout.TripleBottomSplit: vp_ct = 3
        elif layout == hou.geometryViewportLayout.TripleLeftSplit:   vp_ct = 3
        vp_idx_arr = []
        for i in range(vp_ct):
            vp_idx_arr.append(str(i))
        self.layout_dict["vp_idx_arr"] = vp_idx_arr
        self.layout_dict["vp_idx"]     = vp_idx_arr[0]
        
    def vp_frame(self):
        for vp in self.viewer.viewports():
            cam = vp.camera()
            # check if camera is default or node
            if cam == None: vp.frameAll()
            else:           vp.frameAll()
        self.cam_to_state()

    def vp_swap(self):
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
        self.guide_axis_pvt.draw(handle, {})
        self.guide_perim.draw(handle, {})
        self.guide_pvt_2d.draw(handle, {})
        self.guide_pvt_3d.draw(handle, {})
        self.guide_ray.draw(handle, {})
        self.guide_text.draw(handle, {})

    def onGenerate(self, kwargs):
        # prevent exiting state when selecting nodes
        kwargs["state_flags"]["exit_on_node_select"] = False
        self.parms = kwargs["state_parms"]
        self.update_dict_layout()
        self.init_cam()
        self.init_parms()
        self.update_hud()
        self.init_settings()
        self.cam_frame()

    def onKeyEvent(self, kwargs):
        key = kwargs["ui_event"].device().keyString()
        self.log(key)

    
        if   key == "m": self.toggle_mode()                        # toggle hud mode
        elif key == "o": self.toggle_projection()                  # toggle_projection
        elif self.mode == "settings": self.hud_nav(key)            # hud_nav
    
        elif self.mode == "camera":                                # camera manipulation
            vp = self.get_vp()
            vp_type = vp.type()
            self.log(vp_type)
            
            if vp_type == hou.geometryViewportType.Perspective:    # cam is node
                if   key == "Shift+h": self.cam_translate("x", -1) # translate x down
                elif key == "Shift+j": self.cam_translate("y", -1) # translate y down
                elif key == "Shift+k": self.cam_translate("y", 1)  # translate y up
                elif key == "Shift+l": self.cam_translate("x", 1)  # translate x up
                elif key == "h":       self.cam_rotate("y", -15)   # rotate y down
                elif key == "j":       self.cam_rotate("x", 15)    # rotate x up
                elif key == "k":       self.cam_rotate("x", -15)   # rotate x down
                elif key == "l":       self.cam_rotate("y", 15)    # rotate y up
                elif key == "-":       self.cam_zoom(1)            # zoom out
                elif key == "=":       self.cam_zoom(-1)           # zoom in
                elif key == "Shift+-": self.ow += 1                # orthowidth up
                elif key == "Shift+=": self.ow -= 1                # orthowidth down
                elif key == "f":       self.cam_frame()            # frame
                self.state_to_cam()
                
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
                cam.setTranslation(t)

        if key in ("m", "o", "h", "j", "k", "l", "-", "=", "Shift+h", "Shift+j", "Shift+k", "Shift+l", "Shift+-", "Shift+=", "f"): return True
        else: return False

    def onMenuAction(self, kwargs):
        item = kwargs["menu_item"]
        if   item == "cam_frame": self.cam_frame()
        elif item == "cam_reset": self.cam_reset()
        elif item == "vp_frame":  self.vp_frame()

        elif item == "axis_cam":  self.guides["axis_cam"]  = kwargs["axis_cam"]
        elif item == "axis_pvt":  self.guides["axis_pvt"]  = kwargs["axis_pvt"]
        elif item == "perim":     self.guides["perim"]     = kwargs["perim"]
        elif item == "pvt_2d":    self.guides["pvt_2d"]    = kwargs["pvt_2d"]
        elif item == "pvt_3d":    self.guides["pvt_3d"]    = kwargs["pvt_3d"]
        elif item == "ray":       self.guides["ray"]       = kwargs["ray"]
        self.update_guides()

    def onParmChangeEvent(self, kwargs):
        self.update_guides()
        self.state_to_cam()

def createViewerStateTemplate():
    template = hou.ViewerStateTemplate(
        type_name="keycam",
        label="keycam",
        category=hou.sopNodeTypeCategory(),
        contexts=[hou.objNodeTypeCategory()])
    template.bindIcon("DESKTOP_application_sierra")
    template.bindFactory(State)
    menu = make_menu()
    template.bindMenu(menu)
    return template

def make_menu():
    menu = hou.ViewerStateMenu("keycam_menu", "keycam_menu")
    menu.addActionItem("cam_frame", "cam_frame")
    menu.addActionItem("cam_reset", "cam_reset") 
    menu.addActionItem("vp_frame",  "vp_frame") 

    menu.addToggleItem("axis_cam",  "axis_cam", 1)
    menu.addToggleItem("axis_pvt",  "axis_pvt", 1)
    menu.addToggleItem("perim",     "perim",    1)
    menu.addToggleItem("pvt_2d",    "pvt_2d",   0)
    menu.addToggleItem("pvt_3d",    "pvt_3d",   1)
    menu.addToggleItem("ray",       "ray",      1)
    return menu
