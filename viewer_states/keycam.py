import hou
import pprint
import time
import viewerstate.utils as su

class State(object):
    HUD_LAYOUT={
        "title": "layout",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},
            
            {"id": "divider", "type":  "divider"},
            
            {"id": "hud", "label": "hud"},
            {"id": "hud_g", "type": "choicegraph"},
            
            {"id": "layout", "label": "layout"},
            {"id": "layout_g", "type": "choicegraph"},
            
            {"id": "viewport_index", "label": "viewport_index"},
            {"id": "viewport_index_g", "type": "choicegraph"},
            
            {"id": "set_view", "label": "set_view"},
            {"id": "set_view_g", "type": "choicegraph"}
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
            {"id": "mode" ,  "label": "mode", "key": "M"},
            {"id": "divider", "type": "divider"},
            
            {"id": "hud", "label": "hud"},
            {"id": "hud_g", "type" : "choicegraph"},
            
            {"id": "r", "label": "r_delta"},
            {"id": "t", "label": "t_delta"},
            
            {"id": "dist", "label": "dist_delta"},
            
            {"id": "ow", "label": "ow_delta"}
        ]
    }

    HUD_VIS={
        "title": "vis",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},
            {"id": "divider", "type": "divider"},
            
            {"id": "hud", "label": "hud"},          
            {"id": "hud_g", "type": "choicegraph"},
            
            {"id": "vis", "label": "vis"}
        ]
    }

    HUD_FOCUS={
        "title": "focus",
        "rows": [
            {"id": "mode", "label": "mode", "key": "M"},
            {"id": "divider", "type":  "divider"},
            
            {"id": "hud", "label": "hud"},
            {"id": "hud_g", "type":  "choicegraph"},
            
            # {"id": "attr", "label": "attr", "value": "partition"},
            
            {"id": "focus", "label": "focus", "value": 0},
            {"id": "focus_g", "type":  "choicegraph", "count": 10}
        ]
    }

    def __init__(self, state_name, scene_viewer):
        # General Variabls
        self.context = None
        self.huds = ("layout", "movement", "delta", "vis", "focus")
        self.hud = "layout"
        self.modes = ("camera", "settings")
        self.mode = "camera"
        self.sceneViewer = scene_viewer
        self.state_name = state_name

        # Camera Variables
        self.P_pivot = hou.Vector3(0, 0, 0)
        self.P_cam = hou.Vector3(0, 0, 0)
        self.r = hou.Vector3(0, 0, 0)
        self.local_x = hou.Vector3(1, 0, 0)
        self.local_y = hou.Vector3(0, 1, 0)
        self.local_z = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)
        
        # util dicts
        self.guides={
            "axis_size": 1,
            "axis_cam": 1,
            "axis_pivot": 0,
            "bbox": 0,
            "cam_geo": 1,
            "perim": 0,
            "pivot_2d": 0,
            "pivot_3d": 1,
            "ray": 1,
            "tie_axis_to_radius": 0
        }

        self.startup_vars={
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

        
        # HUD states
        
        self.layout_state={
            "controls": ("hud", "layout", "viewport_index", "set_view"),
            "control": "hud",
            
            # layouts: DoubleSide, DoubleStack, Quad, QuadBottomSplit, QuadLeftSplit, Single, TripleBottomSplit, TripleLeftSplit
            "layouts": ("Single", "DoubleSide", "TripleLeftSplit", "Quad"),
            "layout": "Single",

            "viewport_indexs": ("0"),
            "viewport_index": "0",

            "set_views": ("top", "bottom", "left", "right", "front", "back", "persp", "none"),
            "set_view": "persp"

        }
    
        self.movement_state={
            "controls": ("hud", "target"),
            "control": "hud",
            
            "target_arr": ("cam", "pivot"),
            "target": "cam"
        }

        self.delta_state={
            "controls": ("hud", "rot", "tr", "dist", "ow"),
            "control": "hud",
            
            "r": self.units["r"],
            "t": self.units["t"],
            "ow": self.units["ow"],
            "dist": self.units["dist"]
        }

        self.vis_state={
            "controls": ("hud"),
            "control": "hud",
            
            "vis_arr": ("test1", "test2", "test3"),
            "vis": "test1"
        }

        self.focus_state={
            "controls": ("hud", "attr", "focus"),
            "ctl": "hud",
            
            "focus_arr": ("test1", "test2", "test3"),
            "focus": "test1"
        }
        self.initGuides()

        
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
        self.guideText.draw(handle, {})

        
    def onGenerate(self, kwargs):
        # Prevent exiting the state when node selection is changed.
        kwargs["state_flags"]["exit_on_node_select"] = False
        self.parms = kwargs["state_parms"]
        #self.update_dict_layout()
        self.initCam()
        self.initParms()
        self.updateContext()
        self.updateHud()
        self.initSettings()
        self.camFrame()

        
    def onKeyEvent(self, kwargs):
        key = kwargs["ui_event"].device().keyString()
        self.log("keycam key press event: " + key)
        
        if key == "m":                # Toggle HUD mode.
            self.toggleMode()
            return True
        elif key == "o":              # Cycle projection type.
            self.toggleProjection()
            return True
        elif self.mode == "settings": # Navigate the HUD.
            self.hudNav(key)
            return True
        elif self.mode == "camera":   # Camera manipulation.
            
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
            
            viewport_index = self.layout_state["viewport_index"]
            layout = self.layout_state["layout"]

            if layout == "DoubleSide":
                viewport_index = (2, 3)[int(viewport_index)]
            elif layout == "DoubleStack":
                viewport_index = (3, 0)[int(viewport_index)]
            elif layout == "Quad":
                viewport_index = (2, 3, 1, 0)[int(viewport_index)]
            elif layout == "QuadBottomSplit":
                viewport_index = (3, 2, 1, 0)[int(viewport_index)]
            elif layout == "QuadLeftSplit":
                viewport_index = (2, 1, 0, 3)[int(viewport_index)]
            elif layout == "Single":
                viewport_index = 3
            elif layout == "TripleBottomSplit":
                viewport_index = (3, 1, 0)[int(viewport_index)]
            elif layout == "TripleLeftSplit":
                viewport_index = (2, 3, 1)[int(viewport_index)]


            viewports = list(self.sceneViewer.viewports())
            self.log("Viewport index: " + str(viewport_index))
            # print([viewport.type() for viewport in viewports])
            viewport = viewports[viewport_index]
            # viewport = self.getViewport()
            viewportType = viewport.type()
            self.log("Viewport type: " + str(viewportType))
            
            if viewportType == hou.geometryViewportType.Perspective: # Cam is node.
                if key == "Shift+h":   # Translate x down
                    self.camTranslate("x", -1)
                    return True
                elif key == "Shift+j": # Translate y down
                    self.camTranslate("y", -1)
                    return True
                elif key == "Shift+k": # Translate y up
                    self.camTranslate("y", 1)
                    return True
                elif key == "Shift+l": # Translate x up
                    self.camTranslate("x", 1)
                    return True
                elif key == "h":       # Rotate y down
                    self.camRotate("y", -15)
                    return True
                elif key == "j":       # Rotate x up
                    self.camRotate("x", 15)
                    return True
                elif key == "k":       # Rotate x down
                    self.camRotate("x", -15)
                    return True
                elif key == "l":       # Rotate y up
                    self.camRotate("y", 15)
                    return True
                elif key == "-":       # Zoom out
                    self.camZoom(1)
                    return True
                elif key == "=":       # Zoom in
                    self.camZoom(-1)
                    return True
                elif key == "Shift+-": # Ortho width up
                    self.ow += 1
                    return True
                elif key == "Shift+=": # Ortho width down
                    self.ow -= 1
                    return True
                elif key == "f":       # Frame
                    self.camFrame()
                    return True
                
                self.stateToCam()
                
            else: # Cam is default
                cam = viewport.defaultCamera()
                t = list(cam.translation())
                delta = self.units["t"]
                indices = [0, 0]

                if viewportType == hou.geometryViewportType.Top:
                    indices = [0, 1]
                elif viewportType == hou.geometryViewportType.Bottom:
                    indices = [2, 0]
                elif viewportType == hou.geometryViewportType.Front:
                    indices = [0, 1]
                elif viewportType == hou.geometryViewportType.Back:
                    indices = [1, 0]
                elif viewportType == hou.geometryViewportType.Right:
                    indices = [0, 1]
                elif viewportType == hou.geometryViewportType.Left:
                    indices = [1, 2]

                if key == "h":
                    t[indices[0]] += delta
                elif key == "j":
                    t[indices[1]] += delta
                elif key == "k":
                    t[indices[1]] -= delta
                elif key == "l":
                    t[indices[0]] -= delta
                elif key == "-":
                    cam.setOrthoWidth(cam.orthoWidth() + 1)
                elif key == "=":
                    cam.setOrthoWidth(cam.orthoWidth() - 1)
                cam.setTranslation(t)

        else:
            return False

        
    def onMenuAction(self, kwargs):
        item = kwargs["menu_item"]
        if item == "cam_frame":
            self.camFrame()
        elif item == "cam_reset":
            self.camReset()
        elif item == "viewport_frame":
            self.viewportFrame()
        elif item == "axis_cam":
            self.guides["axis_cam"] = kwargs["axis_cam"]
        elif item == "axis_pivot":
            self.guides["axis_pivot"] = kwargs["axis_pivot"]
        elif item == "perim":
            self.guides["perim"] = kwargs["perim"]
        elif item == "pivot_2d":
            self.guides["pivot_2d"] = kwargs["pivot_2d"]
        elif item == "pivot_3d":
            self.guides["pivot_3d"] = kwargs["pivot_3d"]
        elif item == "ray":
            self.guides["ray"] = kwargs["ray"]
        self.updateGuides()

        
    def onParmChangeEvent(self, kwargs):
        self.updateGuides()
        self.stateToCam()

        
    #############################
    # Array Traversal Functions #
    #############################

    
    def arrNext(self, arr, sel):
        index = arr.index(sel)
        index = (index + 1) % len(arr)
        return index

    
    def arrPrev(self, arr, sel):
        index = arr.index(sel)
        index = (index - 1) % len(arr)
        return index


    #################################
    # Camera Manipulation Functions #
    #################################

    
    def camFrame(self):
        centroid = self.getGeoCentroid()
        bbox = self.getGeoBbox()

        self.P_pivot = centroid
        self.P_cam = centroid
        self.ow = 10

        self.camZoom(6)
        self.stateToCam()

        
    def camMovePivot(self):
        target = self.nav_state["target"]
        if target == "cam":
            t = list(self.parms["t"]["value"])
        elif target == "centroid":
            centroid = self.getGeoCentroid()
        elif target == "origin":
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

        
    def camToState(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")

        
    def camReset(self):
        self.P_cam = hou.Vector3(0, 0, 0)
        self.P_pivot = hou.Vector3(0, 0, 0)
        self.r = hou.Vector3(0, 0, 0)
        self.local_x = hou.Vector3(1, 0, 0)
        self.local_y = hou.Vector3(0, 1, 0)
        self.local_z = hou.Vector3(0, 0, 1)
        self.global_x = hou.Vector3(1, 0, 0)
        self.global_y = hou.Vector3(0, 1, 0)
        self.global_z = hou.Vector3(0, 0, 1)
        self.stateToCam()
        self.updateGuides()

        
    def camRotate(self, axis_name, deg):
        axis = None
        if axis_name == "x":
            axis = self.local_x
            self.r[0] += deg
        elif axis_name == "y":
            axis = self.global_y
            self.r[1] += deg

        m = hou.hmath.buildRotateAboutAxis(axis, deg)

        self.P_cam -= self.P_pivot
        self.P_cam *= m
        self.P_cam += self.P_pivot
        self.local_x *= m
        self.local_y *= m
        self.local_z *= m
        self.stateToCam()

        
    def camTranslate(self, axis_name, amt):
        axis = None
        if axis_name == "x":
            axis = self.local_x
        elif axis_name == "y":
            axis = self.local_y

        move = axis * amt
        self.P_pivot += move
        self.P_cam += move
        self.stateToCam()

        
    def camZoom(self, amt):
        move = hou.Vector3(0, 0, 0)
        move = self.local_z * amt
        self.P_cam += move
        self.stateToCam()

        
    def frameDefault(self):
        viewports = self.sceneViewer.viewports()
        for viewport in viewports:
            cam = viewport.camera()
            # Is cam default or node.
            if cam == None:
                viewport.frameAll()
        self.camToState()


    def getGeo(self):
        context = self.context
        displayNode = None

        pwd = self.sceneViewer.pwd()
        print(pwd)
        print(pwd.type().name())

        if context == "dop":
            displayNode = pwd.displayNode()
        elif context == "lop":
            return None
        elif context == "obj":
            children = pwd.children()
            print(children)
            displayNode = children[0]
        elif context == "geo":
            displayNode = pwd.displayNode()

        return displayNode.geometry()
    
    def getGeoBbox(self):
        geo = self.getGeo()
        bbox = geo.boundingBox()
        return bbox

        
    def getGeoCentroid(self):
        geo_in = self.getGeo()
        geo_out = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(geo_out, [geo_in])
        pt = geo_out.point(0)
        centroid = pt.position()
        return centroid
    

    def getViewport(self):
        viewport_indexs = self.layout_state["viewport_indexs"]
        viewport_index = self.layout_state["viewport_index"]
        viewport_index = viewport_indexs.index(viewport_index)
        viewports = list(self.sceneViewer.viewports())
        viewports.reverse()
        viewport = viewports[viewport_index]
        return viewport

    
    def hudNav(self, key):
        # Source common variables.
        ctl_state = getattr(self, self.hud + "_state")
        ctl_state["huds"] = self.huds
        ctl_state["hud"] = self.hud
        ctl = ctl_state["ctl"]

        # Select control.
        if key in ("j", "k"):
            controls = ctl_state["controls"]
            index = controls.index(ctl)

            if key == "j":
                index += 1
            elif key == "k":
                index -= 1

            index %= len(controls)
            ctl = controls[index]
            ctl_state["ctl"] = ctl

        # Change control value.
        elif key in ("h", "l"):
            if ctl == "attr":
                self.setFocusAttr() 
            else:
                val_arr = ctl_state[ctl + "_arr"] 
                val = ctl_state[ctl]
                index = val_arr.index(val)

                if key == "h":
                    index -= 1
                elif key == "l":
                    index += 1 

                index %= len(val_arr)
                val = val_arr[index]
                ctl_state[ctl] = val

        # Update state .
        if ctl == "layout":
            self.setViewportLayout()
        elif ctl == "viewport_index":
            self.set_viewport()
        elif ctl == "set_view":
            self.setView()

        self.hud = ctl_state["hud"]
        self.updateHud()

        
    def initCam(self):
        viewports = list(self.sceneViewer.viewports())
        viewports.reverse()
        viewport = viewports[0]
        # Create keycam node if nonexistant.
        child_arr = [node.name() for node in hou.node("/obj").children()]
        if "keycam" not in child_arr:
            cam = hou.node("/obj").createNode("cam")
            cam.setName("keycam")
            cam.parm("xOrd").set(0)
        # Define vars.
        t = [0, 0, 0]
        r = [0, 0, 0]
        p = [0, 0, 0]
        ow = 1
        cam = viewport.camera()

        if cam == None: # Cam is default.
            cam = viewport.defaultCamera()
            t = cam.translation()
            r = cam.rotation()
            p = cam.pivot()
            ow = cam.orthoWidth()

        else: # Cam is node.
            t = cam.evalParmTuple("t")
            r = cam.evalParmTuple("r")
            p = cam.evalParmTuple("p")
            ow = cam.evalParm("orthowidth")
            
        self.cam = hou.node("/obj/keycam")
        viewport.setCamera(self.cam)
        viewport.lockCameraToView(self.startup_vars["lock_cam"])

        
    def initGuides(self):
        
        # axisCam
        self.guideAxisCam = hou.GeometryDrawable(
            scene_viewer=self.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axisCam")

        # axisPivot
        self.guideAxisPivot = hou.GeometryDrawable(
            scene_viewer=self.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="axisPivot",
            params={"color1": hou.Vector4((1, 1, 1, 0.5))})

        # bbox
        self.guideBbox = hou.GeometryDrawable(
            scene_viewer=self.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="bbox",
            params={"color1": hou.Vector4((1, 1, 1, 0.3))})

        # pivot2d
        self.guidePivot2d = hou.GeometryDrawable(
            scene_viewer=self.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="pivot2d")

        # perim
        self.guidePerim = hou.GeometryDrawable(
            scene_viewer=self.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="perim")

        # pivot3d
        self.guidePivot3d = hou.GeometryDrawable(
            scene_viewer=self.sceneViewer,
            geo_type=hou.drawableGeometryType.Face,
            name="pivot3d")
        self.guidePivot3d.setParams({
            "color1": hou.Vector4(0.8, 0.8, 0.4, 0.7),
            "fade_factor": 0.5
        })
        
        # ray
        self.guideRay = hou.GeometryDrawable(
            scene_viewer=self.sceneViewer,
            geo_type=hou.drawableGeometryType.Line,
            name="ray",
            params={"color1": hou.Vector4((1, 0.8, 1, 0.5))})

        # text
        self.guideText = hou.TextDrawable(
            scene_viewer=self.sceneViewer,
            name="text",
            label="test")

        
    def initParms(self):
        self.t = list(self.cam.evalParmTuple("t"))
        self.p = list(self.cam.evalParmTuple("p"))
        self.r = hou.Vector3(self.cam.evalParmTuple("r"))
        self.pr = list(self.cam.evalParmTuple("pr"))
        self.ow = self.cam.evalParm("orthowidth")

        
    def initSettings(self):
        # Reset cam, or else set state from cam.
        if self.startup_vars["cam_reset"]:
            self.camReset()
        else:
            self.camToState()
            
        # keycam node display flag.
        self.cam.setDisplayFlag(self.guides["cam_geo"])

        
    def setView(self):
        set_view = self.layout_state["set_view"]
        r = None
        if set_view == "top":
            r = (270, 0, 0)
        elif set_view == "bottom":
            r = (90, 0, 0)
        elif set_view == "front":
            r = (0, 180, 0)
        elif set_view == "back":
            r = (0, 0, 0)
        elif set_view == "right":
            r = (0, 90, 0)
        elif set_view == "left":
            r = (0, 270, 0)
        #self.r = hou.Vector3(r)
        self.stateToCam()
        

    def setFocusAttr(self):
        attr = hou.ui.readInput(
            "focus_attr",
            buttons=("OK", "Cancel"),
            initial_contents=self.hud_state_focus["focus_attr"])
        
        if attr[0] == 0:
            self.focus_state["focus_attr"] = attr[1]

            
    def setViewportLayout(self):
        layout = self.layout_state["layout"]
        self.sceneViewer.setViewportLayout(getattr(hou.geometryViewportLayout, layout))

        viewport_ct = 0
        if layout == "DoubleSide":
            viewport_ct = 2
        elif layout == "DoubleStack":
            viewport_ct = 2
        elif layout == "Quad":
            viewport_ct = 4
        elif layout == "QuadBottomSplit":
            viewport_ct = 4
        elif layout == "QuadLeftSplit":
            viewport_ct = 4
        elif layout == "Single":
            viewport_ct = 1
        elif layout == "TripleBottomSplit":
            viewport_ct = 3
        elif layout == "TripleLeftSplit":
            viewport_ct = 3

        viewport_indexs = []
        for i in range(viewport_ct):
            viewport_indexs.append(str(i))

        self.layout_state["viewport_indexs"] = viewport_indexs
        self.layout_state["viewport_index"] = viewport_indexs[0]

        
    def setViewportType(self, viewport_type_name):
        viewportType = eval("hou.geometryViewportType." + viewport_type_name.capitalize())
        viewport = self.sceneViewer.findViewport(self.layout_state["viewport_index"])
        viewport.changeType(viewportType)

        
    def stateToCam(self):
        self.cam.parmTuple("t").set(self.P_cam)
        self.cam.parmTuple("r").set(self.r)
        self.cam.parm("orthowidth").set(self.ow)
        self.updateGuides()

        
    def toggleGuide(self, kwargs, guide):
        kwargs[guide] = not kwargs[guide]
        self.update_bbox()

        
    def toggleMode(self):
        index = self.modes.index(self.mode)
        index = (index + 1) % 2
        self.mode = self.modes[index]
        self.updateHud()
        self.updateAspectRatio()

        
    def toggleProjection(self):
        cam = self.cam
        proj_parm = cam.parm("projection")
        proj = proj_parm.evalAsString() 
        if proj == "ortho":
            proj_parm.set("perspective")
        elif proj == "perspective":
            proj_parm.set("ortho")

        
    def updateAspectRatio(self):
        self.cam.parm("resx").set(1000)
        self.cam.parm("resy").set(1000)
        viewport = self.sceneViewer.findViewport("persp1")
        ratio = viewport.size()[2] / viewport.size()[3]
        self.cam.parm("aspect").set(ratio)


    def updateContext(self):
        node = self.sceneViewer.pwd()

        self.context = node.type().name()

        
    def updateGuides(self):
        self.updateGuideAxisCam()
        self.updateGuideAxisPivot()
        self.updateGuideBbox()
        self.updateGuidePerim()
        self.updateGuidePivot2d()
        self.updateGuidePivot3d()
        self.updateGuideRay()
        self.updateGuideText()

        
    def updateGuideAxisCam(self):
        if self.guides["axis_cam"]:
            axes = (self.local_x, self.local_y, self.local_z)
            geo = hou.Geometry()
            for i in range(3):
                P0 = axes[i] * 1 + self.P_cam
                P1 = axes[i] * -1 + self.P_cam
                pt_arr = geo.createPoints((P0, P1))
                poly = geo.createPolygon(is_closed=False)
                poly.addVertex(pt_arr[0])
                poly.addVertex(pt_arr[1])
            self.guideAxisCam.setGeometry(geo)
            self.guideAxisCam.show(1)
            
        else:
            self.guideAxisCam.setGeometry(None)
            self.guideAxisCam.show(0)

            
    def updateGuideAxisPivot(self):
        if self.guides["axis_pivot"]:
            P_pivot = hou.Vector3(self.P_pivot)
            axes = (hou.Vector3(1, 0, 0), hou.Vector3(0, 1, 0), hou.Vector3(0, 0, 1))
            colors = ([1.0, 0.7, 0.7], [0.7, 1.0, 0.7], [0.7, 0.7, 1.0])
            geo = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (0.1, 0.1, 0.1))

            for i in range(3):
                P0 = axes[i] *  1 + P_pivot
                P1 = axes[i] * -1 + P_pivot
                pt_arr = geo.createPoints((P0, P1))
                pt_arr[0].setAttribValue("Cd", colors[i])
                pt_arr[1].setAttribValue("Cd", colors[i])
                poly = geo.createPolygon(is_closed=False)
                poly.addVertex(pt_arr[0])
                poly.addVertex(pt_arr[1])
            self.guideAxisPivot.setGeometry(geo)
            self.guideAxisPivot.setParams({"fade_factor": 0.0})
            self.guideAxisPivot.show(1)

        else:
            # self.guideAxisPivot.setGeometry(None)
            self.guideAxisPivot.show(0)

            
    def updateGuideBbox(self):
        if self.guides["bbox"]:
            geo  = self.get_get()
            bbox = geo.boundingBox()
            P0 = (bbox[0], bbox[1], bbox[2])
            P1 = (bbox[0], bbox[1], bbox[5])
            P2 = (bbox[3], bbox[1], bbox[5])
            P3 = (bbox[3], bbox[1], bbox[2])
            P4 = (bbox[0], bbox[4], bbox[2])
            P5 = (bbox[0], bbox[4], bbox[5])
            P6 = (bbox[3], bbox[4], bbox[5])
            P7 = (bbox[3], bbox[4], bbox[2])
            #print(bbox)
            self.guideBbox.setGeometry(geo)
            self.guideBbox.show(1)

        else:
            # self.guideBbox.setGeometry(None)
            self.guideBbox.show(0)

            
    def updateGuidePerim(self):
        if self.guides["perim"]:
            rad  = self.P_pivot.distanceTo(self.P_cam)
            self.log(str(rad) + "x")
            verb = hou.sopNodeTypeCategory().nodeVerb("circle")
            verb.setParms({
                "divs": 128,
                "type": 1,
                "t": self.P_pivot,
                #"r": self.r,
                "scale": rad,
                "orient": 2
            })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guide_perim.setParams({
                "color1": hou.Vector4(1.0, 1.0, 1.0, 0.25),
                "fade_factor": 1.0
            })
            self.guidePerim.setGeometry(geo)
            self.guidePerim.show(1)
            
        else:
            # self.guidePerim.setGeometry(geo)
            self.guidePerim.show(0)

            
    def updateGuidePivot2d(self):
        if self.guides["pivot_2d"]:
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
                "scale": ow * 0.0075
            })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guide_pivot_2d.setParams({
                "color1":  hou.Vector4(0.0, 0.0, 1, 1),
                "fade_factor": 1.0
            })
            self.guidePivot2d.setGeometry(geo)
            self.guidePivot2d.show(1)

        else:
            # self.guidePivot2d.setGeometry(None)
            self.guidePivot2d.show(0)

            
    def updateGuidePivot3d(self):
        if self.guides["pivot_3d"]:
            verb = hou.sopNodeTypeCategory().nodeVerb("sphere")
            verb.setParms({
                "type": 1,
                "t": self.P_pivot,
                "scale": self.P_cam.distanceTo(self.P_pivot) * 0.002
            })
            geo = hou.Geometry()
            verb.execute(geo, [])
            self.guidePivot3d.setGeometry(geo)
            self.guidePivot3d.show(1)

        else:
            self.guidePivot3d.setGeometry(None)
            self.guidePivot3d.show(0)

            
    def updateGuideText(self):
        return

    
    def updateGuideRay(self):
        if self.guides["ray"]:
            P_pivot = self.P_pivot
            P_cam = self.P_cam
            geo = hou.Geometry()
            geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
            pt_arr = geo.createPoints((P_pivot, P_cam))
            poly = geo.createPolygon()
            poly.addVertex(pt_arr[0])
            poly.addVertex(pt_arr[1])
            self.guideRay.setGeometry(geo)
            self.guideRay.show(1)

        else:
            self.guideRay.setGeometry(0)
            self.guideRay.show(0)

            
    def updateHud(self):
        # Update graph bar counts.
        self.updateHudGCt()
        # Find and apply the appropriate hud dictionary.
        hud_state = getattr(self, "HUD_" + self.hud.upper())
        self.sceneViewer.hudInfo(template=hud_state)
        
        # Find the new update values.
        vals = getattr(self, self.hud + "_state")
        updates = {}
        
        # for row in hud_state["rows"]:
            # Skip processing dividers.
            # if row["id"] != "divider":
                
                # First three are common to all huds.
                # if row["id"] == "mode":
                    # updates["mode"] = {"value": self.mode}
                # elif row["id"] == "hud":
                    # updates["hud"] = {"value": self.hud}
                # elif row["id"] == "hud_g":
                    # updates["hud_g"] = {"value": self.huds.index(self.hud)}

                # If it is a graph.
                # elif row["id"][-2:] == "_g":
                    # val_name = row["id"][0:-2]
                    # val = vals[val_name]
                    # print(vals)
                    # print(val_name)
                    
                    # vals = vals[val + "s"]
                    # updates[row["id"]] = {"value": vals.index(val)}
                # For other controls.
                # else:
                    # print(row)
                    # val_name = row["id"]
                    # val = vals[val_name]
                    # updates[row["id"]] = {"value": val}

        # Add brackets in setting mode.
        # if self.mode == "settings":
            # updates[vals["ctl"]]["value"] = "[" + updates[vals["ctl"]]["value"] + "]"

        # Apply the updates.
        # self.sceneViewer.hudInfo(hud_values=updates)

        
    def updateHudGCt(self):
        # Calculate the number of bars in a graph based on the length of the appropriate array.
        hud_name = self.hud
        d = getattr(self, hud_name + "_state")
        hud_state = getattr(self, "HUD_" + hud_name.upper())

        for i, row in enumerate(hud_state["rows"]):
            # If row ID indicates it is a graph.
            if row["id"][-2:] == "_g":
                arr = None
                # Count the number of items in the array.
                if row["id"] == "hud_g":
                    arr = self.huds
                else:
                    arr = d[row["id"][0:-2] + "s"]
                # Set the number of bars in the graph.
                hud_state["rows"][i]["count"] = len(arr)

            
    def viewportFrame(self):
        for viewport in self.sceneViewer.viewports():
            cam = viewport.camera()
            # Is camera node or default.
            if cam == None:
                viewport.frameAll()
            else:
                viewport.frameAll()
        self.camToState()

        
    def viewportSwap(self):
        viewports = self.sceneViewer.viewports()
        viewport_names = [viewport.name() for viewport in viewports]
        viewports = viewports[1:] + [viewports[0]]
        viewportTypes = viewportTypes[1:] + [viewportTypes[0]]
        
        for i, viewport in enumerate(viewports):
            viewport.changeName("v" * i)
        for i, viewport in enumerate(viewports):
            viewport.changeName(viewports[i])
            viewport.changeType(viewportTypes[i])


        
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
    menu = hou.ViewerStateMenu("keycamMenu", "keycamMenu")
    menu.addActionItem("camFrame", "camFrame")
    menu.addActionItem("camReset", "camReset") 
    menu.addActionItem("viewportFrame", "viewportFrame") 

    menu.addToggleItem("axis_cam", "axis_cam", 1)
    menu.addToggleItem("axis_pivot", "axis_pivot", 1)
    menu.addToggleItem("perim", "perim", 1)
    menu.addToggleItem("pivot_2d", "pivot_2d", 0)
    menu.addToggleItem("pivot_3d", "pivot_3d", 1)
    menu.addToggleItem("ray", "ray", 1)
    return menu
