import os.path

this_path = hou.hipFile.path()

path = "~/src/hou-ctl/recent_paths"
path = os.path.expanduser(path)
file = open(path, "r")
path_arr = file.read().split("\n")

if this_path in path_arr:
    path_arr.remove(this_path)
path_arr.insert(0, this_path)

file = open(path, "w")
file.write("\n".join(path_arr))
