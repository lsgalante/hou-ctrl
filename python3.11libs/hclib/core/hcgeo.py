import hou

class HCGeo:
    def __init__(self, viewer):
        self.viewer = viewer
        self.geo = self.get()
        self.geo_type = hou.drawableGeometryType.Line
        self.name = "geo"
        self.color = hou.Vector4((1, 1, 1, 0.5))
        self.geo_parms = {"color1": self.color}
        self.geo_drawable = hou.GeometryDrawable(scene_viewer=viewer,
            geo_type=self.geo_type, name=self.name, params=self.geo_parms)

    def bbox(self):
        geo = self.get()
        return geo.boundingBox()

    def centroid(self):
        geo_out = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb("extractcentroid")
        verb.setParms({"partitiontype": 2})
        verb.execute(geo_out, [self.geo])
        pt = geo_out.point(0)
        centroid = pt.position()
        return centroid

    def get(self):
        pwd = self.viewer.pwd()
        self.displayNode = None
        self.context = pwd.childTypeCategory().label()
        if self.context == "dop":
            self.displayNode = pwd.displayNode()
        elif self.context == "lop":
            return None
        elif self.context == "Objects":
            self.displayNode = pwd.children()[0].displayNode()
        elif self.context == "Geometry":
            self.displayNode = pwd.displayNode()
        return self.displayNode.geometry()
