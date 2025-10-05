import hou


class HctlViewport():
    def __init__(self):
        pass
        # self.viewport = viewport
    __init__.interactive = False


    def update():
        pass
    update.interactive = False


    def visualizers(self):
        category = hou.viewportVisualizerCategory.Scene
        vis_arr = hou.viewportVisualizers.visualizers(category)
        return vis_arr
    visualizers.interactive = False
