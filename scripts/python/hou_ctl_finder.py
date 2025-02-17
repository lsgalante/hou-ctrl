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
    def __init__(self):
        super(finder, self).__init__(hou.qt.mainWindow())
        reload(hcu)

        # layout0
        self.layout0 = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)

        # input box
        self.input = line_edit()
        self.input.on_tab.connect(self.change_idx)
        self.input.textEdited.connect(self.filter)
        self.input.returnPressed.connect(self.exec_action)
        self.layout0.addWidget(self.input)

        # context label
        self.context_label = QtWidgets.QLabel()
        self.context_label.setText("Context: " + str(hou.ui.paneTabUnderCursor().type()))
        self.layout0.addWidget(self.context_label)

        # list widget
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.exec_action)

        self.list_widget.addItem("all_menus")
        self.list_widget.addItem("autosave")
        self.list_widget.addItem("dim_unused_nodes")
        self.list_widget.addItem("hide_shelf")
        self.list_widget.addItem("hotkey_editor")
        self.list_widget.addItem("main_menubar")
        self.list_widget.addItem("network_menubar")
        self.list_widget.addItem("overlay")
        self.list_widget.addItem("panetabs")
        self.list_widget.addItem("path")
        self.list_widget.addItem("point_markers")
        self.list_widget.addItem("reload_color_schemes")
        self.list_widget.addItem("rename_node")
        self.list_widget.addItem("show_shelf")
        self.list_widget.addItem("stowbars")
        self.list_widget.addItem("trigger_update")
        self.list_widget.addItem("update_main_menubar")
        self.list_widget.addItem("update_mode_auto")
        self.list_widget.addItem("update_mode_manual")
        self.list_widget.addItem("vectors")
        self.list_widget.addItem("viewer_toolbars")
        self.layout0.addWidget(self.list_widget) 

        # layout1

        #self.autosave_b = QtWidgets.QCheckBox("autosave")
        #self.autosave_b.setChecked(int(hcu.get_autosave_state()))
        #self.autosave_b.stateChanged.connect(hcu.toggle_autosave)
        #self.button_arr.append("autosave")
        #self.layout1.addWidget(self.autosave_b)

        ## apply final layout
        self.setLayout(self.layout0)
        self.set_selection(0)

    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

    def exec_action(self):
        current_item = self.list_widget.selectedItems()[0].text()
        if   current_item == "all_menus":            hcu.toggle_all_menus()
        elif current_item == "dim_unused_nodes":     hcu.toggle_dim_unused_nodes()
        elif current_item == "hide_shelf":           hcu.hide_shelf()
        elif current_item == "hotkey_editor":        hcu.open_hotkey_editor()
        elif current_item == "main_menubar":         hcu.toggle_main_menubar()
        elif current_item == "network_controls":     hcu.toggle_network_controls()
        elif current_item == "network_menubar":      hcu.toggle_network_menubar()
        elif current_item == "overlay":              self.overlay()
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
        self.accept()

    def change_idx(self):
        item = self.list_widget.selectedItems()[0]
        idx = self.list_widget.indexFromItem(item).row()
        self.set_selection(idx + 1)

    def set_selection(self, idx):
        ct = self.list_widget.count()
        items = [self.list_widget.item(i) for i in range(ct)]
        ctr = 0
        for item in items:
            if not item.isHidden():
                if ctr == idx:
                    self.list_widget.setItemSelected(item, 1)
                ctr += 1

    def filter(s):
        text = self.input.text()
        ct = self.list_widget.count()
        items = [self.list_widget.item(i) for i in range(ct)]
        names = [item.text() for item in items]
        suggestions = fuzzyfinder(text, names)
        suggestions = list(suggestions)
        for item in items:
            if item.text() in suggestions:
                item.setHidden(0)    
                ct += 1
            else:
                item.setHidden(1)
        self.set_selection(0)
                
    def overlay(s):
        print("overlay")
