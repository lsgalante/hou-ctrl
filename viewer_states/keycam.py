import hou
from hclib import HCCam, HCGeo, HCSceneViewer


def createViewerStateTemplate():
    ## Define template
    template = hou.ViewerStateTemplate(
        type_name='keycam',
        label="keycam",
        category=hou.objNodeTypeCategory(),
        contexts=[hou.sopNodeTypeCategory()]
    )

    template.bindFactory(State)
    template.bindIcon('DESKTOP_application_sierra')

    ## Parameters
    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='layout',
        label="Layout",
        default_value='single',
        menu_items=[
            ('doubleside', "DoubleSide"),
            ('doublestack', "DoubleStack"),
            ('quad', "Quad"),
            ('quadbottomsplit', "QuadBottomSplit"),
            ('quadleftsplit', "QuadLeftSplit"),
            ('single', "Single"),
            ('triplebottomsplit', "TripleBottomSplit"),
            ('tripleleftsplit', "TripleLeftSplit")
        ]
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='viewport',
        label="Viewport",
        default_value='center',
        menu_items=[('center', "Center")]
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='view',
        label="View",
        default_value='persp',
        menu_items=[
            ('persp', "Perspective"),
            ('top', "Top"),
            ('front', "Front"),
            ('right', "Right"),
            ('uv', "UV"),
            ('bottom', "Bottom"),
            ('back', "Back"),
            ('left', "Left")
        ]
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='camera',
        label="Camera",
        default_value='keycam',
        menu_items=[('keycam', "Keycam"), ('default', "Default"), ('other', "Other")],
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Menu,
        name='target',
        label="Target",
        default_value='cam',
        menu_items=[('cam', "Camera"), ('pivot', "Pivot")],
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Separator,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='t',
        label="Translation",
        num_components=3,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='r',
        label="Rotation",
        num_components=3,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='p',
        label="Pivot",
        num_components=3,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='zoom',
        label="Zoom",
        num_components=1,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='ow',
        label="Ortho Width",
        num_components=1,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Separator,
        toolbox=False
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='deltat',
        label="Delta T",
        default_value=1.0,
        min_limit=0,
        max_limit=10.0
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='deltar',
        label="Delta R",
        default_value=15.0,
        min_limit=-180.0,
        max_limit=180.0
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='deltazoom',
        label="Delta Zoom",
        default_value=10.0,
        min_limit=0,
        max_limit=10.0
    )

    template.bindParameter(
        hou.parmTemplateType.Float,
        name='deltaow',
        label="Delta OW",
        default_value=1.0,
        min_limit=0,
        max_limit=10.0
    )

    # Context menu
    menu = hou.ViewerStateMenu('keycam_menu', "Keycam Menu")
    menu.addActionItem('frame', "Frame")
    menu.addActionItem('reset', "Reset")

    setViewMenu = hou.ViewerStateMenu('set_view_menu', "Set View")
    setViewMenu.addActionItem('top', "Top")
    setViewMenu.addActionItem('bottom', "Bottom")
    setViewMenu.addActionItem('front', "Front")
    setViewMenu.addActionItem('back', "Back")
    setViewMenu.addActionItem('left', "Left")
    # setViewMenu.addActionItem('right', "Right")
    menu.addMenu(setViewMenu)

    guideMenu = hou.ViewerStateMenu('guide_menu', "Guides")
    guideMenu.addToggleItem('bbox', "Bbox", 1)
    guideMenu.addToggleItem('cam_axis', "Camera Axis", 1)
    guideMenu.addToggleItem('pivot_axis', "Pivot Axis", 1)
    guideMenu.addToggleItem('perim', "Perimeter", 0)
    guideMenu.addToggleItem('pivot2d', "2D Pivot", 1)
    guideMenu.addToggleItem('pivot3d', "3D Pivot", 0)
    guideMenu.addToggleItem('ray', "Ray", 0)
    menu.addMenu(guideMenu)

    menu.addSeparator()
    template.bindMenu(menu)

    # Ok
    return template


class State(object):
    def __init__(self, state_name, scene_viewer):
        # Put options first
        self.options = {
            'center_on_geo': 1,
            'lock_cam': 1,
            'reset': 1,
            'show_bbox': 1,
            'show_perim': 0,
            'show_pivot2d': 0,
            'show_pivot3d': 1,
            'show_pivot_axis': 1,
            'show_ray': 0,
        }

        self.viewer = scene_viewer
        self.state_name = state_name
        self.cam_type = None
        self.context = None
        self.kwargs = None

        # Check for cam node
        if not hou.node('/obj/keycam'):
            cam = hou.node('/obj').createNode('cam')
            cam.setName('keycam')
            cam.parm('xOrd').set(0)
        self.cam = hou.node('/obj/keycam')
        self.hccam = HCCam(self.cam, self.viewer)
        # self.hcdefaultcam = HCDefaultCam(self, defaultcam)
        self.hcgeo = None
        self.guides = None
        self.hud = None
        self.hcviewer = None

    def onDraw(self, kwargs):
        self.guides.draw(kwargs)

    def onExit(self, kwargs):
        for viewport in self.viewer.viewports():
            viewport.lockCameraToView(False)

    def onGenerate(self, kwargs):
        # Prevent exiting the state when current node changes
        kwargs['state_flags']['exit_on_node_select'] = False
        self.kwargs = kwargs
        self.hcgeo = HCGeo(self.viewer)
        self.guides = Guides(self)
        self.hcviewer = HCSceneViewer(self.viewer)
        self.hud = Hud(self)
        self.hud.update()
        self.updateNetworkContext()
        self.guides.update()

    def onKeyEvent(self, kwargs):
        self.hccam.fitAspectRatio()
        # Node-based camera
        keymap = {
            '-': lambda: self.hccam.zoom('out'),
            '=': lambda: self.hccam.zoom('in'),
            'o': lambda: self.hccam.toggleProjection(),
            'h': lambda: self.hccam.rotate('left'),
            'j': lambda: self.hccam.rotate('down'),
            'k': lambda: self.hccam.rotate('up'),
            'l': lambda: self.hccam.rotate('right'),
            'v': lambda: self.hcviewer.nextView(),
            'Shift+-': lambda: self.hccam.zoomOrtho('out'),
            'Shift+=': lambda: self.hccam.zoomOrtho('in'),
            'Shift+h': lambda: self.hccam.translate('left'),
            'Shift+j': lambda: self.hccam.translate('down'),
            'Shift+k': lambda: self.hccam.translate('up'),
            'Shift+l': lambda: self.hccam.translate('right'),
            'Ctrl+l': lambda: self.hcviewer.nextLayout(),
            'f': lambda: self.hccam.frame()
            # 'c': lambda: self.hccam.center()
        }
        key = kwargs['ui_event'].device().keyString()
        if key in keymap:
            keymap[key]()
            self.guides.update()
            return True
        else:
            return False

        # Default cam
        # if 2 == 1:
        #     default_cam_map = {
        #         'hou.geometryViewportType.Top': (0, 1),
        #         'hou.geometryViewportType.Bottom': (2, 0),
        #         'hou.geometryViewportType.Front': (0, 1),
        #         'hou.geometryViewportType.Back': (1, 0),
        #         'hou.geometryViewportType.Right': (0, 1),
        #         'hou.geometryViewportType.Left': (1, 2),
        #     }
        #     viewport_type = self.hcviewer.viewport().type()
        #     self.indices = default_cam_map[str(viewport_type)]

        #     keymap = {
        #         '-': self.hcdefaultcam.zoomOut,
        #         '+': self.hcdefaultcam.zoomIn,
        #         'h': self.hcdefaultcam.translateLeft,
        #         'j': self.hcdefaultcam.translateDown,
        #         'k': self.hcdefaultcam.translateUp,
        #         'l': self.hcdefaultcam.translateRight,
        #         'v': self.hcdefaultcam.nextView,
        #         'Shift+h': self.hcdefaultcam.rotateLeft,
        #         'Shift+l': self.hcdefaultcam.rotateRight,
        #         'Ctrl+l': self.hcviewer.nextLayout,
        #     }

    def onMenuAction(self, kwargs):
        menumap = {
            'frame': lambda: self.hccam.frame(),
            'reset': lambda: self.hccam.reset(),
            'bbox': lambda: self.guides.bbox.show(kwargs['bbox']),
            'cam_axis': lambda: self.guides.cam_axis.show(kwargs['cam_axis']),
            'pivot_axis': lambda: self.guides.pivot_axis.show(kwargs['pivot_axis']),
            'perim': lambda: self.guides.perim.show(kwargs['perm']),
            'pivot2d': lambda: self.guides.pivot2d.show(kwargs['pivot2d']),
            'pivot3d': lambda: self.guides.pivot3d.show(kwargs['pivot3d']),
            'ray': lambda: self.guides.ray.show(kwargs['ray'])
        }

        return menumap[kwargs['menu_item']]()

    def onParmChangeEvent(self, kwargs):
        parmmap = {
            't': self.hccam.parms.t,
            'p': self.hccam.parms.p,
            'r': self.hccam.parms.r,
            'ow': self.hccam.parms.ow,
            'zoom': self.hccam.parms.zoom,
            'target': self.hccam.parms.target,
            'deltar': self.hccam.parms.deltar,
            'deltazoom': self.hccam.parms.deltazoom,
            # 'deltaow': self.hccam.parms.deltaow,
            'layout': self.hccam.parms.layout,
            'viewport': self.hccam.parms.viewport,
            # 'view': self.hccam.parms.view,
            # 'camera': self.hccam.parms.camera,
        }
        parm = parmmap[kwargs['parm_name']]
        parm = kwargs['parm_value']
        return parm
        # self.guides.update()

    def updateNetworkContext(self):
        node = self.viewer.pwd()
        self.context = node.type().name()


class Guides:
    def __init__(self, state):
        self.state = state
        self.cam = state.cam
        self.hccam = state.hccam
        self.hcgeo = state.hcgeo
        self.viewer = state.viewer

        self.options = {
            'axis_size': 1,
            'tie_axis_to_radius': 0
        }

        self.states = {
            'cam_axis': 1,
            'pivot_axis': 0,
            'bbox': 1,
            'cam': 0,
            'perim': 0,
            'pivot2d': 0,
            'pivot3d': 1,
            'ray': 0
        }

        self.cam_axis = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='cam_axis'
        )

        self.pivot_axis = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='pivot_axis',
            params={
                'color1': hou.Vector4((1, 1, 1, 0.5))
            }
        )

        self.bbox = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='bbox',
            params={
                'color1': hou.Vector4((1, 1, 1, 0.3)),
                'fade_factor': 0.0
            }
        )

        self.perim = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='perim'
        )

        self.pivot2d = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='pivot2d'
        )

        self.pivot3d = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Face,
            name='pivot3d',
            params={
                'color1': hou.Vector4(0.2, 0.8, 0.2, 0.6),
                'fade_factor': 0.2
            }
        )

        self.ray = hou.GeometryDrawable(
            scene_viewer=self.viewer,
            geo_type=hou.drawableGeometryType.Line,
            name='ray',
            params={
                'color1': hou.Vector4((1, 0.8, 1, 0.5))
            }
        )

    def draw(self, kwargs):
        funcmap = {
            'bbox': self.bbox.draw,
            'cam_axis': self.cam_axis.draw,
            'pivot_axis': self.pivot_axis.draw,
            'perim': self.perim.draw,
            'pivot2d': self.pivot2d.draw,
            'pivot3d': self.pivot3d.draw,
            'ray': self.ray.draw
        }
        for name, value in self.states.items():
            if value:
                funcmap[name](kwargs['draw_handle'], {})

    def update(self):
        funcmap = {
            'bbox': self.makeBbox,
            'cam_axis': self.makeCamAxis,
            'pivot_axis': self.makePivotAxis,
            'perim': self.makePerim,
            'pivot2d': self.makePivot2d,
            'pivot3d': self.makePivot3d,
            'ray': self.makeRay
        }
        for name, value in self.states.items():
            if value:
                funcmap[name]()
        # self.cam_axis.show(self.states['cam_axis'])
        # self.pivot_axis.show(self.states['pivot_axis'])
        self.bbox.show(self.states['bbox'])
        # self.cam.show(self.states['cam'])
        # self.perim.show(self.states['perim'])
        # self.pivot2d.show(self.states['pivot2d'])
        self.pivot3d.show(self.states['pivot3d'])
        # self.ray.show(self.states['ray'])

    def makeCamAxis(self):
        axes = (
            self.hccam.parms.localx,
            self.hccam.parms.localy,
            self.hccam.parms.localz
        )
        geo = hou.Geometry()
        for i in range(3):
            P0 = self.hccam.parms.t + axes[i]
            P1 = self.hccam.parms.t + axes[i] * -1
            pts = geo.createPoints((P0, P1))
            poly = geo.createPolygon(is_closed=False)
            poly.addVertex(pts[0])
            poly.addVertex(pts[1])
        self.cam_axis.setGeometry(geo)

    def makePivotAxis(self):
        axes = (
            hou.Vector3(1, 0, 0),
            hou.Vector3(0, 1, 0),
            hou.Vector3(0, 0, 1)
        )
        colors = (
            [1.0, 0.7, 0.7],
            [0.7, 1.0, 0.7],
            [0.7, 0.7, 1.0]
        )
        geo = hou.Geometry()
        geo.addAttrib(hou.attribType.Point, 'Cd', (0.1, 0.1, 0.1))
        for i in range(3):
            P0 = self.hccam.parms.p + axes[i]
            P1 = self.hccam.parms.p + axes[i] * -1
            pts = geo.createPoints((P0, P1))
            pts[0].setAttribValue('Cd', colors[i])
            pts[1].setAttribValue('Cd', colors[i])
            # poly = geo.createPolygon(is_closed=False)
            # poly.addVertex(pts[0])
            # poly.addVertex(pts[1])
        self.pivot_axis.setGeometry(geo)
        self.pivot_axis.setParams(
            {'fade_factor': 0.0}
        )

    def makeBbox(self):
        guide_geo = hou.Geometry()
        target_geo = self.hcgeo.get()
        bbox = target_geo.boundingBox()
        box = hou.sopNodeTypeCategory().nodeVerb('box')
        box.setParms({
            'size': bbox.sizevec(),
            't': bbox.center()
        })
        box.execute(guide_geo, [])
        self.bbox.setGeometry(guide_geo)

    def makePerim(self):
        guide_geo = hou.Geometry()
        circle = hou.sopNodeTypeCategory().nodeVerb('circle')
        circle.setParms({
            'divs': 128,
            'type': 1,
            't': self.hccam.parms.p,
            'scale': self.hccam.parms.p.distanceTo(self.hccam.parms.t),
            'orient': 2
        })
        circle.execute(guide_geo, [])
        self.perim.setParams({
            'color1': hou.Vector4(1.0, 1.0, 1.0, 0.25),
            'fade_factor': 1.0
        })
        self.perim.setGeometry(guide_geo)

    def makePivot2d(self):
        guide_geo = hou.Geometry()
        circle = hou.sopNodeTypeCategory().nodeVerb('circle')
        circle.setParms({
            'type': 1,
            'r': self.hccam.parms.r,
            't': self.hccam.parms.p,
            'scale': self.hccam.parms.ow * 0.0075
        })
        circle.execute(guide_geo, [])
        self.pivot2d.setParams({
            'color1': hou.Vector4(0.0, 0.0, 1, 1),
            'fade_factor': 1.0
        })
        self.pivot2d.setGeometry(guide_geo)

    def makePivot3d(self):
        guide_geo = hou.Geometry()
        sphere = hou.sopNodeTypeCategory().nodeVerb('sphere')
        sphere.setParms({
            'freq': 7,
            # 'scale' = self.hccam.parms.t.distanceTo(self.hccam.parms.p) * 0.02,
            'scale': 0.03,
            'type': 1,
            't': self.hccam.parms.p
        })
        sphere.execute(guide_geo, [])
        self.pivot3d.setGeometry(guide_geo)

    def makeRay(self):
        guide_geo = hou.Geometry()
        guide_geo.addAttrib(hou.attribType.Point, "Cd", (1, 0, 0))
        pts = guide_geo.createPoints((self.hccam.parms.p, self.hccam.parms.t))
        poly = guide_geo.createPolygon()
        poly.addVertex(pts[0])
        poly.addVertex(pts[1])
        self.ray.setGeometry(guide_geo)


class Hud:
    def __init__(self, state):
        self.state = state
        self.hcviewer = state.hcviewer
        self.viewer = state.viewer
        self.template = {
            'title': "Keycam",
            'rows': [
                {'id': 'layout', 'type': 'plain', 'label': "Layout", 'value': "Single", 'key': "Ctrl + L"},
                {'id': 'layout_g', 'type': 'choicegraph', 'count': 8},
                {'id': 'viewport', 'type': 'plain', 'label': "Viewport", 'value': "0", 'key': "Ctrl + V"},
                {'id': 'viewport_g', 'type': 'choicegraph', 'count': 4},
                {'id': 'view', 'type': 'plain', 'label': "View", 'value': "Perspective", 'key': "V"},
                {'id': 'view_g', 'type': 'choicegraph', 'count': 8},
                {'id': 'target', 'type': 'plain', 'label': "Target", 'value': "Camera", 'key': "T"},
                {'id': 'target_g', 'type': 'choicegraph', 'count': 2},
                {'id': 'vis', 'type': 'plain', 'label': "Vis"},
                {'id': 'focus', 'type': 'plain', 'label': "Focus", 'value': 0},
                {'id': 'focus_g', 'type': 'choicegraph', 'count': 10}
            ]
        }

    def update(self):
        layoutmap = {
            'geometryViewportLayout.DoubleSide': 2,
            'geometryViewportLayout.DoubleStack': 2,
            'geometryViewportLayout.Quad': 4,
            'geometryViewportLayout.QuadBottomSplit': 4,
            'geometryViewportLayout.QuadLeftSplit': 4,
            'geometryViewportLayout.TripleBottomSplit': 3,
            'geometryViewportLayout.TripleLeftSplit': 3,
            'geometryViewportLayout.Single': 1,
        }
        layout = self.hcviewer.layout()
        n_viewports = layoutmap[str(layout)]
        self.template['rows'][3]['count'] = n_viewports
        self.viewer.hudInfo(template=self.template)
        updates = {
            'layout': str(self.hcviewer.layout())[23:],
            'layout_g': self.hcviewer.layouts().index(self.hcviewer.layout()),
        }
        self.viewer.hudInfo(hud_values=updates)
