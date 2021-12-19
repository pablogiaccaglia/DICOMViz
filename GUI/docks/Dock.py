from functools import partial
from typing import List

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDockWidget, QListWidgetItem

from GUI import windowSingleton


class Dock(QDockWidget):

    def __init__(self, name, window):
        super().__init__(windowSingleton.mainWindow)
        self._filesListWidget = QtWidgets.QWidget()
        self._dockContents = QtWidgets.QWidget()
        self._dockContents.setObjectName(name)

        self._listView = QtWidgets.QListWidget(self._dockContents)
        self._listView.itemSelectionChanged.connect(self._handleItemSelectionChange)
        self._listView.itemSelectionChanged.connect(window.dicomHandler.handleGIFExporter)
        self._listView.itemSelectionChanged.connect(partial(window.dicomHandler.handleDocksClicks, self))
        self._verticalLayout = QtWidgets.QVBoxLayout(self._dockContents)
        self._currentPosition = 0

        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)

        self.setMaximumSize(QtCore.QSize(524287, 524287))
        self.setObjectName("dockWidgetOf" + name)
        self._filesListWidget.setObjectName(name)

        self._verticalLayout.setObjectName("verticalLayoutOf" + name)
        self._listView.setObjectName("listViewOf" + name)
        self._verticalLayout.addWidget(self._listView)
        self.setWidget(self._dockContents)

        self._filesList = []

    def deselectItem(self) -> None:
        try:
            self._listView.item(self._currentPosition).setSelected(False)
        except Exception:
            pass

    def loadFiles(self, files: List) -> None:
        pass

    def setSelectedItem(self, index) -> None:
        self._listView.item(index).setSelected(True)
        self._currentPosition = index

    def isSomethingSelected(self) -> bool:
        return len(self._listView.selectedItems()) > 0

    def getCurrentSelectedItem(self) -> QListWidgetItem:
        return self._listView.selectedItems()[0]

    def unselectCurrentSelected(self) -> None:
        if self.isSomethingSelected():
            self.getCurrentSelectedItem().setSelected(False)

    def _handleItemSelectionChange(self) -> None:
        pass
