import os
from typing import List
from PyQt6 import QtWidgets
from DICOM.DicomAbstractContainer import ViewMode
from GUI.docks.Dock import Dock


class DockSeries(Dock):

    def __init__(self, window):
        super().__init__("DockSeries", window)
        self.currentSeries = None
        self.currentSeriesIndex = 0
        self.scrollBarPos = 50

    def loadFiles(self, files: List):

        self.listView.clear()
        self.filesList = files

        for fileName in self.filesList:
            item = QtWidgets.QListWidgetItem(os.path.basename(fileName))
            item.setToolTip(fileName)
            self.listView.addItem(item)

        self.listView.setMinimumWidth(self.listView.sizeHintForColumn(0) + 20)

        if self.filesList:
            self.currentSeriesIndex = self.window.dicomHandler.currSelectedSeriesIndex
            self.currentSeries = self.window.dicomHandler.srcList[self.currentSeriesIndex][1][0]
            self.window.dicomHandler.setImageToView(self.currentSeries.dicomFilesList[0], viewMode = ViewMode.ORIGINAL, isFirstImage = True)
            self.setSelectedItem(index = 0)

    def handleItemSelectionChange(self):
        if not len(self.listView.selectedItems()):
            self.window.graphicsView.setImageToView(None, None, None)
        else:
            self.window.dicomHandler.currSelectedSeriesIndex = self.currentSeriesIndex
            self.window.dicomHandler.toggleMenuOptions(True)
            item = self.getCurrentSelectedItem()
            filename = str(item.toolTip())
            self.currentPosition = self.currentSeries.getIndexFromPath(filename)
            self.window.dicomHandler.setImageToView(self.currentSeries.getDicomFileAt(self.currentPosition), self.window.dicomHandler.currentViewMode, isFirstImage = False)

    def setSelectedItem(self, index):
        super().setSelectedItem(index)
        self.currentRowChanged()

    def currentRowChanged(self):
        self.listView.verticalScrollBar().setValue(self.scrollBarPos)
        self.scrollBarPos = self.scrollBarPos + 16.5