import os
from typing import List
from PyQt6 import QtWidgets
from DICOM.DicomAbstractContainer import ViewMode
from GUI.docks.Dock import Dock


class DockSeries(Dock):

    def __init__(self, window):
        super().__init__("DockSeries", window)
        self.currentSeriesObject = None
        self.currentSelectedSeriesIndex = 0
        self.scrollBarPos = 50

    def loadFiles(self, files: List):

        self.listView.clear()
        self.filesList = files

        if self.filesList:
            self.currentSelectedSeriesIndex = self.window.dicomHandler.currSelectedSeriesIndex
            self.currentSeriesObject = self.window.dicomHandler.currentSeriesObject
            self.window.dicomHandler.currentDicomObject = self.currentSeriesObject
            self.window.dicomHandler.setImageToView(self.currentSeriesObject.getFirstDicomRawImage(),
                                                    viewMode = ViewMode.ORIGINAL, isFirstImage = True)
            self.currentSeriesObject.computeSliceThickness()
            self.currentSeriesObject.loadPixelDataTuple()

        for fileName in self.filesList:
            item = QtWidgets.QListWidgetItem(os.path.basename(fileName))
            item.setToolTip(fileName)
            self.listView.addItem(item)

        self.setSelectedItem(index = 0)

        self.listView.setMinimumWidth(self.listView.sizeHintForColumn(0) + 20)

    def handleItemSelectionChange(self):

        try:
            if not len(self.listView.selectedItems()):
                self.window.graphicsView.setImageToView(None, None, None)
            else:
                self.window.dicomHandler.currentDicomObject = self.currentSeriesObject
                self.window.dicomHandler.toggleMenuOptions(True)
                item = self.getCurrentSelectedItem()
                filename = str(item.toolTip())
                self.currentPosition = self.currentSeriesObject.getIndexFromPath(filename)
                self.window.dicomHandler.setImageToView(self.currentSeriesObject.getDicomFileAt(self.currentPosition),
                                                        self.window.dicomHandler.currentViewMode, isFirstImage = False)
        except:
            pass

    def setSelectedItem(self, index):
        super().setSelectedItem(index)
        self.currentRowChanged()

    def currentRowChanged(self):
        self.listView.verticalScrollBar().setValue(self.scrollBarPos)
        self.scrollBarPos = self.scrollBarPos + 16.5

    def removeSeriesFiles(self):
        self.currentSeriesObject = None
        self.scrollBarPos = 50
        self.listView.clear()
        self.filesList = None
