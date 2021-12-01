import os
from typing import List
from PyQt6 import QtWidgets
from PyQt6.QtCore import QModelIndex

from DICOM.DicomAbstractContainer import ViewMode
from GUI.docks.Dock import Dock


class DockFiles(Dock):

    def __init__(self, window):
        super().__init__("DockFiles", window)

    def loadFiles(self, files: List):

        dicomFileObject = files[0]
        self.listView.clear()
        self.filesList.append(dicomFileObject.filename)
        self.currentPosition = len(self.filesList) - 1

        for fileName in self.filesList:
            item = QtWidgets.QListWidgetItem(os.path.basename(fileName))
            item.setToolTip(fileName)
            self.listView.addItem(item)

        self.listView.setMinimumWidth(self.listView.sizeHintForColumn(0) + 20)

        if self.filesList:
            self.window.dicomHandler.setImageToView(dicomFileObject, viewMode = ViewMode.ORIGINAL, isFirstImage = True)
            self.setSelectedItem(self.currentPosition)

    def handleItemSelectionChange(self):
        if not len(self.listView.selectedItems()):
            self.window.graphicsView.setImageToView(None, None, None)
        else:
            self.window.dicomHandler.toggleMenuOptions(True)
            item = self.getCurrentSelectedItem()
            filename = str(item.toolTip())
            selectedDicomFileObject = self.window.dicomHandler.srcDicomFileObjectsDict[filename]
            self.window.dicomHandler.setImageToView(selectedDicomFileObject, self.window.dicomHandler.currentViewMode, isFirstImage = False)
            self.currentPosition = self.listView.indexFromItem(item).column()