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

        self.pane_label = QLabel()
        self.pane_label.setText("Pane: " + str(pane.currentTab().type()))

        self.is_maximized_label = QLabel()
        self.is_maximized_label.setText("Maximized: " + str(pane.isMaximized))

        self.split_fraction_label = QLabel()
        self.split_lraction_label.setText("Split Fraction: " + str(pane.getSplitFraction()))

        self.layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.layout.addWidget(self.pane_label)
        self.layout.addWidget(self.is_maximized_label)
        self.layout.addWidget(self.split_fraction_label)

        self.setLayout(self.layout)

    def onJ(self):
        split_fraction = self.pane.getSplitFraction()
        split_fraction += 0.05
        self.pane.setSplitFraction(split_fraction)
        self.split_fraction_label.setText("Split Fraction: " + str(split_fraction))

    def onK(self):
        split_fraction = self.pane.getSplitFraction()
        split_fraction -= 0.05
        self.pane.setSplitFraction(split_fraction)
        self.split_fraction_label.setText("Split Fraction: " + str(split_fraction))
