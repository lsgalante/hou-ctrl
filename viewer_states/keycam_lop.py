
        if not hou.node("/stage/keycam"):
            stage_cam = hou.node("/stage").createNode("camera")
            stage_cam.setName("keycam")
