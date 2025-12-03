import hou

class HCGeo:
    def __init__(self, geo):
        self.geo = geo

    def bbox(self):
        return geo.boundingBox()

    def centroid(self):
        geo_out = hou.Geometry()
        extract_centroid = hou.sopNodeTypeCategory().nodeVerb('extractcentroid')
        extract_centroid.setParms(
            {'partitiontype': 2}
        )
        extract_centroid.execute(geo_out, [self.geo])
        pt = geo_out.point(0)
        return pt.position()
