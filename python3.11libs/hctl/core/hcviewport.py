import hou


class HCViewport():
    def __init__(self):
        pass
        # self.viewport = viewport


    def update():
        pass


    def visualizers(self):
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr
