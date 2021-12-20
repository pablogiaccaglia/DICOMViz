import os
from typing import List
from PyQt6 import QtWidgets

from DICOM.DicomAbstractContainer import ViewMode
from GUI import windowSingleton
from GUI.docks.Dock import Dock


class DockFiles(Dock):

    def __init__(self, window):
        super().__init__("DockFiles", window)

    def loadFiles(self, files: List) -> None:

        self._listView.clear()

        for file in files:
            dicomFileObject = file
            self._filesList.append(dicomFileObject.filename)

        self._currentPosition = len(self._filesList) - 1

        for fileName in self._filesList:
            item = QtWidgets.QListWidgetItem(os.path.basename(fileName))
            item.setToolTip(fileName)
            self._listView.addItem(item)

        self._listView.setMinimumWidth(self._listView.sizeHintForColumn(0) + 20)

        if self._filesList:
            windowSingleton.mainWindow.dicomHandler.setImageToView(dicomFileObject, viewMode = ViewMode.ORIGINAL, isFirstImage = True)
            self.setSelectedItem(self._currentPosition)

    def _handleItemSelectionChange(self) -> None:
        if not len(self._listView.selectedItems()):
            windowSingleton.mainWindow.graphicsView.setImageToView(None, None, None)
        else:

            item = self.getCurrentSelectedItem()
            filename = str(item.toolTip())
            selectedDicomFileObject = windowSingleton.mainWindow.dicomHandler.srcDicomFileObjectsDict[filename]
            windowSingleton.mainWindow.dicomHandler.currentDicomFileObject = selectedDicomFileObject
            windowSingleton.mainWindow.dicomHandler.toggleMenuOptions(True)

            windowSingleton.mainWindow.dicomHandler.setImageToView(selectedDicomFileObject, windowSingleton.mainWindow.dicomHandler.currentViewMode, isFirstImage = False)
            self.currentPosition = self._listView.indexFromItem(item).column()