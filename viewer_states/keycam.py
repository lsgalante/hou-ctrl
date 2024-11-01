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
            {"id"  : "xform_mode"  , "label": "xform_mode"              },
            {"id"  : "xform_mode_g", "type" : "choicegraph", "count": 2 },
            {"id"  : "zoom_mode"   , "label": "zoom_mode"               },
            {"id"  : "zoom_mode_g" , "type" : "choicegraph", "count": 3 },
            {"id"  : "proj"        , "label": "projection" , "count": 2 },
            {"id"  : "proj_g"      , "type" : "choicegraph", "count": 2 },
            {"id"  : "target"      , "label": "target"                  },
            {"id"  : "target_g"    , "type" : "choicegraph", "count": 2 },
            {"id"  : "vp_name"     , "label": "vp"                      },
            {"id"  : "vp_name_g"   , "type" : "choicegraph", "count": 4 },
            {"id"  : "layout"      , "label": "layout"                  },
            {"id"  : "layout_g"    , "type" : "choicegraph", "count": 2 },
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
            {"id"  : "ow"       , "label": "ortho_width_delta"                  },
            {"id"  : "clip"     , "label": "clip_delta"                         }
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
        s.state_name     = state_name
        s.axes           = [1, 1, 1]
        s.ctrl_arr       = ("xform_mode", "zoom_mode", "proj", "target", "vp_name", "layout")
        s.ctrl           = "xform_mode"
        s.focus_attr     = "partition"
        s.focus_arr      = ("attribute", "focus")
        s.focus_idx      = 0
        s.focus_sel      = "attribute"
        s.layout_arr     = ("quadbottomsplit", "single")
        s.layout         = "single"
        s.mode_arr       = ("nav", "ctrl", "delta", "vis", "focus")
        s.mode           = "nav"
        s.proj_arr       = ("ortho", "persp")
        s.proj           = "ortho"
        s.reset_on_init  = 1
        s.target_arr     = ("cam", "pivot")
        s.target         = "cam"
        s.vp_name_arr    = ()
        s.vp_name        = ""
        s.vw_arr         = ("persp", "top", "bottom", "front", "back", "right", "left")
        s.vwr            = scene_viewer
        s.xform_mode     = "rot"
        s.xform_mode_arr = ("rot", "tr")
        s.zoom_mode      = "ow"
        s.zoom_mode_arr  = ("ow", "dist", "clip")

        s.unit_dict={
            "axis_size": 4,
            "rot"      : 7.5,
            "tr"       : 1,
            "ow"       : 1,
            "dist"     : 1,
            "clip"     : 2
        }

        s.delta_dict={
            "val_arr"  : ("axis_size", "rot", "tr", "dist", "ow", "clip"),
            "val"      : "axis_size",
            "axis_size": s.unit_dict["axis_size"],
            "rot"      : s.unit_dict["rot"],
            "tr"       : s.unit_dict["tr"],
            "ow"       : s.unit_dict["ow"],
            "dist"     : s.unit_dict["dist"],
            "clip"     : s.unit_dict["clip"]
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
        s.v_log("cam_fit_aspect", "important")
        cam = s.cam
        vp = s.vwr.findViewport(s.vp_name)
        size =  vp.size()
        cam.parm("resx").set(1000)
        cam.parm("resy").set(1000)
        ratio = size[2] / size[3]
        cam.parm("aspect").set(ratio)

    def cam_from_state(s):
        s.v_log("cam_from_state", "important")
        x=1

    def cam_get_dir(s):
        s.v_log("cam_get_dir", "important")
        sp =      s.state_parms
        tru_pvt = sp["tru_pvt"]["value"]
        tr =      sp["tr"]["value"]
        s.v_log(hou.Vector3(tru_pvt) - hou.Vector3(tr), "normal")
        return

    def cam_get_dist(s):
        s.v_log("cam_get_dist", "important")
        dist = s.state_parms["dist"]["value"]
        return dist

    def cam_get_len(s):
        s.v_log("cam_get_len", "important")
        sp =  s.state_parms
        tr =  sp["tr"]["value"]
        pvt = sp["pvt"]["value"]
        len = tr[2]
        return len

    def cam_get_xform(s):
        sp = s.state_parms
        self.v_log("cam_get_xform", "important")
        r = sp["r"]["value"]
        return r

    def cam_init(s):
        s.v_log("cam_init", "important")
        vp = s.vwr.findViewport(s.vp_name)
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
        vp.lockCameraToView(0)

    def cam_move_pvt(s):
        s.v_log("cam_move_pvt", "important")
        sp =     s.state_parms
        target = s.nav_dict["target"]
        if target == "cam":
            tr = sp["tr"]["value"]
            sp["tru_pvt"]["value"] = list(tr)
        elif target == "centroid":
            centroid = s.geo_get_centroid()
        elif target == "origin":
            sp["tr"]["value"] =      [0, 0, s.cam_get_dist()]
            sp["rot"]["value"] =     [45, 45, 0]
            sp["pvt"]["value"] =     [0, 0, -s.cam_get_dist()]
            sp["pvt_rot"]["value"] = [0, 0, 0]
            sp["tru_pvt"]["value"] = [0, 0, 0]
            sp["ow"]["value"] =      10
        elif target == "ray":
            x=1
        s.cam_update()
        s.drawable_update_pvt()
        s.drawable_update_ray()

    def cam_next_proj(s):
        s.v_log("cam_next_proj", "important")
        cam = s.cam
        proj_parm = cam.parm("projection")
        proj = proj_parm.evalAsString() 
        if   proj == "ortho":       proj_parm.set("perspective")
        elif proj == "perspective": proj_parm.set("ortho")

    def cam_proj_update(s):
        s.v_log("cam_proj_update", "important")
        cam = s.cam
        proj_parm = cam.parm("projection")
        if   s.proj == "ortho": proj_parm.set("ortho")
        elif s.proj == "persp": proj_parm.set("perspective")
        s.geo_frame()

    def cam_reset(s):
        s.v_log("cam_reset", "important")
        dist = s.cam_get_dist()
        sp =   s.state_parms
        sp["tr"]["value"] =      [0, 0, dist]
        sp["rot"]["value"] =     [315, 45, 0]
        sp["pvt"]["value"] =     [0, 0, -dist]
        sp["pvt_rot"]["value"] = [0, 0, 0]
        sp["tru_pvt"]["value"] = [0, 0, 0]
        sp["ow"]["value"] =      10
        s.cam_update()
        s.drawable_update_pvt()
        s.drawable_update_ray()

    def cam_rot(s, key):
        s.v_log("cam_rot", "important")
        dd = s.delta_dict
        sp = s.state_parms
        rot = list(sp["rot"]["value"])
        rot_delta = dd["rot"]
        if   key == "h": rot[1] = (rot[1] + rot_delta) % 360
        elif key == "j": rot[0] = (rot[0] - rot_delta) % 360
        elif key == "k": rot[0] = (rot[0] + rot_delta) % 360
        elif key == "l": rot[1] = (rot[1] - rot_delta) % 360
        sp["rot"]["value"] = rot

    def cam_to_state(s):
        s.v_log("cam_to_state", "important")
        cam = s.cam
        sp = s.state_parms
        sp["tr"]["value"] =      list(cam.evalParmTuple("t"))
        sp["pvt"]["value"] =     list(cam.evalParmTuple("p"))
        sp["rot"]["value"] =     list(cam.evalParmTuple("r"))
        sp["pvt_rot"]["value"] = list(cam.evalParmTuple("pr"))
        sp["ow"]["value"] =      cam.evalParm("orthowidth")

    def cam_translate(s, key):
        s.v_log("cam_translate", "important")
        dd = s.delta_dict
        sp = s.state_parms
        # tru_pvt = list(sp["tru_pvt"]["value"])
        s.cam_get_dir()
        pvt =      list(sp["pvt"]["value"])
        tr_delta = dd["tr"]
        if   key == "h": pvt[0] = pvt[0] - tr_delta
        elif key == "j": pvt[1] = pvt[1] - tr_delta
        elif key == "k": pvt[1] = pvt[1] + tr_delta
        elif key == "l": pvt[0] = pvt[0] + tr_delta
        sp["pvt"]["value"] = pvt

    def cam_update(s):
        s.v_log("cam_update", "important")
        sp = s.state_parms
        # convert tru_pivot
        tru_pvt = 1
        if tru_pvt:
            tru_pvt = sp["tru_pvt"]["value"]
            dist    = sp["dist"]["value"]
            sp["tr"]["value"][0]  = tru_pvt[0]
            sp["tr"]["value"][1]  = tru_pvt[1]
            sp["tr"]["value"][2]  = dist
            sp["pvt"]["value"][0] = 0
            sp["pvt"]["value"][1] = 0
            sp["pvt"]["value"][2] = tru_pvt[2] - dist
        # transfer state parameters to camera
        s.cam.parmTuple("r").set(sp["rot"]["value"])
        s.cam.parmTuple("t").set(sp["tr"]["value"])
        s.cam.parmTuple("p").set(sp["pvt"]["value"])
        s.cam.parmTuple("pr").set(sp["pvt_rot"]["value"])
        s.cam.parm("orthowidth").set(sp["ow"]["value"])

    def cam_xform(s, key):
        s.v_log("cam_xform", "important")
        # gather vars
        vp = s.vwr.findViewport(s.vp_name)
        type = vp.type()
        if "persp" in s.vp_name:
            if key in ("Shift+h", "Shift+j", "Shift+k", "Shift+l"):
                if   s.xform_mode == "rot": s.cam_tr(key[-1])
                elif s.xform_mode == "tr" : s.cam_rot(key[-1])
            elif key in ("h", "j", "k", "l"):
                if   s.xform_mode == "rot": s.cam_rot(key)
                elif s.xform_mode == "tr" : s.cam_tr(key)
            s.cam_update()
            s.drawable_update_pvt()
            s.drawable_update_ray()
        elif vp == "top1"   : s.cam_xform_flat(key, "top")
        elif vp == "bottom1": s.cam_xform_flat(key, "bottom")
        elif vp == "front1" : s.cam_xform_flat(key, "front")
        elif vp == "back1"  : s.cam_xform_flat(key, "back")
        elif vp == "right1" : s.cam_xform_flat(key, "right")
        elif vp == "left1"  : s.cam_xform_flat(key, "left")

    def cam_xform_flat(s, key, vw_type):
        s.v_log("cam_xform_flat", "important")
        vp = s.vwr.findViewport(s.vp_name)
        idx_arr       = [0, 0]
        if   vw_type == "top"   : idx_arr = [0, 2]
        elif vw_type == "bottom": idx_arr = [2, 0]
        elif vw_type == "front" : idx_arr = [0, 1]
        elif vw_type == "back"  : idx_arr = [1, 0]
        elif vw_type == "right" : idx_arr = [2, 1]
        elif vw_type == "left"  : idx_arr = [1, 2]
        cam = vp.defaultCamera() # pyright: ignore
        t  = list( cam.translation() )
        ti = s.unit_dict["tr"]
        if   key == "h": t[idx_arr[0]] += ti
        elif key == "j": t[idx_arr[1]] += ti
        elif key == "k": t[idx_arr[1]] -= ti
        elif key == "l": t[idx_arr[0]] -= ti
        cam.setTranslation(t)

    def cam_xform_update(s):
        s.v_log("cam_xform_update", "important")

    def cam_zoom(s, key):
        s.v_log("cam_zoom", "important")
        dd = s.delta_dict
        sp = s.state_parms
        proj = s.proj
        ow_delta =   dd["ow"]
        dist_delta = dd["dist"]
        if s.proj == "persp":
            #if   key == "Shift+-":
            #elif key == "Shift+=":
            if   key == "=": sp["dist"]["value"] -= dist_delta
            elif key == "-": sp["dist"]["value"] += dist_delta
        elif s.proj == "ortho":
            if s.zoom_mode == "ow":
                #if   key == "Shift+-":
                #elif key == "Shift+=":
                if   key == "-": sp["ow"]["value"] += ow_delta
                elif key == "=": sp["ow"]["value"] -= ow_delta
            elif s.zoom_mode == "dist":
                #if   key == "Shift+-":
                #elif key == "Shift+=":
                if   key == "=": sp["dist"]["value"] += dist_delta
                elif key == "-": sp["dist"]["value"] -= dist_delta
            elif s.zoom_mode == "clip":
                return
        s.cam_update()
        s.drawable_update_pvt()
        s.drawable_update_ray()

    def drawable_toggle_bbx(s, kwargs, action):
        s.v_log("drawable_toggle_bbx", "important")
        enabled = kwargs["toggle_bbx"]
        s.drawable_update_bbx()

    def drawable_update_axis(s, kwargs, code):
        s.v_log("drawable_update_axis", "important")
        # change state
        if   code == "show_all": s.axes    = [1, 1, 1]
        elif code == "hide_all": s.axes    = [0, 0, 0]
        elif code == "x"       : s.axes[0] = kwargs["x_axis"]
        elif code == "y"       : s.axes[1] = kwargs["y_axis"]
        elif code == "z"       : s.axes[2] = kwargs["z_axis"]
        # draw them
        dd = s.delta_dict
        size = dd["axis_size"]
        geo = hou.Geometry()
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
                prim = geo.createPolygon(is_closed=False)
                prim.addVertex(pts[0])
                prim.addVertex(pts[1])
        s.drawable_axis.setGeometry(geo)
        s.drawable_axis.setParams({"fade_factor": 0.0})

    def drawable_update_bbox(self):
        s.v_log("drawable_update_bbox", "important")
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
        s.v_log("drawable_update_pvt", "important")
        sp =          s.state_parms
        rot =         list(sp["rot"]["value"])
        tr =          list(sp["tr"]["value"])
        pvt =         list(sp["pvt"]["value"])
        ow =          sp["ow"]["value"]
        scale =       ow * 0.0075
        P =           hou.Vector3(pvt) + hou.Vector3(tr)
        geo =         hou.Geometry()
        circle_verb = hou.sopNodeTypeCategory().nodeVerb("circle")
        circle_verb.setParms({"type": 1, "r": rot, "t": P, "scale": scale})
        circle_verb.execute(geo, [])
        s.drawable_pvt.setGeometry(geo)
        s.drawable_pvt.setParams({
            "color1": hou.Vector4(0.0, 0.0, 1, 1),
            "fade_factor": 1.0
        })

    def drawable_update_ray(s):
        s.v_log("drawable_update_ray", "important")
        sp = s.state_parms
        tr =       sp["tr"]["value"]
        rot =      sp["rot"]["value"]
        pvt =      sp["pvt"]["value"]
        tru_pvt =  sp["tru_pvt"]["value"]
        rot =      hou.hmath.buildRotate(rot)
        cam_P =    hou.Vector3(0, 0, s.cam_get_len()) * rot
        cam_P +=   hou.Vector3(tru_pvt[0], tru_pvt[1], tru_pvt[2])
        pvt_P =    hou.Vector3(tr) + hou.Vector3(pvt)
        geo =      hou.Geometry()
        pts =      geo.createPoints((cam_P, pvt_P))
        prim =     geo.createPolygon()
        prim.addVertex(pts[0])
        prim.addVertex(pts[1])
        s.drawable_ray.setGeometry(geo)

    def geo_frame(s):
        s.v_log("geo_frame", "important")
        [ vp.frameAll() for vp in s.vwr.viewports() ]
        s.cam_to_state()
        s.drawable_update_pvt()

    def geo_get_centroid(s):
        s.v_log("geo_get_centroid", "important")
        geo = s.geo_get()
        result_geo = hou.Geometry()
        centroid_verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        centroid_verb.setParms({"partitiontype": 2})
        centroid_verb.execute(result_geo, [geo])
        pt = result_geo.point(0)
        centroid = pt.position()
        return centroid

    def geo_get_extrema(s):
        s.v_log("geo_get_extrema", "important")
        geo = s.geo_get()
        bbx = geo.boundingBox()

    def geo_get(s):
        s.v_log("geo_get", "important")
        display_node = s.vwr.pwd().displayNode()
        geo = display_node.geometry()
        return geo

    def hud_change_focus(s, key):
        s.v_log("hud_change_focus", "important")
        if   key == "j": s.focus_sel = s.list_next(s.focus_arr, s.focus_sel)
        elif key == "k": s.focus_sel = s.list_prev(s.focus_arr, s.focus_sel) 
        elif key in ("h", "l"):
            attr = hou.ui.readInput("focus_attr", buttons=("OK", "Cancel"), initial_contents=s.focus_attr)
            if attr[0] == 0: s.focus_attr = attr[1]
        s.hud_update("focus")

    def hud_change_ctrl(s, key):
        s.v_log("hud_change_ctrl", "important")
        # select ctrl
        if key in ("j", "k"):
            ctrl_idx = s.ctrl_arr.index(s.ctrl)
            if   key == "j": ctrl_idx += 1
            elif key == "k": ctrl_idx -= 1
            ctrl_idx %= len(s.ctrl_arr)
            s.ctrl = s.ctrl_arr[ctrl_idx]
        # change val
        elif key in ("h", "l"):
            val = getattr(s, s.ctrl)
            val_arr = getattr(s, s.ctrl + "_arr")
            val_idx = val_arr.index(val)
            if   key == "h": val_idx -= 1
            elif key == "l": val_idx += 1
            val_idx %= len(val_arr)
            setattr(s, s.ctrl, val_arr[val_idx])
        if   s.ctrl == "proj":   s.cam_proj_update()
        elif s.ctrl == "layout": s.vp_layout_set()
        s.hud_update(s.mode)

    def hud_change_val(s, key):
        s.v_log("hud_change_val", "important")
        dd =      s.delta_dict
        ud =      s.unit_dict
        val =     vd["val"]
        val_arr = vd["val_arr"]
        if   key == "h": dd[val] -=  ud[val]
        elif key == "j": vd["val"] = s.list_prev(val_arr, val)
        elif key == "k": vd["val"] = s.list_next(val_arr, val)
        elif key == "l": vd[val] +=  dd[val]
        s.hud_update("val_dict")

    def hud_init(s):
        s.v_log("hud_init", "important")
        s.vwr.hudInfo(template=s.HUD_NAV)
        updates = {
            "mode"        : {"value": s.mode},
            "mode_g"      : {"value": s.mode_arr.index(s.mode)},
            "xform_mode"  : {"value": s.xform_mode},
            "xform_mode_g": {"value": s.xform_mode_arr.index(s.xform_mode)},
            "zoom_mode"   : {"value": s.zoom_mode},
            "zoom_mode_g" : {"value": s.zoom_mode_arr.index(s.zoom_mode)},
            "proj"        : {"value": s.proj},
            "proj_g"      : {"value": s.proj_arr.index(s.proj)},
            "target"      : {"value": s.target},
            "target_g"    : {"value": s.target_arr.index(s.target)},
            "vp_name"     : {"value": s.vp_name},
            "vp_name_g"   : {"value": s.vp_name_arr.index(s.vp_name)},
            "layout"      : {"value": s.layout},
            "layout_g"    : {"value": s.layout_arr.index(s.layout)}
        }
        s.vwr.hudInfo(hud_values=updates)

    def hud_next_mode(s):
        s.v_log("hud_next_mode", "important")
        idx = s.mode_arr.index(s.mode)
        idx += 1
        idx %= len(s.mode_arr)
        new_mode = s.mode_arr[idx]
        s.mode = new_mode
        s.hud_update(new_mode)

    def hud_prev_mode(s):
        s.v_log("hud_prev_mode", "important")
        idx = s.mode_arr.index(s.mode)
        idx -= 1
        idx %= len(s.mode_arr)
        new_mode = s.mode_arr[idx]
        s.mode = new_mode
        s.hud_update(new_mode)

    def hud_update(s, hud):
        s.v_log("hud_update", "important")
        dd = s.delta_dict
        if hud == "nav":
            s.vwr.hudInfo(template=s.HUD_NAV)
            updates={
                "mode"        : {"value": s.mode},
                "mode_g"      : {"value": s.mode_arr.index(s.mode)},
                "xform_mode"  : {"value": s.xform_mode},
                "xform_mode_g": {"value": s.xform_mode_arr.index(s.xform_mode)},
                "zoom_mode"   : {"value": s.zoom_mode},
                "zoom_mode_g" : {"value": s.zoom_mode_arr.index(s.zoom_mode)},
                "proj"        : {"value": s.proj},
                "proj_g"      : {"value": s.proj_arr.index(s.proj)},
                "target"      : {"value": s.target},
                "target_g"    : {"value": s.target_arr.index(s.target)},
                "vp_name"     : {"value": s.vp_name},
                "vp_name_g"   : {"value": s.vp_name_arr.index(s.vp_name)},
                "layout"      : {"value": s.layout},
                "layout_g"    : {"value": s.layout_arr.index(s.layout)}
            }
            s.vwr.hudInfo(hud_values=updates)

        elif hud == "ctrl":
            s.v_log(s.zoom_mode, "normal")
            s.vwr.hudInfo(template=s.HUD_NAV)
            updates={
                "mode"        : {"value": s.mode},
                "mode_g"      : {"value": s.mode_arr.index(s.mode)},
                "xform_mode"  : {"value": s.xform_mode},
                "xform_mode_g": {"value": s.xform_mode_arr.index(s.xform_mode)},
                "zoom_mode"   : {"value": s.zoom_mode},
                "zoom_mode_g" : {"value": s.zoom_mode_arr.index(s.zoom_mode)},
                "proj"        : {"value": s.proj},
                "proj_g"      : {"value": s.proj_arr.index(s.proj)},
                "target"      : {"value": s.target},
                "target_g"    : {"value": s.target_arr.index(s.target)},
                "vp_name"     : {"value": s.vp_name},
                "vp_name_g"   : {"value": s.vp_name_arr.index(s.vp_name)},
                "layout"      : {"value": s.layout},
                "layout_g"    : {"value": s.layout_arr.index(s.layout)}
            }
            updates[s.ctrl]["value"] = "[" + updates[s.ctrl]["value"] + "]"
            s.vwr.hudInfo(hud_values=updates)

        elif hud == "delta":
            s.vwr.hudInfo(template=s.HUD_DELTA)
            updates={
                "mode"     : {"value": s.mode},
                "mode_g"   : {"value": s.mode_arr.index(s.mode)},
                "axis_size": {"value": str(dd["axis_size"])},
                "rot"      : {"value": str(dd["rot"])},
                "tr"       : {"value": str(dd["tr"])},
                "ow"       : {"value": str(dd["ow"])},
                "dist"     : {"value": str(dd["dist"])},
                "clip"     : {"value": str(dd["clip"])}
            }
            updates[dd["val"]]["value"] = "[" + updates[dd["val"]]["value"] + "]"
            s.vwr.hudInfo(hud_values=updates)
        
        elif hud == "vis":
            s.vwr.hudInfo(template=s.HUD_VIS)
            updates={
            }
            s.vwr.hudInfo(hud_values=updates)

        elif hud == "focus":
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
        s.v_log("init_parms", "important")
        cam = s.cam
        sp = s.state_parms
        sp["tr"]["value"] =      list(cam.evalParmTuple("t"))
        sp["pvt"]["value"] =     list(cam.evalParmTuple("p"))
        sp["rot"]["value"] =     list(cam.evalParmTuple("r"))
        sp["pvt_rot"]["value"] = list(cam.evalParmTuple("pr"))
        sp["ow"]["value"] =      cam.evalParm("orthowidth")

    def list_next(s, list, sel):
        idx = list.index(sel)
        idx = (idx + 1) % len(list)
        return idx

    def list_prev(s, list, sel):
        idx = list.index(sel)
        idx = (idx - 1) % len(list)
        return idx

    def print(s, key):
        s.v_log("print", "important")
        sp = s.state_parms
        if key == "cam_vals":
            t = sp["t"]["value"]
            r = sp["r"]["value"]
            p = sp["p"]["value"]
            p = sp["pr"]["value"]
            s.v_log("r:\n", r, "t:\n", t, "p:\n", p, "pr:\n", pr, "normal")
        elif key == "centroid":
            s.v_log(s.geo_get_centroid(), "normal")
        elif key == "hud_state":
            x=1
        elif key == "vp":
            s.v_log(s.vp, "normal")

    def print_kwargs(s, kwargs):
        s.v_log("print_kwargs", "important")
        s.v_log_separator()
        ui_event = str(kwargs["ui_event"])
        ui_event = ui_event.replace("\\n", "\n")
        del kwargs["ui_event"]
        s.v_log_separator()
        s.v_log(ui_event, "normal")

    def vp_arr_update(s):
        s.v_log("vp_arr_update", "important")
        vp_arr = list(s.vwr.viewports())
        vp_arr.reverse()
        vp_name_arr = [vp.name() for vp in vp_arr]
        s.vp_name_arr = vp_name_arr
        s.vp_name = vp_name_arr[0]

    def vp_layout_init(s):
        s.v_log("vp_layout_init", "important")
        gvl = hou.geometryViewportLayout
        layout = s.vwr.viewportLayout()
        if   layout == gvl.Single         : s.layout = "single"
        elif layout == gvl.QuadBottomSplit: s.layout = "quadbottomsplit"

    def vp_layout_set(s):
        s.v_log("vp_layout_set", "important")
        gvl = hou.geometryViewportLayout
        if   s.layout == "quadbottomsplit": s.vwr.setViewportLayout(gvl.QuadBottomSplit)
        elif s.layout == "single"         : s.vwr.setViewportLayout(gvl.Single)
        s.cam_fit_aspect()

    def vp_swap(s):
        s.v_log("vp_swap", "important")
        vp_arr = s.vwr.viewports()
        vp_name_arr = [vp.name() for vp in vp_arr]
        vp_type_arr = [vp.type() for vp in vp_arr]

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
        s.v_log("vp_type_set", "important")
        vp_name = s.vp
        vp = s.vwr.findViewport(vp_name)
        if   code == "persp":
            vp.changeType(hou.geometryViewportType.Perspective)
        elif code == "top":
            vp.changeType(hou.geometryViewportType.Top)
        elif code == "bottom":
            vp.changeType(hou.geometryViewportType.Bottom)
        elif code == "front":
            vp.changeType(hou.geometryViewportType.Front)
        elif code == "back":
            vp.changeType(hou.geometryViewportType.Back)
        elif code == "right":
            vp.changeType(hou.geometryViewportType.Right)
        elif code == "left":
            vp.changeType(hou.geometryViewportType.Left)
        

    def v_log(s, message, level):
        if   level == "normal"   : s.log(message)
        elif level == "important": s.log(message, severity=hou.severityType.ImportantMessage)

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
        s.v_log("onGenerate", "important")
        # prevent exiting state when selecting nodes
        kwargs["state_flags"]["exit_on_node_select"] = False
        # init vars
        s.vp    = s.vwr.selectedViewport()
        s.state_parms = kwargs["state_parms"]
        # viewports
        s.vp_arr_update()
        s.vp_layout_init()
        # cam
        s.cam_init()
        s.cam_fit_aspect()
        # parms
        s.init_parms()
        # hud
        s.hud_init()
        if s.reset_on_init:
            s.cam_reset()

    def onKeyEvent(s, kwargs):
        s.v_log_separator()
        s.v_log("onKeyEvent", "important")
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
        s.v_log("onMenuAction", "important")
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
