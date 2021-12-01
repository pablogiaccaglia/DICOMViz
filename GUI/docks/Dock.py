from typing import List

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDockWidget, QListWidgetItem


class Dock(QDockWidget):

    def __init__(self, name, window):
        super().__init__(window)
        self.filesListWidget = QtWidgets.QWidget()
        self.dockContents = QtWidgets.QWidget()
        self.dockContents.setObjectName(name)
        self.window = window
        self.listView = QtWidgets.QListWidget(self.dockContents)
        self.listView.itemSelectionChanged.connect(self.handleItemSelectionChange)
        self.listView.itemSelectionChanged.connect(self.window.dicomHandler.handleGIFExporter)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockContents)
        self.currentPosition = 0

        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)

        self.setMaximumSize(QtCore.QSize(524287, 524287))
        self.setObjectName("dockWidgetOf" + name)
        self.filesListWidget.setObjectName(name)

        self.verticalLayout.setObjectName("verticalLayoutOf" + name)
        self.listView.setObjectName("listViewOf" + name)
        self.verticalLayout.addWidget(self.listView)
        self.setWidget(self.dockContents)

        self.filesList = []

    def handleItemSelectionChange(self):
        pass

    def deselectItem(self):
        try:
            self.listView.item(self.currentPosition).setSelected(False)
        except Exception as e:
            pass

    def loadFiles(self, files: List):
        pass

    def setSelectedItem(self, index):
        self.listView.item(index).setSelected(True)
        self.currentPosition = index

    def isSomethingSelected(self) -> bool:
        return len(self.listView.selectedItems()) > 0

    def getCurrentSelectedItem(self) -> QListWidgetItem:
        return self.listView.selectedItems()[0]

    def unselectCurrentSelected(self):
        if self.isSomethingSelected():
            self.getCurrentSelectedItem().setSelected(False)
