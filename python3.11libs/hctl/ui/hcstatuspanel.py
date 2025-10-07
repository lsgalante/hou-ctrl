import hou
from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__(hou.qt.mainWindow())
        self.resize(500, 200)
        self.setWindowTitle("hctl status")
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        # Widgets
        self.projectPathLabel = QLabel("Project Path")
        self.networkPathLabel = QLabel("Network Path")
        self.tabTypeLabel = QLabel("Tab Type")

        # Layout
        self.layout =QVBoxLayout()
        self.layout.addWidget(self.projectPathLabel)
        self.layout.addWidget(self.networkPathLabel)
        self.layout.addWidget(self.tabTypeLabel)
        self.layout.addStretch()
        self.setLayout(self.layout)

        self.update()


    def closeEvent(self, event):
        self.setParent(None)


    def lists(self):
        # Arrays for navigating pane tabs
        self.tab_types = (
            hou.paneTabType.ApexEditor,
            hou.paneTabType.CompositorViewer,
            hou.paneTabType.DetailsView,
            hou.paneTabType.NetworkEditor,
            hou.paneTabType.Parm,
            hou.paneTabType.PythonPanel,
            hou.paneTabType.PythonShell,
            hou.paneTabType.SceneViewer,
            hou.paneTabType.Textport
        )

        self.tab_type_names = (
            "ApexEditor",
            "CompositorViewer",
            "DetailsView",
            "NetworkEditor",
            "Parm",
            "PythonPanel",
            "PythonShell",
            "SceneViewer",
            "Textport"
        )

        self.tab_names = [tab.name() for tab in self.hctlSession.tabs()]

        # Populate pane tab labels array
        self.tab_labels = []
        for tab in self.hctlSession.tabs():
            index = self.tab_types.index(tab.type())
            label = self.tab_type_names[index]
            self.tab_labels.append(label)


    def update(self):
        # Labels
        self.projectPathLabel.setText("Project path: " + hou.session.projectPath)
        self.networkPathLabel.setText("Network Path: " + hou.session.networkPath)
        self.tabTypeLabel.setText("Tab type: " + str(hou.session.tabType))
