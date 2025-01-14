import hou
from PySide2 import QtCore, QtGui, QtWidgets
from fuzzyfinder import fuzzyfinder
import hou_ctl_utils as hcu
from importlib import reload
#import os

class line_edit(QtWidgets.QLineEdit):
    on_tab = QtCore.Signal()
    def event(self, event):
        if event.type() == QtCore.QEvent.Type.KeyPress and event.key() == QtCore.Qt.Key_Tab:
            self.on_tab.emit()
            return True
        else:
            return QtWidgets.QLineEdit.event(self, event)


class finder(QtWidgets.QDialog):
    def __init__(s):
        super(finder, s).__init__(hou.qt.mainWindow())
        reload(hcu)

        ####
        # layout0
        s.layout0 = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)

        # input box
        s.input = line_edit()
        s.input.on_tab.connect(s.change_idx)
        s.input.textEdited.connect(s.fltr)
        s.input.returnPressed.connect(s.exec_action)
        s.layout0.addWidget(s.input)

        # list widget
        s.list_widget = QtWidgets.QListWidget()
        s.list_widget.itemClicked.connect(s.exec_action)

        s.list_widget.addItem("all_menus")
        s.list_widget.addItem("autosave")
        s.list_widget.addItem("dim_unused_nodes")
        s.list_widget.addItem("hide_shelf")
        s.list_widget.addItem("hotkey_editor")
        s.list_widget.addItem("main_menubar")
        s.list_widget.addItem("network_menubar")
        s.list_widget.addItem("overlay")
        s.list_widget.addItem("panetabs")
        s.list_widget.addItem("path")
        s.list_widget.addItem("point_markers")
        s.list_widget.addItem("reload_color_schemes")
        s.list_widget.addItem("rename_node")
        s.list_widget.addItem("show_shelf")
        s.list_widget.addItem("stowbars")
        s.list_widget.addItem("trigger_update")
        s.list_widget.addItem("update_main_menubar")
        s.list_widget.addItem("update_mode_auto")
        s.list_widget.addItem("update_mode_manual")
        s.list_widget.addItem("vectors")
        s.list_widget.addItem("viewer_toolbars")
        s.layout0.addWidget(s.list_widget) 

        # layout1

        #s.autosave_b = QtWidgets.QCheckBox("autosave")
        #s.autosave_b.setChecked(int(hcu.get_autosave_state()))
        #s.autosave_b.stateChanged.connect(hcu.toggle_autosave)
        #s.button_arr.append("autosave")
        #s.layout1.addWidget(s.autosave_b)

        ## apply final layout
        s.setLayout(s.layout0)
        s.set_selection(0)

    def closeEvent(s, event):
        print("closing")
        s.setParent(None)

    def exec_action(s):
        current_item = s.list_widget.selectedItems()[0].text()
        if current_item == "all_menus":               hcu.toggle_all_menus()
        elif current_item == "dim_unused_nodes":     hcu.toggle_dim_unused_nodes()
        elif current_item == "hide_shelf":           hcu.hide_shelf()
        elif current_item == "hotkey_editor":        hcu.open_hotkey_editor()
        elif current_item == "main_menubar":         hcu.toggle_main_menubar()
        elif current_item == "network_controls":     hcu.toggle_network_controls()
        elif current_item == "network_menubar":      hcu.toggle_network_menubar()
        elif current_item == "overlay":              s.overlay()
        elif current_item == "panetabs":             hcu.toggle_panetabs()
        elif current_item == "point_markers":        hcu.toggle_point_markers()
        elif current_item == "reload_color_schemes": hcu.reload_color_schemes()
        elif current_item == "rename_node":          hcu.rename_node()
        elif current_item == "show_shelf":           hcu.show_shelf()
        elif current_item == "stowbars":             hcu.toggle_stowbars()
        elif current_item == "trigger_update":       hcu.trigger_update()
        elif current_item == "update_main_menubar":  hcu.update_main_menubar()
        elif current_item == "update_mode_auto":     hcu.update_mode_auto()
        elif current_item == "update_mode_manual":   hcu.update_mode_manual()
        elif current_item == "vectors":              hcu.toggle_vectors()
        elif current_item == "viewer_toolbars":      hcu.toggle_viewer_toolbars()

    def change_idx(s):
        item = s.list_widget.selectedItems()[0]
        idx = s.list_widget.indexFromItem(item).row()
        s.set_selection(idx + 1)

    def set_selection(s, idx):
        ct = s.list_widget.count()
        items = [s.list_widget.item(i) for i in range(ct)]
        ctr = 0
        for item in items:
            if not item.isHidden():
                if ctr == idx:
                    s.list_widget.setItemSelected(item, 1)
                ctr += 1

    def fltr(s):
        text = s.input.text()
        ct = s.list_widget.count()
        items = [s.list_widget.item(i) for i in range(ct)]
        names = [item.text() for item in items]
        suggestions = fuzzyfinder(text, names)
        suggestions = list(suggestions)
        for item in items:
            if item.text() in suggestions:
                item.setHidden(0)    
                ct += 1
            else:
                item.setHidden(1)
        s.set_selection(0)
                
    def overlay(s):
        print("overlay")
