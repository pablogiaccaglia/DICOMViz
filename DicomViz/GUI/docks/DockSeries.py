import os
from typing import List
from PyQt6 import QtWidgets
from ...DICOM.DicomAbstractContainer import ViewMode
from .. import windowSingleton
from .Dock import Dock


class DockSeries(Dock):

    def __init__(self, window):
        super().__init__("DockSeries", window)
        self._currentSeriesObject = None
        self.currentSelectedSeriesIndex = 0
        self._scrollBarPos = 50
        self.firstLoad = True

    def loadFiles(self, files: List) -> None:

        self.firstLoad = True

        self._listView.clear()
        self._filesList = files

        if self._filesList:
            self.currentSelectedSeriesIndex = windowSingleton.mainWindow.dicomHandler.currSelectedSeriesIndex
            self._currentSeriesObject = windowSingleton.mainWindow.dicomHandler.currentSeriesObject
            windowSingleton.mainWindow.dicomHandler.currentDicomFileObject = self._currentSeriesObject
            obj = self._currentSeriesObject.getDicomRawImage(index = 0)
            windowSingleton.mainWindow.dicomHandler.setImageToView(obj, viewMode = ViewMode.ORIGINAL, isFirstImage = True)
            self._currentSeriesObject.computeSliceThickness()
            self._currentSeriesObject.loadPixelDataTuple()

        for fileName in self._filesList:
            item = QtWidgets.QListWidgetItem(os.path.basename(fileName))
            item.setToolTip(fileName)
            self._listView.addItem(item)

        self._listView.setMinimumWidth(self._listView.sizeHintForColumn(0) + 20)

    def setSelectedItem(self, index) -> None:
        super().setSelectedItem(index)
        self._currentRowChanged()

    def removeSeriesFiles(self) -> None:
        self._currentSeriesObject = None
        self._scrollBarPos = 50
        self._listView.clear()
        self._filesList = None

    def _currentRowChanged(self) -> None:
        self._listView.verticalScrollBar().setValue(self._scrollBarPos)
        self._scrollBarPos = self._scrollBarPos + 16.5

    def _handleItemSelectionChange(self) -> None:

        if self.firstLoad:
            self.firstLoad = False
            return

        try:
            if not len(self._listView.selectedItems()):
                windowSingleton.mainWindow.graphicsView.setImageToView(None, None, None)
            else:
                windowSingleton.mainWindow.dicomHandler.currentDicomFileObject = self._currentSeriesObject
                windowSingleton.mainWindow.dicomHandler.toggleMenuOptions(True)
                item = self.getCurrentSelectedItem()
                filename = str(item.toolTip())
                self.currentPosition = self._currentSeriesObject.getIndexFromPath(filename)
                windowSingleton.mainWindow.dicomHandler.setImageToView(
                    self._currentSeriesObject.getDicomFile(self.currentPosition),
                    windowSingleton.mainWindow.dicomHandler.currentViewMode,
                    isFirstImage = False)


        except:
            pass
