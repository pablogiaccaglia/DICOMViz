from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget

from GUI.docks.DockSeries import DockSeries
from GUI.graphics import DICOMGraphicsView
from GUI.graphics.GIFExporter import GIFExporter


class GIFHandler(QWidget):

    def __init__(self, dockSeries: DockSeries, graphicsView: DICOMGraphicsView, handler):
        super().__init__(parent = graphicsView)
        self.dockSeries = dockSeries
        self.currentSeriesIndex = dockSeries.currentSeriesIndex
        self.graphicsView = graphicsView
        self.handler = handler
        self.currentSeries = self.handler.srcList[self.currentSeriesIndex][1][0]
        self.seriesSize = self.currentSeries.size
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateImage)
        self.currentImageIndex = 0
        self.stopped = False
        self.graphicsView.isAnimationOn = True

    def start(self):
        self.timer.start(50)

    def updateImage(self):
        if self.currentImageIndex == self.seriesSize:
            self.currentImageIndex = 0

        self.dockSeries.setSelectedItem(self.currentImageIndex)

        self.graphicsView.setImageToView(DicomContainer = self.currentSeries.getDicomFileAt(self.currentImageIndex),
                                         viewMode = self.handler.currentViewMode,
                                         isFirstImage = False)

        self.currentImageIndex = self.currentImageIndex + 1

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key.Key_Return:
            if self.stopped is False:
                self.graphicsView.isAnimationOn = False
                self.timer.stop()
                self.stopped = True
            else:
                self.stopped = False
                self.graphicsView.isAnimationOn = True
                self.currentImageIndex = self.dockSeries.currentPosition
                self.start()

    @classmethod
    def prepareGIFExport(cls, data):
        GIFExporter.setGIFData(data)