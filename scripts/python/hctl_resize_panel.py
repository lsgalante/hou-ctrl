import hou
import hctl_utils as hcu
from PySide6 import QtCore, QtGui, QtWidgets
from importlib import reload

class resizeWidget(QtWidgets.QDialog):
    def __init__(self, pane):
        super(resizeWidget, self).__init__(hou.qt.mainWindow())
        reload(hcu)

        self.pane = pane

        # Keys
        key_j = QtWidgets.QShortcut(QtGui.QKeySequence("J"), self)
        key_j.activated.connect(self.onJ)
        key_k = QtWidgets.QShortcut(QtGui.QKeySequence("K"), self)
        key_k.activated.connect(self.onK)


        self.paneLabel = QtWidgets.QLabel()
        self.paneLabel.setText("Pane: " + str(pane.currentTab().type()))

        self.isMaximizedLabel = QtWidgets.QLabel()
        self.isMaximizedLabel.setText("Maximized: " + str(pane.isMaximized))

        self.splitFractionLabel = QtWidgets.QLabel()
        self.splitFractionLabel.setText("Split Fraction: " + str(pane.getSplitFraction()))

        self.layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom)
        self.layout.addWidget(self.paneLabel)
        self.layout.addWidget(self.isMaximizedLabel)
        self.layout.addWidget(self.splitFractionLabel)

        self.setLayout(self.layout)


    def onJ(self):
        split_fraction = self.pane.getSplitFraction()
        split_fraction += 0.05
        self.pane.setSplitFraction(split_fraction)
        self.splitFractionLabel.setText("Split Fraction: " + str(split_fraction))


    def onK(self):
        split_fraction = self.pane.getSplitFraction()
        split_fraction -= 0.05
        self.pane.setSplitFraction(split_fraction)
        self.splitFractionLabel.setText("Split Fraction: " + str(split_fraction))
