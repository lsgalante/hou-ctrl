import os.path

path = "~/src/hou-ctrl/recent_paths"
path = os.path.expanduser(path)
file = open(path, "r")
choice_arr = file.read().split("\n")

i = hou.ui.selectFromList(
    choices=choice_arr,
    exclusive=True,
    message="recent files",
    column_header="path"
)
if len(i) > 0:
    hou.hipFile.load(choice_arr[i[0]])