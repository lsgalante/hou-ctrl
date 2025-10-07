import hou
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QLabel, QShortcut, QBoxLayout


class HCResizePanel(QtWidgets.QDialog):
    def __init__(self, pane):
        super(HCResizePanel, self).__init__(hou.qt.mainWindow())

        self.pane = pane

        # Keys
        key_j = QShortcut(QtGui.QKeySequence("J"), self)
        key_j.activated.connect(self.onJ)
        key_k = QShortcut(QtGui.QKeySequence("K"), self)
        key_k.activated.connect(self.onK)


        self.paneLabel = QLabel()
        self.paneLabel.setText("Pane: " + str(pane.currentTab().type()))

        self.isMaximizedLabel = QLabel()
        self.isMaximizedLabel.setText("Maximized: " + str(pane.isMaximized))

        self.splitFractionLabel = QLabel()
        self.splitFractionLabel.setText("Split Fraction: " + str(pane.getSplitFraction()))

        self.layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
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
