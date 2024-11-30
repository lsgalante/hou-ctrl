import hou
import pprint
import time
import viewerstate.utils as su

class State(object):
    HUD_LAYOUT={
        "title": "layout",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},
            {"id": "divider", "type": "divider"},
            {"id": "hud", "label": "hud"},
            {"id": "hud_g", "type": "choicegraph"},
            {"id": "main_vp_view", "label": "main_vp_view"},
            {"id": "main_vp_view_g", "type": "choicegraph"},
            {"id": "vp_name", "label": "vp_name"},
            {"id": "vp_name_g", "type": "choicegraph"},
            {"id": "layout", "label": "layout"},
            {"id": "layout_g", "type": "choicegraph"}
        ]
    }

    HUD_MOVEMENT={
        "title": "movement",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},
            {"id": "divider", "type": "divider"},
            {"id": "hud", "label": "hud"},
            {"id": "hud_g", "type": "choicegraph"},
            {"id": "target", "label": "target"},
            {"id": "target_g", "type": "choicegraph"}
        ]
    }

    HUD_DELTA={
        "title": "delta",
        "rows": [
            {"id": "mode" , "label": "mode", "key": "M"},
            {"id": "divider", "type": "divider"},
            {"id": "hud", "label": "hud"},
            {"id": "hud_g", "type" : "choicegraph"},
            {"id": "axis_size", "label": "axis_size"},
            {"id": "rot", "label": "rot_delta"},
            {"id": "tr", "label": "tr_delta"},
            {"id": "dist", "label": "dist_delta"},
            {"id": "ow", "label": "ortho_width_delta"}
        ]
    }

    HUD_VIS={
        "title": "vis",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},
            {"id": "divider", "type": "divider"},
            {"id": "hud", "label": "hud"},          
            {"id": "hud_g", "type": "choicegraph"},
            {"id": "viz", "label": "vis"}
        ]
    }

    HUD_FOCUS={
        "title": "focus",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},
            {"id": "divider", "type": "divider"},
            {"id": "hud", "label": "hud"},
            {"id": "hud_g", "type": "choicegraph"}, 
            {"id": "attr", "label": "attr", "value": "partition"},
            {"id": "focus", "label": "focus", "value": 0},
            {"id": "focus_g", "type": "choicegraph", "count": 10}
        ]
    }

    def __init__(s, state_name, scene_viewer):
        s.state_name = state_name
        s.axes = [1, 1, 1]
        s.hud_arr = ("layout", "movement", "delta", "vis", "focus")
        s.hud = "layout"
        s.init_reset = 1
        s.init_cam_display = 0
        s.mode_arr = ("navigate", "settings")
        s.mode = "navigate"
        s.viewer = scene_viewer
        s.vp_persp  = hou.geometryViewportType.Perspective
        s.vp_top    = hou.geometryViewportType.Top
        s.vp_bottom = hou.geometryViewportType.Bottom
        s.vp_front  = hou.geometryViewportType.Front
        s.vp_back   = hou.geometryViewportType.Back
        s.vp_right  = hou.geometryViewportType.Right
        s.vp_left   = hou.geometryViewportType.Left

        s.hud_dict_layout={
            "ctrl_arr": ("hud", "main_vp_view", "vp_name", "layout"),
            "ctrl": "hud",
            "main_vp_view_arr": ("persp", "top", "bottom", "front", "back", "right", "left"),
            "main_vp_view": "persp",
            "viewport_arr": (),
            "viewport": "",
            "vw_arr": ("persp", "top", "bottom", "front", "back", "right", "left"),
            "layout_arr": ("DoubleSide", "DoubleStack", "Quad", "QuadBottomSplit", "QuadLeftSplit", "Single", "TripleBottomSplit", "TripleLeftSplit"),
            "layout": "Single"
        }
    
        s.hud_dict_movement={
            "ctrl_arr": ("hud", "target"),
            "ctrl": "hud",
            "target_arr": ("cam", "pivot"),
            "target": "cam"
        }

        s.unit_dict={
            "axis_size": 4,
            "rot": 7.5,
            "tr": 1,
            "ow": 1,
            "dist": 1
        }

        s.hud_dict_delta={
            "ctrl_arr": ("hud", "axis_size", "rot", "tr", "dist", "ow"),
            "ctrl": "hud",
            "axis_size": s.unit_dict["axis_size"],
            "rot": s.unit_dict["rot"],
            "tr": s.unit_dict["tr"],
            "ow": s.unit_dict["ow"],
            "dist": s.unit_dict["dist"]
        }

        s.hud_dict_vis={
            "ctrl_arr": ("hud"),
            "ctrl": "hud"
        }

        s.hud_dict_focus={
            "ctrl_arr": ("hud", "attr", "focus"),
            "ctrl": "hud",
            "focus_attr": "partition",
            "focus_idx": 0
        }

        # drawables
        s.drawable_axis = hou.GeometryDrawable(
            scene_viewer=s.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_axis",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))}
        )

        s.drawable_bbox = hou.GeometryDrawable(
            scene_viewer=s.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))}
        )

        s.drawable_pvt = hou.GeometryDrawable(
            scene_viewer=s.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_pvt"
        )

        s.drawable_ray = hou.GeometryDrawable(
            scene_viewer=s.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_ray",
            params={"color1": hou.Vector4((1, 0.8, 1, 0.5))}
        )

        s.drawable_txt = hou.TextDrawable(
            scene_viewer=s.viewer,
            name="drawable_txt",
            label="test")

        s.drawable_axis.show(True)
        s.drawable_bbox.show(False)
        s.drawable_pvt.show(True)
        s.drawable_ray.show(True)
    ##
    ##

    def cam_fit_aspect(s):
        s.v_log("cam_fit_aspect", "func")
        s.cam.parm("resx").set(1000)
        s.cam.parm("resy").set(1000)
        vp = s.viewer.findViewport("persp1")
        ratio = vp.size()[2] / vp.size()[3]
        s.cam.parm("aspect").set(ratio)

    def cam_from_state(s):
        s.v_log("cam_from_state", "func")
        x=1

    def cam_get_dir(s):
        s.v_log("cam_get_dir", "func")
        tru_pvt = s.parms["tru_pvt"]["value"]
        tr = s.parms["tr"]["value"]
        s.v_log(hou.Vector3(tru_pvt) - hou.Vector3(tr), "normal")
        return

    def cam_get_len(s):
        s.v_log("cam_get_len", "func")
        tr = s.parms["tr"]["value"]
        pvt = s.parms["pvt"]["value"]
        len = tr[2]
        return len

    def cam_get_xform(s):
        self.v_log("cam_get_xform", "func")
        r = s.parms["r"]["value"]
        return r

    def cam_init(s):
        s.v_log("cam_init", "func")
        vp = s.vp_get()[0]
        # check if keycam exists and if not, make it
        child_arr = [ node.name() for node in hou.node("/obj").children() ]
        if "keycam" not in child_arr:
            cam = hou.node("/obj").createNode("cam")
            cam.setName("keycam")
        # define vars
        tr = [0, 0, 0]
        rot = [0, 0, 0]
        pvt = [0, 0, 0]
        ow = 1
        # check if cam is default cam
        cam = vp.camera()
        if cam == None:
            cam = vp.defaultCamera()
            tr = cam.translation()
            rot = cam.rotation()
            pvt = cam.pivot()
            ow = cam.orthoWidth()
        else:
            tr = cam.evalParmTuple("t")
            rot = cam.evalParmTuple("r")
            pvt = cam.evalParmTuple("p")
            ow = cam.evalParm("orthowidth")
        s.cam = hou.node("/obj/keycam")
        vp.setCamera(s.cam)
        vp.lockCameraToView(1)

    def cam_move_pvt(s):
        s.v_log("cam_move_pvt", "func")
        target = s.hud_dict_nav["target"]
        if target == "cam":
            tr = s.parms["tr"]["value"]
            s.parms["tru_pvt"]["value"] = list(tr)
        elif target == "centroid":
            centroid = s.geo_get_centroid()
        elif target == "origin":
            dist = s.parms["dist"]["value"]
            s.parms["tr"]["value"] = [0, 0, dist]
            s.parms["rot"]["value"] = [45, 45, 0]
            s.parms["pvt"]["value"] = [0, 0, -dist]
            s.parms["pvt_rot"]["value"] = [0, 0, 0]
            s.parms["tru_pvt"]["value"] = [0, 0, 0]
            s.parms["ow"]["value"] = 10
        elif target == "ray":
            x=1
        s.cam_update()
        s.drawable_update_pvt()
        s.drawable_update_ray()

    def cam_next_proj(s):
        s.v_log("cam_next_proj", "func")
        cam = s.cam
        proj_parm = cam.parm("projection")
        proj = proj_parm.evalAsString() 
        if proj == "ortho": proj_parm.set("perspective")
        elif proj == "perspective": proj_parm.set("ortho")

    def cam_proj_update(s):
        s.v_log("cam_proj_update", "func")
        cam = s.cam
        proj_parm = cam.parm("projection")
        if s.proj == "ortho": proj_parm.set("ortho")
        elif s.proj == "persp": proj_parm.set("perspective")
        s.geo_frame()

    def cam_reset(s):
        s.v_log("cam_reset", "func")
        dist = s.parms["dist"]["value"]
        s.parms["tr"]["value"] = [0, 0, dist]
        s.parms["rot"]["value"] = [315, 45, 0]
        s.parms["pvt"]["value"] = [0, 0, -dist]
        s.parms["pvt_rot"]["value"] = [0, 0, 0]
        s.parms["tru_pvt"]["value"] = [0, 0, 0]
        s.parms["ow"]["value"] = 10
        s.cam_update()
        s.drawable_update_pvt()
        s.drawable_update_ray()

    def cam_rot(s, key):
        s.v_log("cam_rot", "func")
        rot = list(s.parms["rot"]["value"])
        delt = s.hud_dict_delta["rot"]
        if key == "h": rot[1] += delt
        elif key == "j": rot[0] -= delt
        elif key == "k": rot[0] += delt
        elif key == "l": rot[1] -= delt
        rot[0] %= 360
        rot[1] %= 360
        s.parms["rot"]["value"] = rot

    def cam_set_view(s):
        s.v_log("cam_set_view", "func")
        d = s.hud_dict_layout
        s.v_log(d["viewport"], "normal")
        s.v_log(d["viewport_arr"], "normal")

    def cam_to_state(s):
        s.v_log("cam_to_state", "func")
        cam = s.cam
        s.parms["tr"]["value"] = list(cam.evalParmTuple("t"))
        s.parms["pvt"]["value"] = list(cam.evalParmTuple("p"))
        s.parms["rot"]["value"] = list(cam.evalParmTuple("r"))
        s.parms["pvt_rot"]["value"] = list(cam.evalParmTuple("pr"))
        s.parms["ow"]["value"] = cam.evalParm("orthowidth")

    def cam_tr(s, key):
        s.v_log("cam_tr", "func")
        # tru_pvt = list(s.parms["tru_pvt"]["value"])
        # s.cam_get_dir()
        pvt = list(s.parms["pvt"]["value"])
        tr = list(s.parms["tr" ]["value"])
        delt = s.hud_dict_delta["tr"]
        if key == "h":
            pvt[0] -= delt
        elif key == "j":
            pvt[1] -= delt
            tr[1] -= delt
        elif key == "k":
            pvt[1] += delt
            tr[1] += delt
        elif key == "l":
            pvt[0] += delt
        #s.parms["pvt"]["value"] = pvt
        s.parms["tr"]["value"] = tr

    def cam_update(s):
        s.v_log("cam_update", "func")
        # convert tru_pivot
        tru_pvt = 1
        if tru_pvt:
            tru_pvt = s.parms["tru_pvt"]["value"]
            dist = s.parms["dist"]["value"]
            #s.parms["tr"]["value"][0] = tru_pvt[0]
            #s.parms["tr"]["value"][1] = tru_pvt[1]
            s.parms["tr"]["value"][2] = dist
            #s.parms["pvt"]["value"][0] = 0
            #s.parms["pvt"]["value"][1] = 0
            s.parms["pvt"]["value"][2] = tru_pvt[2] - dist
        # transfer state parameters to camera
        s.cam.parmTuple("r").set(s.parms["rot"]["value"])
        s.cam.parmTuple("t").set(s.parms["tr"]["value"])
        s.cam.parmTuple("p").set(s.parms["pvt"]["value"])
        s.cam.parmTuple("pr").set(s.parms["pvt_rot"]["value"])
        s.cam.parm("orthowidth").set(s.parms["ow"]["value"])

    def cam_xform(s, key):
        s.v_log("cam_xform", "func")
        # gather vars
        vp = s.vp_get()[0]
        type = vp.type()
        if "main" in s.hud_dict_layout["vp_name"]:
            if key[0] == "S": s.cam_tr(key[-1])
            else: s.cam_rot(key)
            s.cam_update()
            s.drawable_update_pvt()
            s.drawable_update_ray()
        else:
            vp = s.viewer.findViewport(s.vp_name)
            cam = vp.defaultCamera()
            tr = list(cam.translation())
            ti = s.unit_dict["tr"]
            idx_arr = [0, 0]
            if "top" in s.vp_name: idx_arr = [0, 1]
            elif "bottom" in s.vp_name: idx_arr = [2, 0]
            elif "front" in s.vp_name: idx_arr = [0, 1]
            elif "back" in s.vp_name: idx_arr = [1, 0]
            elif "right" in s.vp_name: idx_arr = [0, 1]
            elif "left" in s.vp_name: idx_arr = [1, 2]
            if key == "h": tr[idx_arr[0]] += ti
            elif key == "j": tr[idx_arr[1]] += ti
            elif key == "k": tr[idx_arr[1]] -= ti
            elif key == "l": tr[idx_arr[0]] -= ti
            cam.setTranslation(tr)

    def cam_zoom(s, key):
        s.v_log("cam_zoom", "func")
        vp_arr = s.vp_get()
        for vp in vp_arr:
            if vp.type() == s.vp_persp:
                proj = s.cam.parm("projection").evalAsString()
                if proj == "perspective":
                    if key == "=": s.parms["dist"]["value"] -= s.hud_dict_delta["dist"]
                    elif key == "-": s.parms["dist"]["value"] += s.hud_dict_delta["dist"]
                elif proj == "ortho":
                    if key == "Shift+-": s.parms["dist"]["value"] -= s.hud_dict_delta["dist"]
                    elif key == "Shift+=": s.parms["dist"]["value"] += s.hud_dict_delta["dist"]
                    elif key == "-": s.parms["ow"]["value"] += s.hud_dict_delta["ow"]
                    elif key == "=": s.parms["ow"]["value"] -= s.hud_dict_delta["ow"]
                s.cam_update()
                s.drawable_update_pvt()
                s.drawable_update_ray()
            else:
                cam = vp.defaultCamera()
                ow = cam.orthoWidth()
                if key == "-": cam.setOrthoWidth(ow + s.hud_dict_delta["ow"])
                elif key == "=": cam.setOrthoWidth(ow - s.hud_dict_delta["ow"])

    def drawable_toggle_bbx(s, kwargs, action):
        s.v_log("drawable_toggle_bbx", "func")
        enabled = kwargs["toggle_bbx"]
        s.drawable_update_bbx()

    def drawable_update_axis(s, kwargs, code):
        s.v_log("drawable_update_axis", "func")
        # set
        if code == "show_all": s.axes = [1, 1, 1]
        elif code == "hide_all": s.axes = [0, 0, 0]
        elif code == "x": s.axes[0] = kwargs["x_axis"]
        elif code == "y": s.axes[1] = kwargs["y_axis"]
        elif code == "z": s.axes[2] = kwargs["z_axis"]
        # draw
        dd = s.hud_dict_delta
        size = dd["axis_size"]
        geo  = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, "Cd", (1, 1, 1))
        for idx in (0, 1, 2):
            if s.axes[idx]:
                p0 = [0, 0, 0]
                p1 = [0, 0, 0]
                p0[idx] = -size
                p1[idx] = size
                pts = geo.createPoints((p0, p1))
                cd = [0, 0, 0]
                cd[idx] = 1
                pts[0].setAttribValue("Cd", cd)
                pts[1].setAttribValue("Cd", cd)
                prim = geo.createPolygon(is_closed=False)
                prim.addVertex(pts[0])
                prim.addVertex(pts[1])
        s.drawable_axis.setGeometry(geo)
        s.drawable_axis.setParams({"fade_factor": 0.0})

    def drawable_update_bbox(self):
        s.v_log("drawable_update_bbox", "func")
        geo = s.get_get()
        bbox = geo.boundingBox()
        p0 = (bbox[0], bbox[1], bbox[2])
        p1 = (bbox[0], bbox[1], bbox[5])
        p2 = (bbox[3], bbox[1], bbox[5])
        p3 = (bbox[3], bbox[1], bbox[2])
        p4 = (bbox[0], bbox[4], bbox[2])
        p5 = (bbox[0], bbox[4], bbox[5])
        p6 = (bbox[3], bbox[4], bbox[5])
        p7 = (bbox[3], bbox[4], bbox[2])
        print(bbox)

    def drawable_update_pvt(s):
        s.v_log("drawable_update_pvt", "func")
        rot = list(s.parms["rot"]["value"])
        tr = list(s.parms["tr" ]["value"])
        pvt = list(s.parms["pvt"]["value"])
        ow = s.parms["ow"]["value"]
        scale = ow * 0.0075
        P = hou.Vector3(pvt) + hou.Vector3(tr)
        geo = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({"type": 1, "r": rot, "t": P, "scale": scale})
        verb.execute(geo, [])
        s.drawable_pvt.setGeometry(geo)
        s.drawable_pvt.setParams({
            "color1": hou.Vector4(0.0, 0.0, 1, 1),
            "fade_factor": 1.0
        })

    def drawable_update_ray(s):
        s.v_log("drawable_update_ray", "func")
        tr = s.parms["tr"]["value"]
        rot = s.parms["rot"]["value"]
        pvt = s.parms["pvt"]["value"]
        tru_pvt = s.parms["tru_pvt"]["value"]
        rot = hou.hmath.buildRotate(rot)
        cam_P = hou.Vector3(0, 0, s.cam_get_len()) * rot
        cam_P += hou.Vector3(tru_pvt[0], tru_pvt[1], tru_pvt[2])
        pvt_P = hou.Vector3(tr) + hou.Vector3(pvt)
        geo = hou.Geometry()
        pts = geo.createPoints((cam_P, pvt_P))
        prim = geo.createPolygon()
        prim.addVertex(pts[0])
        prim.addVertex(pts[1])
        s.drawable_ray.setGeometry(geo)

    def focus_set_attr(s):
        s.v_log("focus", "func")
        #if key == "j": s.focus_sel = s.list_next(s.focus_arr, s.focus_sel)
        #elif key == "k": s.focus_sel = s.list_prev(s.focus_arr, s.focus_sel) 
        attr = hou.ui.readInput("focus_attr", buttons=("OK", "Cancel"), initial_contents=s.hud_dict_focus["focus_attr"])
        if attr[0] == 0:
            s.hud_dict_focus["focus_attr"] = attr[1]
        #s.v_log(s.hud_dict_focus["attr"], "normal")
        #s.hud_update()

    def geo_frame( s ):
        s.v_log("geo_frame", "func")
        for vp in s.viewer.viewports():
            cam = vp.camera()
            if cam == None: vp.frameAll()
            else: vp.frameAll()
        #[vp.frameAll() for vp in s.viewer.viewports()]
        s.cam_to_state()
        #s.drawable_update_pvt()

    def geo_get_centroid(s):
        s.v_log("geo_get_centroid", "func")
        geo = s.geo_get()
        result_geo = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(result_geo, [geo])
        pt = result_geo.point(0)
        centroid = pt.position()
        return centroid

    def geo_get_extrema(s):
        s.v_log("geo_get_extrema", "func")
        geo = s.geo_get()
        bbx = geo.boundingBox()

    def geo_get(s):
        s.v_log("geo_get", "func")
        display_node = s.viewer.pwd().displayNode()
        geo = display_node.geometry()
        return geo

    def hud_g_ct(s):
        # calculate the number of bars in a graph based on the length of the corresponding array
        s.v_log("hud_g_ct", "func")
        hud_name = s.hud
        d = getattr(s, "hud_dict_" + hud_name)
        hud_dict = getattr(s, "HUD_" + hud_name.upper())
        # counter keeps track of the index of the row within the hud
        ct = 0
        for x in hud_dict["rows"]:
            # if the row id indicates it is a graph
            if x["id"][-2:] == "_g":
                arr = None
                # count the number of items in the array
                if x["id"] == "hud_g": arr = s.hud_arr
                else: arr = d[x["id"][0:-2] + "_arr"]
                # set the number of bars in the graph
                hud_dict["rows"][ct]["count"] = len(arr)
            ct += 1

    def hud_mode(s):
        s.v_log("hud_mode", "func")
        idx = s.mode_arr.index(s.mode)
        idx += 1
        idx %= 2
        s.mode = s.mode_arr[idx]
        s.hud_update()
        s.cam_fit_aspect()

    def hud_nav(s, key):
        s.v_log("hud_nav", "func")
        # source common variables
        d = getattr(s, "hud_dict_" + s.hud)
        d["hud_arr"] = s.hud_arr
        d["hud"] = s.hud
        ctrl = d["ctrl"]
        # select control        
        if key in ("j", "k"):
            ctrl_arr = d["ctrl_arr"]
            ctrl_idx = ctrl_arr.index(ctrl)
            if key == "j": ctrl_idx += 1
            elif key == "k": ctrl_idx -= 1
            ctrl_idx %= len(ctrl_arr)
            ctrl = ctrl_arr[ctrl_idx]
            d["ctrl"] = ctrl
        # change control value
        elif key in ("h", "l"):
            if ctrl == "attr":
                s.focus_set_attr() 
            else:
                ctrl_val_arr = d[ctrl + "_arr"] 
                ctrl_val = d[ctrl]
                ctrl_val_idx = ctrl_val_arr.index(ctrl_val)
                if key == "h": ctrl_val_idx -= 1
                elif key == "l": ctrl_val_idx += 1 
                ctrl_val_idx %= len(ctrl_val_arr)
                ctrl_val = ctrl_val_arr[ctrl_val_idx]
                d[ctrl] = ctrl_val_arr[ctrl_val_idx]

        # update dict 
        #setattr(s, s.hud + "_hud_dict", hud_dict)
        if ctrl == "layout": s.vp_layout_set()
        elif ctrl == "main_vp_view": s.cam_set_view()
        #elif s.hud == "delta":
        #    if key == "h": s.delta_dict[val ] -= s.unit_dict[val]
        #    elif key == "j": s.unit_dict["val"] = s.list_prev(val_arr, val)
        #    elif key == "k": s.unit_dict["val"] = s.list_next(val_arr, val)
        #    elif key == "l": s.delta_dict[val ] += s.unit_dict[val]
        s.hud = d["hud"]
        s.hud_update()

    def hud_update(s):
        # fetch and assign the new values for all hud rows
        s.v_log("hud_update", "func")
        s.hud_g_ct()
        updates = None
        # get the hud value dict and the hud format dict
        v_d = getattr(s, "hud_dict_" + s.hud)
        f_d = getattr(s, "HUD_" + s.hud.upper())
        # set the hud to the appropriate format dict
        s.viewer.hudInfo(template=f_d)

        # find the new update values
        updates = {}
        for row in f_d["rows"]:
            if row["id"] != "divider":
                # first three are common to all huds
                if row["id"] == "mode": updates["mode"] = {"value": s.mode}
                elif row["id"] == "hud": updates["hud"] = {"value": s.hud}
                elif row["id"] == "hud_g": updates["hud_g"] = {"value": s.hud_arr.index(s.hud)}
                # if it is a graph
                elif row["id"][-2:] == "_g":
                    val_name = row["id"][0:-2]
                    val = v_d[val_name]
                    val_arr = v_d[val_name + "_arr"]
                    updates[row["id"]] = {"value": val_arr.index(val)}
                else:
                    val_name = row["id"]
                    val = v_d[val_name]
                    updates[row["id"]] = {"value": val}

        if s.mode == "settings":
            updates[v_d["ctrl"]]["value"] = "[" + updates[v_d["ctrl"]]["value"] + "]"
        s.viewer.hudInfo(hud_values=updates)

    def init_parms(s):
        s.v_log("init_parms", "func")
        cam = s.cam
        s.parms["tr"]["value"] = list(cam.evalParmTuple("t"))
        s.parms["pvt"]["value"] = list(cam.evalParmTuple("p"))
        s.parms["rot"]["value"] = list(cam.evalParmTuple("r"))
        s.parms["pvt_rot"]["value"] = list(cam.evalParmTuple("pr"))
        s.parms["ow"]["value"] = cam.evalParm("orthowidth")

    def init_settings(s):
        s.v_log("init_settings", "func")
        # reset camera
        if s.init_reset: s.cam_reset()
        else: s.cam_to_state()
        # keycam node display flag
        s.cam.setDisplayFlag(s.init_cam_display)

    def list_next(s, list, sel):
        idx = list.index(sel)
        idx = (idx + 1) % len(list)
        return idx

    def list_prev(s, list, sel):
        idx = list.index(sel)
        idx = (idx - 1) % len(list)
        return idx

    def print(s, key):
        s.v_log("print", "func")
        if key == "cam_vals":
            t = s.parms["t"]["value"]
            r = s.parms["r"]["value"]
            p = s.parms["p"]["value"]
            p = s.parms["pr"]["value"]
            s.v_log("r:\n", r, "t:\n", t, "p:\n", p, "pr:\n", pr, "normal")
        elif key == "centroid":
            s.v_log(s.geo_get_centroid(), "normal")
        elif key == "hud_state":
            x=1
        elif key == "vp":
            s.v_log(s.vp, "normal")

    def print_kwargs(s, kwargs):
        s.v_log("print_kwargs", "func")
        s.v_log_separator()
        ui_event = str(kwargs["ui_event"])
        ui_event = ui_event.replace("\\n", "\n")
        del kwargs["ui_event"]
        s.v_log_separator()
        s.v_log(ui_event, "normal")

    def vp_arr_populate(s):
        s.v_log("vp_arr_populate", "func")
        vp_arr = list( s.viewer.viewports() )
        vp_arr.reverse()
        vp_name_arr = []
        for vp in vp_arr:
            if vp.type() == s.vp_persp: vp_name_arr.append("main")
            else: vp_name_arr.append(vp.name())
        vp_name_arr.append("non-main")
        s.hud_dict_layout["vp_name_arr"] = vp_name_arr
        s.hud_dict_layout["vp_name"] = vp_name_arr[0]
        s.hud_dict_layout["layout" ] = str(s.viewer.viewportLayout()).split(".")[-1]

    def vp_focus(s):
        s.v_log("vp_focus", "func")

    def vp_get(s):
        s.v_log("vp_get", "func")
        vp_name = s.hud_dict_layout["vp_name"]
        if vp_name == "main": 
            return [s.viewer.findViewport("persp1")]
        elif vp_name == "non-main":
            vp_arr = []
            for vp in s.viewer.viewports():
                if vp.name() != "persp1":
                    vp_arr.append(vp)
            vp_arr.reverse()
            return vp_arr
        else:
            return [s.viewer.findViewport(s.vp_name)]

    def vp_layout_set(s):
        s.v_log("vp_layout_set", "func")
        layout = s.hud_dict_layout["layout"]
        s.viewer.setViewportLayout(getattr(hou.geometryViewportLayout, layout))

    def vp_swap(s):
        s.v_log("vp_swap", "func")
        vp_arr = s.viewer.viewports()
        vp_name_arr = [vp.name() for vp in vp_arr]

        vp_name_arr = vp_name_arr[1:] + [vp_name_arr[0]]
        vp_type_arr = vp_type_arr[1:] + [vp_type_arr[0]]
        for i, vp in enumerate(vp_arr):
            vp.changeName("v" * i)
        for i, vp in enumerate(vp_arr):
            vp.changeName(vp_name_arr[i])
            vp.changeType(vp_type_arr[i])
        # s.v_log(v_name_arr, "normal")
        # s.v_log(v_type_arr, "normal")

    def vp_type_set(s, code):
        s.v_log("vp_type_set", "func")
        vp_name = s.vp
        vp = s.viewer.findViewport(vp_name)
        if code == "persp": vp.changeType(s.vp_persp)
        elif code == "top": vp.changeType(s.vp_top)
        elif code == "bottom": vp.changeType(s.vp_bottom)
        elif code == "front": vp.changeType(s.vp_front)
        elif code == "back": vp.changeType(s.vp_back)
        elif code == "right": vp.changeType(s.vp_right)
        elif code == "left": vp.changeType(s.vp_left)

    def v_log(s, message, level):
        if level == "normal": s.log(message)
        elif level == "func": s.log(message, severity=hou.severityType.ImportantMessage)

    def v_log_separator(s):
        s.v_log("-------------------------", "normal")

    ##
    ##

    def onDraw(s, kwargs):
        dh = kwargs["draw_handle"]
        s.drawable_axis.draw(dh, {})
        s.drawable_pvt.draw(dh, {})
        s.drawable_ray.draw(dh, {})
        s.drawable_txt.draw(dh, {})

    def onGenerate(s, kwargs):
        s.v_log_separator()
        s.v_log("onGenerate", "func")
        # prevent exiting state when selecting nodes
        kwargs["state_flags"]["exit_on_node_select"] = False
        # init vars
        s.vp = s.viewer.selectedViewport()
        s.parms = kwargs["state_parms"]
        # vp/cam
        s.vp_arr_populate()
        s.cam_init()
        # parms
        s.init_parms()
        # hud
        s.hud_update()
        s.init_settings()

    def onKeyEvent(s, kwargs):
        s.v_log_separator()
        s.v_log("onKeyEvent", "func")
        key = kwargs["ui_event"].device().keyString()
        s.v_log(key, "normal")
        # navigate
        if key[-1] in ("h", "j", "k", "l"):
            if s.mode == "navigate": s.cam_xform(key)
            elif s.mode == "settings": s.hud_nav(key)
            return True
        # hud mode
        elif key == "m":
            s.hud_mode()
            return True
        # change projection
        elif key == "o":
            s.cam_next_proj()    
            return True
        # zoom
        elif key[-1] in ("-", "="):
            s.cam_zoom(key)
            return True
        # do nothing
        else:
            return False

    def onMenuAction(s, kwargs):
        s.v_log_separator()
        s.v_log("onMenuAction", "func")
        action = kwargs["menu_item"]
        # move pvt
        if action == "pvt_to_ray": s.cam_move_pvt("ray")
        elif action == "pvt_to_camera": s.cam_move_pvt("camera")
        elif action == "pvt_to_centroid": s.cam_move_pvt("centroid")
        elif action == "pvt_to_origin": s.cam_move_pvt("origin")
        # frame (?)
        elif action == "geo_frame": s.geo_frame()
        # adjust cam
        elif action == "cam_reset": s.cam_reset()
        elif action == "cam_fit_aspect": s.cam_fit_aspect()
        elif action == "cam_to_state": s.cam_to_state()
        elif action == "toggle_bbx": s.toggle_bbox(kwargs, action)
        # axis
        elif action == "show_all_axes": s.drawable_update_axis(kwargs, "show_all")
        elif action == "hide_all_axes": s.drawable_update_axis(kwargs, "hide_all")
        elif action == "x_axis": s.drawable_update_axis(kwargs, "x")
        elif action == "y_axis": s.drawable_update_axis(kwargs, "y")
        elif action == "z_axis": s.drawable_update_axis(kwargs, "z")
        # vw Menu
        elif action == "vp_swap": s.vp_swap()
        # test menu
        elif action == "vp_arr_populate": s.vp_arr_populate()
        # print menu
        elif action == "print_cam_vals": s.print("cam_vals")
        elif action == "print_centroid": s.print("centroid")
        elif action == "print_kwargs": s.print_kwargs(kwargs)
        elif action == "print_vp": s.print("vp")

        # def onMouseEvent(s, kwargs):
        #     node = kwargs["node"]
        #     ui_event = kwargs["ui_event"]
        #     scrx = ui_event.device().mouseX()
        #     scry = ui_event.device().mouseY()
        #     if ui_event.reason() == hou.uiEventReason.Picked\
        #         or ui_event.reason() == hou.uiEventReason.Start:
        #         origin, dir = ui_event.ray()
        #         prim = s.vp.queryPrimAtPixel(None, round(scrx), round(scry))
        #         if prim == None:
        #             return
        #         else:
        #             val = prim.attribValue("sprue")
        #             if val == 0:
        #                 stash1 = node.node("stash1")
        #                 stash1.parm("stashinput").pressButton()
        #             else:
        #                 node.node("switch2").parm("input").set(1)
        #                 node.node("stash1").parm("stashinput").pressButton()
        #                 node.node("switch2").parm("input").set(0)

    def onParmChangeEvent(s, kwargs):
        updates = (0, 0, 0, 0, 0)
        pn = kwargs["parm_name"]
        if pn == "axis_size": updates = (1, 0, 0, 0, 0)
        elif pn == "dist": updates = (0, 1, 1, 1, 1)
        elif pn == "tr": updates = (0, 1, 1, 1, 1)
        elif pn == "rot": updates = (0, 1, 1, 1, 1)
        elif pn == "pvt": updates = (0, 1, 1, 1, 1)
        elif pn == "pvt_rot": updates = (0, 1, 1, 1, 1)
        elif pn == "tru_pvt": updates = (0, 1, 1, 1, 1)
        if updates[0]: s.drawable_update_axis()
        if updates[1]: s.cam_update()
        if updates[2]: s.cam_update()
        if updates[3]: s.drawable_update_pvt()
        if updates[4]: s.drawable_update_pvt()

def make_menu(template):
    menu = hou.ViewerStateMenu("keycam_menu", "keycam_menu")
    menu.addActionItem("pvt_to_ray", "pvt_to_ray")
    menu.addActionItem("pvt_to_cam", "pvt_to_cam")
    menu.addActionItem("pvt_to_centroid", "pvt_to_centroid")
    menu.addActionItem("pvt_to_origin", "pvt_to_origin")
    menu.addSeparator()
    menu.addActionItem("cam_reset", "cam_reset")
    menu.addActionItem("cam_fit_aspect", "cam_fit_aspect")
    menu.addActionItem("geo_frame", "geo_frame")
    menu.addActionItem("swap_vp", "swap_vp")
    menu.addSeparator()
    menu.addActionItem("show_all_axes", "show_all_axes")
    menu.addActionItem("hide_all_axes", "hide_all_axes")
    menu.addToggleItem("x_axis", "x_axis", 1)
    menu.addToggleItem("y_axis", "y_axis", 1)
    menu.addToggleItem("z_axis", "z_axis", 1)
    menu.addToggleItem("toggle_bbox", "toggle_bbox", 0)
    menu.addSeparator()
    menu.addActionItem("print_cam_vals", "print_cam_vals")
    menu.addActionItem("print_kwargs", "print_kwargs")
    menu.addActionItem("print_centroid", "print_centroid")
    menu.addActionItem("print_vp", "print_vp")
    menu.addSeparator()
    menu.addActionItem("cam_to_state", "cam_to_state")
    menu.addActionItem("vp_arr_populate", "vp_arr_populate")
    template.bindMenu(menu)

def make_parameters(template):
    t = template
    ptt = hou.parmTemplateType
    t.bindParameter(ptt.Float,"axis_size", "axis_size", default_value=2.0, toolbox=False)
    t.bindParameter(ptt.Separator, "sep0", toolbox=False)
    t.bindParameter(ptt.Float,"dist", "dist", default_value=10.0)
    t.bindParameter(ptt.Float,"ow", "ow", default_value=10.0)
    t.bindParameter(ptt.Separator, "sep1", toolbox=False)
    t.bindParameter(ptt.Float,"tr", "tr", num_components=3, toolbox=False)
    t.bindParameter(ptt.Float,"rot", "rot", num_components=3, toolbox=False)
    t.bindParameter(ptt.Float,"pvt", "pvt", num_components=3, toolbox=False)
    t.bindParameter(ptt.Float,"pvt_rot", "pvt_rot", num_components=3, toolbox=False)
    t.bindParameter(ptt.Separator, "sep2", toolbox=False)
    t.bindParameter(ptt.Float,"up", "up", num_components=3, toolbox=False)
    t.bindParameter(ptt.Float,"tru_pvt", "tru_pvt",  num_components=3, toolbox=False)

def createViewerStateTemplate():
    template = hou.ViewerStateTemplate(\
      type_name="keycam",
      label="keycam",
      category=hou.sopNodeTypeCategory(),
      contexts=[hou.objNodeTypeCategory()])
    make_menu(template)
    make_parameters(template)
    template.bindIcon("DESKTOP_application_sierra")
    template.bindFactory(State)
    return template
