# pyright: reportMissingImports=false
import hou
import pprint
import time
import viewerstate.utils as su

# abbreviations
# dd = delta_dict
# nd = nav_dict
# ow = orthowidth
# tr = translation
# vp = viewport
# vwr = viewer

class State(object):
    HUD_NAV = {
        "title": "nav",
        "rows": [
            {"id"  : "mode"        , "label": "mode"       , "key"  :"M"},
            {"id"  : "mode_g"      , "type" : "choicegraph", "count": 5 },
            {"type": "divider"                                          },
            {"id"  : "vp_name"     , "label": "viewport"                },
            {"id"  : "vp_name_g"   , "type" : "choicegraph", "count": 4 },
            {"id"  : "layout"      , "label": "layout"                  },
            {"id"  : "layout_g"    , "type" : "choicegraph", "count": 8 },
            {"id"  : "target"      , "label": "target"                  },
            {"id"  : "target_g"    , "type" : "choicegraph", "count": 2 }
        ]
    }

    HUD_DELTA = {
        "title": "delta",
        "rows": [
            {"id"  : "mode"     , "label": "mode"       , "key"  : "M"          },
            {"id"  : "mode_g"   , "type" : "choicegraph", "count": 5, "value": 2},
            {"type": "divider"                                                  },
            {"id"  : "axis_size", "label": "axis_size"                          },
            {"id"  : "rot"      , "label": "rot_delta"                          },
            {"id"  : "tr"       , "label": "tr_delta"                           },
            {"id"  : "dist"     , "label": "dist_delta"                         },
            {"id"  : "ow"       , "label": "ortho_width_delta"                  }
        ]
    }

    HUD_VIS = {
        "title": "vis",
        "rows": [
            {"id"  : "mode"  , "label": "mode"       , "key"  : "M"          },
            {"id"  : "mode_g", "type" : "choicegraph", "count": 5, "value": 3},
            {"type": "divider"                                               },
            {"id"  : "viz"   , "label": "vis"                                }
        ]
    }

    HUD_FOCUS = {
        "title": "focus",
        "rows": [
            {"id"  : "mode"     , "label": "mode"       , "key"  : "M"           },
            {"id"  : "mode_g"   , "type" : "choicegraph", "count": 5 , "value": 4},
            {"type": "divider"                                                   },
            {"id"  : "attr"     , "label": "attr"       , "value": "partition"   },
            {"id"  : "focus"    , "label": "focus"      , "value": 0             },
            {"id"  : "focus_g"  , "type" : "choicegraph", "count": 10            }
        ]
    }

    def __init__(s, state_name, scene_viewer):
        s.state_name       = state_name
        s.axes             = [1, 1, 1]
        s.ctrl_arr         = ("vp_name", "layout", "target")
        s.ctrl             = "vp_name"
        s.focus_attr       = "partition"
        s.focus_arr        = ("attribute", "focus")
        s.focus_idx        = 0
        s.focus_sel        = "attribute"
        s.layout_arr       = ("DoubleSide", "DoubleStack", "Quad", "QuadBottomSplit", "QuadLeftSplit", "Single", "TripleBottomSplit", "TripleLeftSplit")
        s.layout           = "Single"
        s.mode_arr         = ("nav", "ctrl", "delta", "vis", "focus")
        s.mode             = "nav"
        s.init_reset       = 1
        s.init_cam_display = 0
        s.target_arr       = ("cam", "pivot")
        s.target           = "cam"
        s.vp_name_arr      = ()
        s.vp_name          = ""
        s.vw_arr           = ("persp", "top", "bottom", "front", "back", "right", "left")
        s.vwr              = scene_viewer

        s.unit_dict={
            "axis_size": 4,
            "rot"      : 7.5,
            "tr"       : 1,
            "ow"       : 1,
            "dist"     : 1
        }

        s.delta_dict={
            "val_arr"  : ("axis_size", "rot", "tr", "dist", "ow"),
            "val"      : "axis_size",
            "axis_size": s.unit_dict["axis_size"],
            "rot"      : s.unit_dict["rot"],
            "tr"       : s.unit_dict["tr"],
            "ow"       : s.unit_dict["ow"],
            "dist"     : s.unit_dict["dist"]
        }

        # drawables
        s.drawable_axis = hou.GeometryDrawable(
            scene_viewer=s.vwr,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_axis",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))}
        )

        s.drawable_bbox = hou.GeometryDrawable(
            scene_viewer=s.vwr,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))}
        )

        s.drawable_pvt = hou.GeometryDrawable(
            scene_viewer=s.vwr,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_pvt"
        )

        s.drawable_ray = hou.GeometryDrawable(
            scene_viewer=s.vwr,
            geo_type=hou.drawableGeometryType.Line,
            name="drawable_ray",
            params={"color1": hou.Vector4((1, 0.8, 1, 0.5))}
        )

        s.drawable_txt = hou.TextDrawable(
            scene_viewer=s.vwr,
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
        vp    = s.vwr.findViewport("persp1")
        ratio = vp.size()[2] / vp.size()[3]
        s.cam.parm("aspect").set(ratio)

    def cam_from_state(s):
        s.v_log("cam_from_state", "func")
        x=1

    def cam_get_dir(s):
        s.v_log("cam_get_dir", "func")
        tru_pvt = s.parms["tru_pvt"]["value"]
        tr      = s.parms["tr"     ]["value"]
        s.v_log(hou.Vector3(tru_pvt) - hou.Vector3(tr), "normal")
        return

    def cam_get_dist(s):
        s.v_log("cam_get_dist", "func")
        dist = s.parms["dist"]["value"]
        return dist

    def cam_get_len(s):
        s.v_log("cam_get_len", "func")
        tr  = s.parms["tr" ]["value"]
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
        tr  = [0, 0, 0]
        rot = [0, 0, 0]
        pvt = [0, 0, 0]
        ow  = 1
        # check if cam is default cam
        cam = vp.camera()
        if cam == None:
            cam = vp.defaultCamera()
            tr  = cam.translation()
            rot = cam.rotation()
            pvt = cam.pivot()
            ow  = cam.orthoWidth()
        else:
            tr  = cam.evalParmTuple("t")
            rot = cam.evalParmTuple("r")
            pvt = cam.evalParmTuple("p")
            ow  = cam.evalParm("orthowidth")
        s.cam = hou.node("/obj/keycam")
        vp.setCamera(s.cam)
        vp.lockCameraToView(1)

    def cam_move_pvt(s):
        s.v_log("cam_move_pvt", "func")
        target = s.nav_dict["target"]
        if   target == "cam":
            tr                          = s.parms["tr"]["value"]
            s.parms["tru_pvt"]["value"] = list(tr)
        elif target == "centroid":
            centroid                    = s.geo_get_centroid()
        elif target == "origin":
            s.parms["tr"     ]["value"] = [0, 0, s.cam_get_dist()]
            s.parms["rot"    ]["value"] = [45, 45, 0]
            s.parms["pvt"    ]["value"] = [0, 0, -s.cam_get_dist()]
            s.parms["pvt_rot"]["value"] = [0, 0, 0]
            s.parms["tru_pvt"]["value"] = [0, 0, 0]
            s.parms["ow"     ]["value"] = 10
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
        if   proj == "ortho":       proj_parm.set("perspective")
        elif proj == "perspective": proj_parm.set("ortho")

    def cam_proj_update(s):
        s.v_log("cam_proj_update", "func")
        cam = s.cam
        proj_parm = cam.parm("projection")
        if   s.proj == "ortho": proj_parm.set("ortho")
        elif s.proj == "persp": proj_parm.set("perspective")
        s.geo_frame()

    def cam_reset(s):
        s.v_log("cam_reset", "func")
        dist = s.cam_get_dist()
        s.parms["tr"     ]["value"] = [0, 0, dist]
        s.parms["rot"    ]["value"] = [315, 45, 0]
        s.parms["pvt"    ]["value"] = [0, 0, -dist]
        s.parms["pvt_rot"]["value"] = [0, 0, 0]
        s.parms["tru_pvt"]["value"] = [0, 0, 0]
        s.parms["ow"     ]["value"] = 10
        s.cam_update()
        s.drawable_update_pvt()
        s.drawable_update_ray()

    def cam_rot(s, key):
        s.v_log("cam_rot", "func")
        dd = s.delta_dict
        rot = list(s.parms["rot"]["value"])
        rot_delta = dd["rot"]
        if   key == "h": rot[1] = (rot[1] + rot_delta) % 360
        elif key == "j": rot[0] = (rot[0] - rot_delta) % 360
        elif key == "k": rot[0] = (rot[0] + rot_delta) % 360
        elif key == "l": rot[1] = (rot[1] - rot_delta) % 360
        s.parms["rot"]["value"] = rot

    def cam_to_state(s):
        s.v_log("cam_to_state", "func")
        cam = s.cam
        s.parms["tr"     ]["value"] = list(cam.evalParmTuple("t"))
        s.parms["pvt"    ]["value"] = list(cam.evalParmTuple("p"))
        s.parms["rot"    ]["value"] = list(cam.evalParmTuple("r"))
        s.parms["pvt_rot"]["value"] = list(cam.evalParmTuple("pr"))
        s.parms["ow"     ]["value"] = cam.evalParm("orthowidth")

    def cam_tr(s, key):
        s.v_log("cam_tr", "func")
        # tru_pvt = list(s.parms["tru_pvt"]["value"])
        # s.cam_get_dir()
        pvt = list(s.parms["pvt"]["value"])
        tr  = list(s.parms["tr" ]["value"])
        if   key == "h": pvt[0] = pvt[0] - s.delta_dict["tr"]
        elif key == "j":
            pvt[1] = pvt[1] - s.delta_dict["tr"]
            tr[1]  = tr[1]  - s.delta_dict["tr"]
        elif key == "k":
            pvt[1] = pvt[1] + s.delta_dict["tr"]
            tr[1]  = tr[1]  + s.delta_dict["tr"]
        elif key == "l": pvt[0] = pvt[0] + s.delta_dict["tr"]
        #s.parms["pvt"]["value"] = pvt
        s.parms["tr" ]["value"] = tr

    def cam_update(s):
        s.v_log("cam_update", "func")
        # convert tru_pivot
        tru_pvt = 1
        if tru_pvt:
            tru_pvt = s.parms["tru_pvt"]["value"]
            dist    = s.parms["dist"   ]["value"]
            #s.parms["tr" ]["value"][0] = tru_pvt[0]
            #s.parms["tr" ]["value"][1] = tru_pvt[1]
            s.parms["tr" ]["value"][2] = dist
            #s.parms["pvt"]["value"][0] = 0
            #s.parms["pvt"]["value"][1] = 0
            s.parms["pvt"]["value"][2] = tru_pvt[2] - dist
        # transfer state parameters to camera
        s.cam.parmTuple("r" ).set(s.parms["rot"    ]["value"])
        s.cam.parmTuple("t" ).set(s.parms["tr"     ]["value"])
        s.cam.parmTuple("p" ).set(s.parms["pvt"    ]["value"])
        s.cam.parmTuple("pr").set(s.parms["pvt_rot"]["value"])
        s.cam.parm("orthowidth").set(s.parms["ow"]["value"])

    def cam_xform(s, key):
        s.v_log("cam_xform", "func")
        # gather vars
        vp   = s.vp_get()[0]
        type = vp.type()
        if "main" in s.vp_name:
            if key[0] == "S": s.cam_tr(key[-1])
            else            : s.cam_rot(key)
            s.cam_update()
            s.drawable_update_pvt()
            s.drawable_update_ray()
        else:
            vp      = s.vwr.findViewport(s.vp_name)
            cam     = vp.defaultCamera()
            tr      = list(cam.translation())
            ti      = s.unit_dict["tr"]
            idx_arr = [0, 0]
            if   "top"    in s.vp_name: idx_arr = [0, 1]
            elif "bottom" in s.vp_name: idx_arr = [2, 0]
            elif "front"  in s.vp_name: idx_arr = [0, 1]
            elif "back"   in s.vp_name: idx_arr = [1, 0]
            elif "right"  in s.vp_name: idx_arr = [0, 1]
            elif "left"   in s.vp_name: idx_arr = [1, 2]
            if   key == "h": tr[idx_arr[0]] += ti
            elif key == "j": tr[idx_arr[1]] += ti
            elif key == "k": tr[idx_arr[1]] -= ti
            elif key == "l": tr[idx_arr[0]] -= ti
            cam.setTranslation(tr)

    def cam_zoom(s, key):
        s.v_log("cam_zoom", "func")
        vp_arr = s.vp_get()
        for vp in vp_arr:
            if vp.type() == hou.geometryViewportType.Perspective:
                proj = s.cam.parm("projection").evalAsString()
                if   proj == "perspective":
                    if   key == "="      : s.parms["dist"]["value"] -= s.delta_dict["dist"]
                    elif key == "-"      : s.parms["dist"]["value"] += s.delta_dict["dist"]
                elif proj == "ortho":
                    if   key == "Shift+-": s.parms["dist"]["value"] -= s.delta_dict["dist"]
                    elif key == "Shift+=": s.parms["dist"]["value"] += s.delta_dict["dist"]
                    elif key == "-"      : s.parms["ow"  ]["value"] += s.delta_dict["ow"]
                    elif key == "="      : s.parms["ow"  ]["value"] -= s.delta_dict["ow"]
                s.cam_update()
                s.drawable_update_pvt()
                s.drawable_update_ray()
            else:
                cam = vp.defaultCamera()
                ow = cam.orthoWidth()
                if   key == "-": cam.setOrthoWidth(ow + s.delta_dict["ow"])
                elif key == "=": cam.setOrthoWidth(ow - s.delta_dict["ow"])

    def drawable_toggle_bbx(s, kwargs, action):
        s.v_log("drawable_toggle_bbx", "func")
        enabled = kwargs["toggle_bbx"]
        s.drawable_update_bbx()

    def drawable_update_axis(s, kwargs, code):
        s.v_log("drawable_update_axis", "func")
        # set
        if   code == "show_all": s.axes    = [1, 1, 1]
        elif code == "hide_all": s.axes    = [0, 0, 0]
        elif code == "x"       : s.axes[0] = kwargs["x_axis"]
        elif code == "y"       : s.axes[1] = kwargs["y_axis"]
        elif code == "z"       : s.axes[2] = kwargs["z_axis"]
        # draw
        dd   = s.delta_dict
        size = dd["axis_size"]
        geo  = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, "Cd", (1, 1, 1))
        for idx in (0, 1, 2):
            if s.axes[idx]:
                p0      = [0, 0, 0]
                p1      = [0, 0, 0]
                p0[idx] = -size
                p1[idx] = size
                pts     = geo.createPoints((p0, p1))
                cd      = [0, 0, 0]
                cd[idx] = 1
                pts[0].setAttribValue("Cd", cd)
                pts[1].setAttribValue("Cd", cd)
                prim    = geo.createPolygon(is_closed=False)
                prim.addVertex(pts[0])
                prim.addVertex(pts[1])
        s.drawable_axis.setGeometry(geo)
        s.drawable_axis.setParams({"fade_factor": 0.0})

    def drawable_update_bbox(self):
        s.v_log("drawable_update_bbox", "func")
        geo  = s.get_get()
        bbox = geo.boundingBox()
        p0   = (bbox[0], bbox[1], bbox[2])
        p1   = (bbox[0], bbox[1], bbox[5])
        p2   = (bbox[3], bbox[1], bbox[5])
        p3   = (bbox[3], bbox[1], bbox[2])
        p4   = (bbox[0], bbox[4], bbox[2])
        p5   = (bbox[0], bbox[4], bbox[5])
        p6   = (bbox[3], bbox[4], bbox[5])
        p7   = (bbox[3], bbox[4], bbox[2])
        print(bbox)

    def drawable_update_pvt(s):
        s.v_log("drawable_update_pvt", "func")
        rot   = list(s.parms["rot"]["value"])
        tr    = list(s.parms["tr" ]["value"])
        pvt   = list(s.parms["pvt"]["value"])
        ow    = s.parms["ow"]["value"]
        scale = ow * 0.0075
        P     = hou.Vector3(pvt) + hou.Vector3(tr)
        geo   = hou.Geometry()
        verb  = hou.sopNodeTypeCategory().nodeVerb("circle")
        verb.setParms({"type": 1, "r": rot, "t": P, "scale": scale})
        verb.execute(geo, [])
        s.drawable_pvt.setGeometry(geo)
        s.drawable_pvt.setParams({
            "color1": hou.Vector4(0.0, 0.0, 1, 1),
            "fade_factor": 1.0
        })

    def drawable_update_ray(s):
        s.v_log("drawable_update_ray", "func")
        tr      =  s.parms["tr"     ]["value"]
        rot     =  s.parms["rot"    ]["value"]
        pvt     =  s.parms["pvt"    ]["value"]
        tru_pvt =  s.parms["tru_pvt"]["value"]
        rot     =  hou.hmath.buildRotate(rot)
        cam_P   =  hou.Vector3(0, 0, s.cam_get_len()) * rot
        cam_P   += hou.Vector3(tru_pvt[0], tru_pvt[1], tru_pvt[2])
        pvt_P   =  hou.Vector3(tr) + hou.Vector3(pvt)
        geo     =  hou.Geometry()
        pts     =  geo.createPoints((cam_P, pvt_P))
        prim    =  geo.createPolygon()
        prim.addVertex(pts[0])
        prim.addVertex(pts[1])
        s.drawable_ray.setGeometry(geo)

    def geo_frame( s ):
        s.v_log("geo_frame", "func")
        for vp in s.vwr.viewports():
            cam = vp.camera()
            if cam == None: vp.frameAll()
            else          : vp.frameAll()
            
        #[vp.frameAll() for vp in s.vwr.viewports()]
        s.cam_to_state()
        #s.drawable_update_pvt()

    def geo_get_centroid(s):
        s.v_log("geo_get_centroid", "func")
        geo        = s.geo_get()
        result_geo = hou.Geometry()
        verb       = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(result_geo, [geo])
        pt         = result_geo.point(0)
        centroid   = pt.position()
        return centroid

    def geo_get_extrema(s):
        s.v_log("geo_get_extrema", "func")
        geo = s.geo_get()
        bbx = geo.boundingBox()

    def geo_get(s):
        s.v_log("geo_get", "func")
        display_node = s.vwr.pwd().displayNode()
        geo          = display_node.geometry()
        return geo

    def hud_change_focus(s, key):
        s.v_log("hud_change_focus", "func")
        if   key == "j": s.focus_sel = s.list_next(s.focus_arr, s.focus_sel)
        elif key == "k": s.focus_sel = s.list_prev(s.focus_arr, s.focus_sel) 
        elif key in ("h", "l"):
            attr = hou.ui.readInput("focus_attr", buttons=("OK", "Cancel"), initial_contents=s.focus_attr)
            if attr[0] == 0: s.focus_attr = attr[1]
        s.hud_update()

    def hud_change_ctrl(s, key):
        s.v_log("hud_change_ctrl", "func")
        # select ctrl
        if key in ("j", "k"):
            ctrl_idx = s.ctrl_arr.index(s.ctrl)
            if   key == "j": ctrl_idx += 1
            elif key == "k": ctrl_idx -= 1
            ctrl_idx %= len(s.ctrl_arr)
            s.ctrl = s.ctrl_arr[ctrl_idx]
        # change val
        elif key in ("h", "l"):
            val     = getattr(s, s.ctrl)
            val_arr = getattr(s, s.ctrl + "_arr")
            val_idx = val_arr.index(val)
            if   key == "h": val_idx -= 1
            elif key == "l": val_idx += 1
            val_idx %= len(val_arr)
            setattr(s, s.ctrl, val_arr[val_idx])
        if s.ctrl == "layout": s.vp_layout_set()
        s.hud_update()

    def hud_change_val(s, key):
        s.v_log("hud_change_val", "func")
        dd =      s.delta_dict
        ud =      s.unit_dict
        val =     vd["val"]
        val_arr = vd["val_arr"]
        if   key == "h": dd[val] -=  ud[val]
        elif key == "j": vd["val"] = s.list_prev(val_arr, val)
        elif key == "k": vd["val"] = s.list_next(val_arr, val)
        elif key == "l": vd[val] +=  dd[val]
        s.hud_update()

    def hud_next_mode(s):
        s.v_log("hud_next_mode", "func")
        idx = s.mode_arr.index(s.mode)
        idx += 1
        idx %= len(s.mode_arr)
        new_mode = s.mode_arr[idx]
        s.mode = new_mode
        s.hud_update()
        s.cam_fit_aspect()

    def hud_prev_mode(s):
        s.v_log("hud_prev_mode", "func")
        idx = s.mode_arr.index(s.mode)
        idx -= 1
        idx %= len(s.mode_arr)
        new_mode = s.mode_arr[idx]
        s.mode = new_mode
        s.hud_update()
        s.cam_fit_aspect()

    def hud_update(s):
        s.v_log("hud_update", "func")
        dd = s.delta_dict
        if s.mode == "nav":
            # change count of vp_name_arr graph
            s.HUD_NAV["rows"][4]["count"] = len(s.vp_name_arr)
            s.vwr.hudInfo(template=s.HUD_NAV)
            updates={
                "mode"        : {"value": s.mode},
                "mode_g"      : {"value": s.mode_arr.index(s.mode)},
                "vp_name"     : {"value": s.vp_name},
                "vp_name_g"   : {"value": s.vp_name_arr.index(s.vp_name)},
                "layout"      : {"value": s.layout},
                "layout_g"    : {"value": s.layout_arr.index(s.layout)},
                "target"      : {"value": s.target},
                "target_g"    : {"value": s.target_arr.index(s.target)}
            }
            s.vwr.hudInfo(hud_values=updates)

        elif s.mode == "ctrl":
            s.vwr.hudInfo(template=s.HUD_NAV)
            updates={
                "mode"        : {"value": s.mode},
                "mode_g"      : {"value": s.mode_arr.index(s.mode)},
                "vp_name"     : {"value": s.vp_name},
                "vp_name_g"   : {"value": s.vp_name_arr.index(s.vp_name)},
                "layout"      : {"value": s.layout},
                "layout_g"    : {"value": s.layout_arr.index(s.layout)},
                "target"      : {"value": s.target},
                "target_g"    : {"value": s.target_arr.index(s.target)}
            }
            updates[s.ctrl]["value"] = "[" + updates[s.ctrl]["value"] + "]"
            s.vwr.hudInfo(hud_values=updates)

        elif s.mode == "delta":
            s.vwr.hudInfo(template=s.HUD_DELTA)
            updates={
                "mode"     : {"value": s.mode},
                "mode_g"   : {"value": s.mode_arr.index(s.mode)},
                "axis_size": {"value": str(dd["axis_size"])},
                "rot"      : {"value": str(dd["rot"])},
                "tr"       : {"value": str(dd["tr"])},
                "ow"       : {"value": str(dd["ow"])},
                "dist"     : {"value": str(dd["dist"])}
            }
            updates[dd["val"]]["value"] = "[" + updates[dd["val"]]["value"] + "]"
            s.vwr.hudInfo(hud_values=updates)
        
        elif s.mode == "vis":
            s.vwr.hudInfo(template=s.HUD_VIS)
            updates={
            }
            s.vwr.hudInfo(hud_values=updates)

        elif s.mode == "focus":
            s.vwr.hudInfo(template=s.HUD_FOCUS)
            updates={
                "attr"   : {"value": s.focus_attr},
                "focus"  : {"value": str(0)},
                "focus_g": {"value": 0}
            }
            sel = s.focus_sel
            #updates[sel]["value"] = "[" + updates[sel]["value"] + "]"
            s.vwr.hudInfo(hud_values=updates)

    def init_parms(s):
        s.v_log("init_parms", "func")
        cam = s.cam
        s.parms["tr"     ]["value"] = list(cam.evalParmTuple("t"))
        s.parms["pvt"    ]["value"] = list(cam.evalParmTuple("p"))
        s.parms["rot"    ]["value"] = list(cam.evalParmTuple("r"))
        s.parms["pvt_rot"]["value"] = list(cam.evalParmTuple("pr"))
        s.parms["ow"     ]["value"] = cam.evalParm("orthowidth")

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
            t = s.parms["t" ]["value"]
            r = s.parms["r" ]["value"]
            p = s.parms["p" ]["value"]
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

    def vp_arr_update(s):
        s.v_log("vp_arr_update", "func")
        vp_arr      = list(s.vwr.viewports())
        vp_arr.reverse()
        vp_name_arr = []
        for vp in vp_arr:
            if vp.type() == hou.geometryViewportType.Perspective: vp_name_arr.append("main")
            else: vp_name_arr.append(vp.name())
        vp_name_arr.append("non-main")
        [s.v_log(vp_name_arr, "normal")]
        s.vp_name_arr = vp_name_arr
        s.vp_name     = vp_name_arr[0]
        s.layout      = str(s.vwr.viewportLayout()).split(".")[-1]

    def vp_focus(s):
        s.v_log("vp_focus", "func")

    def vp_get(s):
        s.v_log("vp_get", "func")
        if s.vp_name == "main": 
            return [s.vwr.findViewport("persp1")]
        elif s.vp_name == "non-main":
            vp_arr = []
            for vp in s.vwr.viewports():
                if vp.name() != "persp1":
                    vp_arr.append(vp)
            vp_arr.reverse()
            return vp_arr
        else:
            return [s.vwr.findViewport(s.vp_name)]

    def vp_layout_set(s):
        s.v_log("vp_layout_set", "func")
        s.vwr.setViewportLayout(eval("hou.geometryViewportLayout." + s.layout))

    def vp_swap(s):
        s.v_log("vp_swap", "func")
        vp_arr = s.vwr.viewports()
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
        vp = s.vwr.findViewport(vp_name)
        if   code == "persp" : vp.changeType(hou.geometryViewportType.Perspective)
        elif code == "top"   : vp.changeType(hou.geometryViewportType.Top)
        elif code == "bottom": vp.changeType(hou.geometryViewportType.Bottom)
        elif code == "front" : vp.changeType(hou.geometryViewportType.Front)
        elif code == "back"  : vp.changeType(hou.geometryViewportType.Back)
        elif code == "right" : vp.changeType(hou.geometryViewportType.Right)
        elif code == "left"  : vp.changeType(hou.geometryViewportType.Left)

    def v_log(s, message, level):
        if   level == "normal": s.log(message)
        elif level == "func"  : s.log(message, severity=hou.severityType.ImportantMessage)

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
        s.vp    = s.vwr.selectedViewport()
        s.parms = kwargs["state_parms"]
        # vp/cam
        s.vp_arr_update()
        s.cam_init()
        # parms
        s.init_parms()
        # hud
        s.v_log(s.layout, "normal")
        s.hud_update()
        s.init_settings()

    def onKeyEvent(s, kwargs):
        s.v_log_separator()
        s.v_log("onKeyEvent", "func")
        key = kwargs["ui_event"].device().keyString()
        s.v_log(key, "normal")
        # prev mode
        if key == "Shift+m":
            s.hud_prev_mode()
            return True
        # navigate
        elif key[-1] in ("h", "j", "k", "l"):
            if   s.mode == "nav"  : s.cam_xform(key)
            elif s.mode == "ctrl" : s.hud_change_ctrl(key)
            elif s.mode == "delta": s.hud_change_delta(key)
            elif s.mode == "focus": s.hud_change_focus(key)
            return True
        # next mode
        elif key == "m":
            s.hud_next_mode()
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
        if   action == "pvt_to_ray"     : s.cam_move_pvt("ray")
        elif action == "pvt_to_camera"  : s.cam_move_pvt("camera")
        elif action == "pvt_to_centroid": s.cam_move_pvt("centroid")
        elif action == "pvt_to_origin"  : s.cam_move_pvt("origin")
        # frame (?)
        elif action == "geo_frame"      : s.geo_frame()
        # adjust cam
        elif action == "cam_reset"      : s.cam_reset()
        elif action == "cam_fit_aspect" : s.cam_fit_aspect()
        elif action == "cam_to_state"   : s.cam_to_state()
        elif action == "toggle_bbx"     : s.toggle_bbox(kwargs, action)
        # axis
        elif action == "show_all_axes"  : s.drawable_update_axis(kwargs, "show_all")
        elif action == "hide_all_axes"  : s.drawable_update_axis(kwargs, "hide_all")
        elif action == "x_axis"         : s.drawable_update_axis(kwargs, "x")
        elif action == "y_axis"         : s.drawable_update_axis(kwargs, "y")
        elif action == "z_axis"         : s.drawable_update_axis(kwargs, "z")
        # vw Menu
        elif action == "vp_swap"     : s.vp_swap()
        # test menu
        elif action == "vp_arr_update"  : s.vp_arr_update()
        # print menu
        elif action == "print_cam_vals" : s.print("cam_vals")
        elif action == "print_centroid" : s.print("centroid")
        elif action == "print_kwargs"   : s.print_kwargs(kwargs)
        elif action == "print_vp"       : s.print("vp")

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
        if   pn == "axis_size": updates = (1, 0, 0, 0, 0)
        elif pn == "dist":      updates = (0, 1, 1, 1, 1)
        elif pn == "tr":        updates = (0, 1, 1, 1, 1)
        elif pn == "rot":       updates = (0, 1, 1, 1, 1)
        elif pn == "pvt":       updates = (0, 1, 1, 1, 1)
        elif pn == "pvt_rot":   updates = (0, 1, 1, 1, 1)
        elif pn == "tru_pvt":  updates = (0, 1, 1, 1, 1)
        if updates[0]: s.drawable_update_axis()
        if updates[1]: s.cam_update()
        if updates[2]: s.cam_update()
        if updates[3]: s.drawable_update_pvt()
        if updates[4]: s.drawable_update_pvt()

def make_menu(template):
    menu = hou.ViewerStateMenu("keycam_menu", "keycam_menu")
    menu.addActionItem("pvt_to_ray"     , "pvt_to_ray")
    menu.addActionItem("pvt_to_cam"     , "pvt_to_cam")
    menu.addActionItem("pvt_to_centroid", "pvt_to_centroid")
    menu.addActionItem("pvt_to_origin"  , "pvt_to_origin")
    menu.addSeparator()
    menu.addActionItem("cam_reset"      , "cam_reset")
    menu.addActionItem("cam_fit_aspect" , "cam_fit_aspect")
    menu.addActionItem("geo_frame"      , "geo_frame")
    menu.addActionItem("swap_vp"        , "swap_vp")
    menu.addSeparator()
    menu.addActionItem("show_all_axes"  , "show_all_axes")
    menu.addActionItem("hide_all_axes"  , "hide_all_axes")
    menu.addToggleItem("x_axis"         , "x_axis", 1)
    menu.addToggleItem("y_axis"         , "y_axis", 1)
    menu.addToggleItem("z_axis"         , "z_axis", 1)
    menu.addToggleItem("toggle_bbox"    , "toggle_bbox", 0)
    menu.addSeparator()
    menu.addActionItem("print_cam_vals" , "print_cam_vals")
    menu.addActionItem("print_kwargs"   , "print_kwargs")
    menu.addActionItem("print_centroid" , "print_centroid")
    menu.addActionItem("print_vp"       , "print_vp")
    menu.addSeparator()
    menu.addActionItem("cam_to_state"   , "cam_to_state")
    menu.addActionItem("vp_arr_update"  , "vp_arr_update")
    template.bindMenu(menu)

def make_parameters(template):
    t = template
    ptt = hou.parmTemplateType
    t.bindParameter(ptt.Float,     "axis_size", "axis_size", default_value=2.0, toolbox=False)
    t.bindParameter(ptt.Separator, "sep0",      toolbox=False)
    t.bindParameter(ptt.Float,     "dist",      "dist",      default_value=10.0)
    t.bindParameter(ptt.Float,     "ow",        "ow",        default_value=10.0)
    t.bindParameter(ptt.Separator, "sep1",      toolbox=False)
    t.bindParameter(ptt.Float,     "tr",        "tr",        num_components=3,  toolbox=False)
    t.bindParameter(ptt.Float,     "rot",       "rot",       num_components=3,  toolbox=False)
    t.bindParameter(ptt.Float,     "pvt",       "pvt",       num_components=3,  toolbox=False)
    t.bindParameter(ptt.Float,     "pvt_rot",   "pvt_rot",   num_components=3,  toolbox=False)
    t.bindParameter(ptt.Separator, "sep2",      toolbox=False)
    t.bindParameter(ptt.Float,     "up",        "up",        num_components=3,  toolbox=False)
    t.bindParameter(ptt.Float,     "tru_pvt",   "tru_pvt",   num_components=3,  toolbox=False)

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
