import hou
from .hcgeo import HCGeo
from .hctab import HCTab

class HCPathTab(HCTab):
    def __init__(self, tab):
        self.tab = tab

    def context(self):
        return self.tab.pwd()

    def contextType(self):
        return self.tab.pwd().type().name()

    def currentNode(self):
        return self.tab.currentNode()

    def geo(self):
        map = {
            'dop': self.tab.currentNode,
            'lop': None,
            'obj': self.tab.pwd().children()[0].displayNode,
            'geo': self.tab.currentNode
        }
        node = map[self.contextType()]()
        return node.geometry()

    def hcgeo(self):
        return HCGeo(self.geo())

    def nodeType(self):
        return self.tab.currentNode().type().name()

    def path(self):
        return self.tab.pwd().path()

    def pwd(self):
        return self.tab.pwd()

    def selectedNodes(self):
        return self.tab.pwd().selectedChildren()
