# import pathlib

# print("--BEGIN 123.py--")

# enable_recent_menu = 0

# if enable_recent_menu == 1:
#     path_raw = "~/src/hou-ctl/recent_paths"
#     path = pathlib.PosixPath(path_raw)
#     path = path.expanduser()

#     if not path.is_file():
#         path.touch()

#     choices_raw = path.read_text()
#     choice_arr = choices_raw.split("\n")
#     i = hou.ui.selectFromList(
#         choices=choice_arr,
#         exclusive=True,
#         message="Recent Files",
#         column_header="Path"
#     )

#     # on accept
#     if len(i) > 0:
#         choice = choice_arr[i[0]]
#         hou.hipFile.load(choice)

# print("--END 123.py--")
