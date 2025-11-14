import hou

# KEY NAMES
# uparrow, downarrow, leftarrow, rightarrow
# alt, cmd, shift, ctrl, tab, del, backspace, enter, esc
# f1...f12
# pageup, pagedown, end, home, insert
# /, \\
# pad0...pad9
# padstar, padslash
# pause
# space


def load():

    assignments_to_clear = (
        #
        # Desktop manager
        "deskmgr.new",
        "deskmgr.save",
        "h.desktop_mgr",
        #
        # Global
        "h.add_key",
        "h.aliases",
        "h.audio_panel",
        "h.auto_key",
        "h.cache_manager",
        "h.channeleditor",
        "h.clear_cop_caches",
        "h.comp_project_manager",
        "h.context_help",
        "h.mat_palette",
        #
        # hctl
        "h.desktopToggleHctl",
        #
        # Pane
        #
        # Pane - scene viewer
        "h.pane.gview.increase_subd",
        "h.pane.gview.decrease_subd",
        "h.pane.gview.restore_prevcam",
        "h.pane.gview.state.volatile_chmodify",
        #
        # Pane - network editor
        "h.pane.wsheet.add_image",
        "h.pane.wsheet.add_postit",
        "h.pane.wsheet.addfileop",
        "h.pane.wsheet.allowdroponwire",
        "h.pane.wsheet.batch_rename",
        "h.pane.wsheet.up",
        "h.pane.wsheet.down",
        "h.pane.wsheet.left",
        "h.pane.wsheet.right",
        "h.pane.wsheet.edit_images",
        "h.pane.wsheet.layout",
        "h.pane.wsheet.layout_all",
        "h.pane.wsheet.maximize",
        "h.pane.wsheet.minimize",
        "h.pane.wsheet.node_quick_nav",
        "h.pane.wsheet.scope_chans",
        "h.pane.wsheet.select",
        "h.pane.wsheet.stitch_mode",
        "h.pane.wsheet.zoom_in",
        "h.pane.wsheet.zoom_out",
        #
        # Input fields
        "inputfield.context_help",
    )

    assignments_to_remove = (
        #
        # Global
        ("h.cut", "alt+x"),
        #
        # Network editor
        ("h.pane.wsheet.home", "h"),
        ("h.pane.wsheet.home_selected", "shift+h"),
    )

    assignments_to_add = (
        # Pane
        ("h.pane.shelf", "ctrl+]"),
        ("h.pane.shelf", "cmd+]"),
        ("h.pane.nexttab", "ctrl+space"),
        ("h.pane.prevtab", "ctrl+shift+space"),
        #
        # hctl
        ("h.hCSessionPanel", "alt+x"),
        ("h.hCSessionPanel", "\\"),
        #
        # Scene viewer
        ("h.pane.gview.refplane", "shift+g"),
        #
        # Parameters
        ("h.pane.parms.edit_expression", "ctrl+e"),
        ("h.pane.editparms.selectall", "alt+h"),
        #
        # Network editor vim
        # ("h.pane.wsheet.up", "shift+k"),
        # ("h.pane.wsheet.down", "shift+j"),
        # ("h.pane.wsheet.left", "shift+h"),
        # ("h.pane.wsheet.right", "shift+l"),
        ("h.pane.wsheet.node_quick_nav", "ctrl+s"),
        ("h.pane.wsheet.select", "ctrl+alt+h"),
        # ("h.pane.wsheet.zoom_in", "="),
        # ("h.pane.wsheet.zoom_out", "-"),
        #
        # Text editor emacs
        # ("h.pane.textport.up", "ctrl+p"),
        # ("h.pane.textport.down", "ctrl+n"),
        # ("h.pane.textport.next", "ctrl+f"),
        # ("h.pane.textport.prev", "ctrl+b"),
        # ("h.pane.textport.top", "ctrl+a"),
        # ("h.pane.textport.bottom", "ctrl+e"),
        # ("h.pane.textport.nextword", "cmd+f"),
        # ("h.pane.textport.pageup", "cmd+v"),
        # ("h.pane.textport.pagedown", "ctrl+v"),
        # ("h.pane.textport.firstline", "cmd+shift+,"),
        # ("h.pane.textport.lastline", "cmd+shift+."),
        # ("h.pane.textport.jump_to_line", "alt+g"),
        # ("h.pane.textport.selectup", "ctrl+shift+p"),
        # ("h.pane.textport.selectdown", "ctrl+shift+n"),
        # ("h.pane.textport.selectnext", "ctrl+shift+f"),
        # ("h.pane.textport.selectprev", "ctrl+shift+b"),
        # ("h.pane.textport.selectbottom", "ctrl+shift+e"),
        # ("h.pane.textport.selecttop", "ctrl+shift+a"),
        # ("h.pane.textport.selectnextword", "cmd+shift+f"),
        # ("h.pane.textport.toggle_comment", "ctrl+;"),
        #
        # Text editor vim
        ("h.pane.textport.up", "ctrl+k"),
        ("h.pane.textport.down", "ctrl+j"),
        ("h.pane.textport.next", "ctrl+l"),
        ("h.pane.textport.prev", "ctrl+h"),
        ("h.pane.textport.top", "alt+k"),
        ("h.pane.textport.bottom", "alt+j"),
        ("h.pane.textport.nextword", "ctrl+w"),
        ("h.pane.textport.prevword", "ctrl+b"),
        ("h.pane.textport.pageup", "ctrl+u"),
        ("h.pane.textport.pagedown", "ctrl+d"),
        ("h.pane.textport.firstline", "ctrl+G"),
        ("h.pane.textport.lastline", "ctrl+g"),
        ("h.pane.textport.jump_to_line", "alt+g"),
        ("h.pane.textport.selectup", "ctrl+shift+k"),
        ("h.pane.textport.selectdown", "ctrl+shift+j"),
        ("h.pane.textport.selectnext", "ctrl+shift+l"),
        ("h.pane.textport.selectprev", "ctrl+shift+h"),
        ("h.pane.textport.selectnextword", "ctrl+shift+w"),
        ("h.pane.textport.selectprevword", "ctrl+shift+b"),
        ("h.pane.textport.toggle_comment", "ctrl+/"),
        #
        # Input field
        ("inputfield.down", "ctrl+n"),
        ("inputfield.end", "ctrl+e"),
        ("inputfield.home", "ctrl+a"),
        ("inputfield.next", "ctrl+f"),
        ("inputfield.next_word", "alt+f"),
        ("inputfield.prev", "ctrl+b"),
        ("inputfield.prev_word", "alt+b"),
        ("inputfield.up", "ctrl+p"),
    )

    commands_to_bind = ()

    # System specific
    # if sys == "Darwin":
        # return
    # elif sys == "linux":
        # return

    for assignment in assignments_to_clear:
        context = assignment.rpartition(".")[0]
        symbol = assignment
        hou.hotkeys.clearAssignments(context, symbol)

    for assignment in assignments_to_remove:
        context = assignment[0].rpartition(".")[0]
        symbol = assignment[0]
        key = assignment[1]
        hou.hotkeys.removeAssignment(context, symbol, key)

    for assignment in assignments_to_add:
        context = assignment[0].rpartition(".")[0]
        print(context)
        symbol = assignment[0]
        key = assignment[1]
        hou.hotkeys.addAssignment(context, symbol, key)

    for binding in commands_to_bind:
        context = binding[0]
        command = binding[1]
        hou.hotkeys.addCommandBinding(context, command)
