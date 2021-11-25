from PyQt6.QtCore import QTimer

from DICOM import Handler
from DICOM.DicomSeries import DicomSeries
from GUI.graphics import DICOMGraphicsView


class GIFHandler:

    def __init__(self, currentSeries: DicomSeries, currentSeriesIndex: int, graphicsView: DICOMGraphicsView,
                 handler: Handler):
        self.currentSeries = currentSeries
        self.currentSeriesIndex = currentSeriesIndex
        self.seriesSize = self.currentSeries.size
        self.graphicsView = graphicsView
        self.handler = handler
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateImage)

    def start(self):
        self.timer.start(50)

    def updateImage(self):
        if self.currentSeriesIndex == self.seriesSize:
            self.currentSeriesIndex = 0

        self.graphicsView.setImageToView(DicomContainer = self.currentSeries.getDicomFileAt(self.currentSeriesIndex),
                                         viewMode = self.handler.currentViewMode,
                                         isFirstImage = False)
        self.currentSeriesIndex = self.currentSeriesIndex + 1
