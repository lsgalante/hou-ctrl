import hou, inspect, platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFrame, QLineEdit, QGridLayout, QLabel, QVBoxLayout, QListWidgetItem, QBoxLayout, QDialog, QListWidget
from PySide2.QtCore import Qt
from fuzzyfinder import fuzzyfinder
import hctl_utils as hcu
from importlib import reload




class filterBox(QLineEdit):
    key_ctl_n = QtCore.Signal()
    key_ctl_p = QtCore.Signal()
    key_down = QtCore.Signal()
    key_up = QtCore.Signal()

    # Input event
    def event(self, event):

        # Key press
        if event.type() == QtCore.QEvent.Type.KeyPress:
            key = event.key()
            mods = event.modifiers()

            # Single keys
            if key == Qt.Key_Up:
                self.key_ctl_p.emit()
                return True
            elif key == Qt.Key_Down:
                self.key_ctl_n.emit()
                return True
            
            # Keys with Modifiers
            else:

                if platform.system() == "Darwin": # macos
                    if key == Qt.Key_N and mods == Qt.MetaModifier:
                        self.key_ctl_n.emit()
                        return True
                    elif key == Qt.Key_P and mods == Qt.MetaModifier:
                        self.key_ctl_p.emit()
                        return True
                else: # linux
                    if key == Qt.Key_N and mods == Qt.ControlModifier:
                        self.key_ctl_n.emit()
                        return True
                    elif key == Qt.Key_P and mods == Qt.ControlModifier:
                        self.key_ctl_p.emit()
                        return True
                    
            return QLineEdit.event(self, event)
        
        else:
            return QLineEdit.event(self, event)

        

class dialog(QDialog):
    def __init__(self):
        super(dialog, self).__init__(hou.qt.mainWindow())
        reload(hcu)

        # States
        self.filePath = hou.hipFile.name()
        self.currentPane = hou.ui.paneUnderCursor()
        self.currentPaneTab = hou.ui.paneTabUnderCursor()
        self.currentNetworkPath = hcu.paneTabGetPath()
        self.currentNode = hcu.paneTabGetCurrentNode()
        self.currentSceneViewer = hcu.paneTabGetSceneViewer()
        self.currentViewport = hcu.paneTabGetCurrentViewport()
        self.currentContext = self.currentPaneTab.type()

        
        ###

        
        # Tab type Menu
        self.tabTypeMenu = QtWidgets.QComboBox()
        tab_types = ["ApexEditor", "DetailsView", "NetworkEditor", "Parm", "PythonPanel", "PythonShell", "SceneViewer", "Textport"]
        self.tabTypeMenu.addItems(tab_types)
        key = str(self.currentContext)
        key = key.lstrip("paneTabType")
        key = key.lstrip(".")
        self.tabTypeMenu.setCurrentIndex(tab_types.index(key))
        self.tabTypeMenu.activated.connect(self.tabTypeChange)

        
        # Autosave
        autoSaveCheckBox = QtWidgets.QCheckBox("Auto Save")
        autoSaveState = hcu.sessionGetAutoSaveState()
        if autoSaveState == "1": autoSaveCheckBox.setCheckState(Qt.Checked)
        elif autoSaveState == "0": autoSaveCheckBox.setCheckState(Qt.Unchecked)
        autoSaveCheckBox.clicked.connect(hcu.sessionToggleAutoSave)

            
        # Pin
        pinCheckBox = QtWidgets.QCheckBox("Pin Tab")
        if self.currentPaneTab.isPin(): pinCheckBox.setCheckState(Qt.Checked)
        else: pinCheckBox.setCheckState(Qt.Unchecked)        
        pinCheckBox.clicked.connect(hcu.paneTabTogglePin)

        
        # Top Frame Layout
        topFrameLayout = QtWidgets.QGridLayout()
        topFrameLayout.addWidget(QLabel("File Path:"),        0, 0)
        topFrameLayout.addWidget(QLabel("Network Path:    "), 1, 0)
        topFrameLayout.addWidget(QLabel("Current Node:"),     2, 0)
        topFrameLayout.addWidget(QLabel("Context:"),          3, 0)
        topFrameLayout.addWidget(autoSaveCheckBox,            4, 0)
        topFrameLayout.addWidget(pinCheckBox,                 5, 0)
        
        topFrameLayout.addWidget(QLabel(self.filePath),           0, 1)
        topFrameLayout.addWidget(QLabel(self.currentNetworkPath), 1, 1)
        topFrameLayout.addWidget(QLabel(str(self.currentNode)),   2, 1)
        topFrameLayout.addWidget(self.tabTypeMenu,                3, 1)

        top_frame_h = 160
        row_h = top_frame_h / 5
        topFrameLayout.setRowMinimumHeight(0, row_h)
        topFrameLayout.setRowMinimumHeight(1, row_h)
        topFrameLayout.setRowMinimumHeight(2, row_h)
        topFrameLayout.setRowMinimumHeight(3, row_h)
        topFrameLayout.setRowMinimumHeight(4, row_h)
        topFrameLayout.setRowMinimumHeight(5, row_h)

        
        # Top frame Widget
        self.topFrame = QFrame()
        self.topFrame.setFrameShape(QFrame.Panel)
        self.topFrame.setLineWidth(1)
        self.topFrame.setLayout(topFrameLayout)
        self.topFrame.setFixedHeight(160)

            
        # Filter Box Widget
        self.filterBox = filterBox() 
        self.filterBox.key_ctl_n.connect( self.listNext )
        self.filterBox.key_ctl_p.connect( self.listPrev )
        self.filterBox.key_down.connect( self.listNext )
        self.filterBox.key_up.connect( self.listPrev )
        self.filterBox.textEdited.connect( self.listFilter )
        self.filterBox.returnPressed.connect( self.execAction )

        
        # Function List
        self.items = []
        # hcu functions
        funcs = inspect.getmembers(hcu)
        for func in funcs:
            name = func[0]
            obj = func[1]
            if hasattr(obj, "interactive_contexts"):
                if "all" in obj.interactive_contexts:
                    self.items.append((name, obj))
                elif str(self.currentContext) in obj.interactive_contexts:
                    self.items.append((name, obj))

                    
        # Function List Widget
        self.functionList = QListWidget()
        for item in self.items:
            self.functionList.addItem(item[0])
        self.functionList.itemClicked.connect(self.execAction)
        self.functionList.setSelectionMode(QListWidget.SingleSelection)
        self.functionList.setFocusPolicy(Qt.StrongFocus)

        
        # Bottom Frame Layout
        bottomFrameLayout = QVBoxLayout()
        bottomFrameLayout.addWidget(self.filterBox)
        bottomFrameLayout.addWidget(self.functionList)

        
        # Bottom Frame
        self.bottomFrame = QFrame()
        self.bottomFrame.setFrameShape(QFrame.Panel)
        self.bottomFrame.setLineWidth(1)
        self.bottomFrame.setLayout(bottomFrameLayout)

        
        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.topFrame)
        self.layout.addWidget(self.bottomFrame)
        self.setLayout(self.layout)
        self.listSetIndex(0)

        
        # Size
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.resize(600, 300)
        self.setWindowTitle("hctl")
        self.filterBox.setFocus()
        
            
    def closeEvent(self, event):
        print("closing")
        self.setParent(None)

        
    def execAction(self):
        items = self.listGetItems()
        currentItem = self.functionList.selectedItems()[0]
        index = items.index(currentItem)
        self.items[index][1]()
        self.accept()

        
    def listFilter(self):
        query = self.filterBox.text()
        items = self.listGetItems()
        item_names = [item.text() for item in items]
        matches = list( fuzzyfinder(query, item_names) )
        for item in items:
            if item.text() in matches:
                item.setHidden(0)    
            else:
                item.setHidden(1)
        self.listSetIndex(0)

        
    def listGetItems(self):
        item_count = self.functionList.count()
        items = [self.functionList.item(i) for i in range(item_count)]
        return(items)

    
    def listGetVisibleItems(self):
        item_count = self.functionList.count()
        items = []
        for i in range(item_count):
            item = self.functionList.item(i)
            if not item.isHidden(): 
                items.append(item)
        return(items)

        
    def listSetIndex(self, index):
        items = self.listGetItems()
        counter = 0
        for item in items:
            if not item.isHidden():
                if counter == index:
                    self.functionList.setItemSelected(item, 1)
                counter += 1

                
    def listNext(self):
        items = self.listGetVisibleItems()
        currentItem = self.functionList.selectedItems()[0]
        index = items.index(currentItem)
        index = (index + 1) % len(items)
        self.listSetIndex(index)

        
    def listPrev(self):
        items = self.listGetVisibleItems()
        currentItem = self.functionList.selectedItems()[0]
        index = items.index(currentItem)
        index = (index - 1) % len(items)
        self.listSetIndex(index)


    def tabTypeChange(self):
        index = self.tabTypeMenu.currentIndex()
        if index == 0:
            self.currentPaneTab = self.currentPaneTab.setType(hou.paneTabType.ApexEditor)
        elif index == 1:
            self.currentPaneTab = self.currentPaneTab.setType(hou.paneTabType.DetailsView)
        elif index == 2:
            self.currentPaneTab = self.currentPaneTab.setType(hou.paneTabType.NetworkEditor)
        elif index == 3:
            self.currentPaneTab = self.currentPaneTab.setType(hou.paneTabType.Parm)            
        elif index == 4:
            self.currentPaneTab = self.currentPaneTab.setType(hou.paneTabType.PythonPanel)
        elif index == 5:
            self.currentPaneTab = self.currentPaneTab.setType(hou.paneTabType.PythonShell)
        elif index == 6:
            self.currentPaneTab = self.currentPaneTab.setType(hou.paneTabType.SceneViewer)
