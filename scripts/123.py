import os.path
import pathlib

path_raw = "~/src/hou-ctl/recent_paths"
path = PosixPath(path_raw)
path = path.expanduser()

if path.is_file():
    continue

else:
    path.touch()

choices_raw = file.read_text()
choice_arr = choices_raw.split("\n")

i = hou.ui.selectFromList(
    choices=choice_arr,
    exclusive=True,
    message="recent files",
    column_header="path"
)

# on accept
if len(i) > 0:
    choice = choice_arr[i[0]]
    hou.hipFile.load(choice)

# on cancel
else:
    return