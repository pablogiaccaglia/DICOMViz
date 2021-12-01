from typing import List

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDockWidget


class Dock(QDockWidget):

    def __init__(self, name, window):
        super().__init__(window)
        self.filesListWidget = QtWidgets.QWidget()
        self.dockContents = QtWidgets.QWidget()
        self.dockContents.setObjectName(name)
        self.listView = QtWidgets.QListWidget(self.dockContents)
        self.listView.itemSelectionChanged.connect(self.handleItemSelectionChange)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockContents)
        self.window = window
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
        except:
            pass

    def loadFiles(self, files: List):
        pass
