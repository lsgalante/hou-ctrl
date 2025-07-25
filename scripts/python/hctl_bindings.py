import hou

# Key names:
# uparrow, downarrow, leftarrow, rightarrow
# alt, cmd, shift, ctrl, tab, del, backspace, enter, esc
# f1, f2...
# pageup, pagedown, end, home, insert
# /, \\
# pad0, pad1, pad2...
# padstar, padslash
# pause
# space

def updateBindings():
    hou.hotkeys.revertToDefaults("h", "", False)

    # Clear all assignments from command
    assignment_clear_arr = (
        "deskmgr.new",
        "deskmgr.save",

        "h.add_key",
        "h.aliases",
        "h.audio_panel",
        "h.auto_key",
        "h.cache_manager",
        "h.channeleditor",
        "h.clear_cop_caches",
        "h.comp_project_manager",
        "h.context_help",
        # "h.copy",
        # "h.cut",
        "h.desktop_mgr",
        "h.desktopToggleHctl"
        # "h.find",
        "h.mat_palette",
        # "h.open",
        # "h.pane.closetab",
        # "h.paste",
        # "h.redo",
        # "h.save",
        # "h.undo",

        "h.pane.gview.decrease_subd",
        "h.pane.gview.increase_subd",
        "h.pane.gview.state.volatile_chmodify",

        # "h.pane.edit_bookmark",
        # "h.pane.nexttab",
        # "h.pane.to_parm",

        "h.pane.wsheet.add_image",
        "h.pane.wsheet.add_postit",
        "h.pane.wsheet.addfileop",
        "h.pane.wsheet.allowdroponwire",
        "h.pane.wsheet.batch_rename",
        "h.pane.wsheet.down",
        "h.pane.wsheet.edit_images",
        "h.pane.wsheet.layout", "l",
        "h.pane.wsheet.layout_all",
        "h.pane.wsheet.left",
        "h.pane.wsheet.maximize",
        "h.pane.wsheet.minimize",
        "h.pane.wsheet.node_quick_nav",
        "h.pane.wsheet.right",
        "h.pane.wsheet.scope_chans",
        "h.pane.wsheet.select",
        "h.pane.wsheet.stitch_mode",
        "h.pane.wsheet.up",
        "h.pane.wsheet.zoom_in",
        "h.pane.wsheet.zoom_out",

        "inputfield.context_help"
    )

    # Remove assignments
    assignment_remove_arr = (
        ("h.cut", "alt+x"),
        ("h.pane.wsheet.home", "h"),
        ("h.pane.wsheet.home_selected", "shift+h"),
    )

    # New assignments
    assignment_add_arr = (
        # ("deskmgr.save", "ctrl+s"),

        # ("h.copy", "cmd+w"),
        # ("h.cut", "ctrl+w"),
        ("h.hctlSession_hctlPanel", "alt+x"),
        # ("h.find", "ctrl+s"),
        # ("h.open", "ctrl+o"),
        # ("h.paste", "ctrl+y"),
        # ("h.redo", "ctrl+shift+z"),
        # ("h.save", "cmd+s"),
        ("h.sceneViewerToggleKeycam", "shift+k"),
        # ("h.undo", "ctrl+/"),

        ("h.pane.editparms.selectall", "alt+h"),

        ("h.pane.gview.refplane", "shift+g"),

        ("h.pane.nexttab", "ctrl+space"),
        ("h.pane.prevtab", "ctrl+shift+space"),

        ("h.pane.parms.edit_expression", "ctrl+e"),

        ("h.pane.wsheet.up", "shift+k"),
        ("h.pane.wsheet.down", "shift+j"),
        ("h.pane.wsheet.left", "shift+h"),
        ("h.pane.wsheet.node_quick_nav", "ctrl+s"),
        ("h.pane.wsheet.right", "shift+l"),
        ("h.pane.wsheet.select", "ctrl+alt+h"),
        # ("h.pane.wsheet.zoom_in", "="),
        # ("h.pane.wsheet.zoom_out", "-"),

        ("h.pane.textport.down", "ctrl+n"),
        ("h.pane.textport.up", "ctrl+p"),
        ("h.pane.textport.bottom", "ctrl+e"),
        ("h.pane.textport.firstline", "cmd+shift+,"),
        ("h.pane.textport.top", "ctrl+a"),
        ("h.pane.textport.jump_to_line", "alt+g"),
        ("h.pane.textport.lastline", "cmd+shift+."),
        ("h.pane.textport.next", "ctrl+f"),
        ("h.pane.textport.nextword", "cmd+f"),
        ("h.pane.textport.pagedown", "ctrl+v"),
        ("h.pane.textport.pageup", "cmd+v"),
        ("h.pane.textport.prev", "ctrl+b"),
        ("h.pane.textport.selectdown", "ctrl+shift+n"),
        ("h.pane.textport.selectbottom", "ctrl+shift+e"),
        ("h.pane.textport.selecttop", "ctrl+shift+a"),
        ("h.pane.textport.selectnext", "ctrl+shift+f"),
        ("h.pane.textport.selectnextword", "cmd+shift+f"),
        ("h.pane.textport.selectprev", "ctrl+shift+b"),
        ("h.pane.textport.selectprevword", "cmd+shift+b"),
        ("h.pane.textport.selectup", "ctrl+shift+p"),
        ("h.pane.textport.toggle_comment", "ctrl+;"),

        ("inputfield.down", "ctrl+n"),
        ("inputfield.end", "ctrl+e"),
        ("inputfield.home", "ctrl+a"),
        ("inputfield.next", "ctrl+f"),
        ("inputfield.next_word", "alt+f"),
        ("inputfield.prev", "ctrl+b"),
        ("inputfield.prev_word", "alt+b"),
        ("inputfield.up", "ctrl+p")
    )

    # Command bindings
    command_binding_arr = (
        # ("h.pane.pythonshell", "h.desktopToggleHctl")
    )


    for assignment in assignment_clear_arr:
        context = assignment.rpartition(".")[0]
        symbol = assignment
        hou.hotkeys.clearAssignments(context, symbol)

    for assignment in assignment_remove_arr:
        context = assignment[0].rpartition(".")[0]
        symbol = assignment[0]
        key = assignment[1]
        hou.hotkeys.removeAssignment(context, symbol, key)

    for assignment in assignment_add_arr:
        context = assignment[0].rpartition(".")[0]
        print(context)
        symbol = assignment[0]
        key = assignment[1]
        hou.hotkeys.addAssignment(context, symbol, key)

    for binding in command_binding_arr:
        context = binding[0]
        command = binding[1]
        hou.hotkeys.addCommandBinding(context, command)
