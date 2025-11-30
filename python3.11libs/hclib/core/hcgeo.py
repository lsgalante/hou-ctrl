import hou

class HCGeo:
    def __init__(self, viewer):
        self.viewer = viewer
        self.geo = self.get()

    def bbox(self):
        geo = self.get()
        return geo.boundingBox()

    def centroid(self):
        geo_out = hou.Geometry()
        verb = hou.sopNodeTypeCategory().nodeVerb('extractcentroid')
        verb.setParms(
            {'partitiontype': 2}
        )
        verb.execute(geo_out, [self.geo])
        pt = geo_out.point(0)
        centroid = pt.position()
        return centroid

    def context(self):
        return self.viewer.pwd()

    def contextType(self):
        return self.viewer.pwd().type().name()

    def get(self):
        map = {
            'dop': self.node,
            'lop': None,
            'obj': self.viewer.pwd().children()[0].displayNode,
            'Geometry': self.node
        }
        self.displayNode = map[self.contextType()]()
        return self.displayNode.geometry()

    def node(self):
        return self.viewer.currentNode()

    def nodeType(self):
        return self.viewer.currentNode().type().name()
