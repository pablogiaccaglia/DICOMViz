from functools import partial

from PyQt6 import QtCore
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget

from GUI.docks.DockSeries import DockSeries
from GUI.graphics import DICOMGraphicsView
from GUI.graphics.GIFExporter import GIFExporter


class GIFHandler(QWidget):
    animationToggled = pyqtSignal()

    def __init__(self, dockSeries: DockSeries, graphicsView: DICOMGraphicsView, handler):
        super().__init__(parent = graphicsView)
        self.dockSeries = dockSeries
        self.currentSeriesIndex = dockSeries.currentSelectedSeriesIndex
        self.graphicsView = graphicsView
        self.handler = handler
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateImage)
        self.dockSeriesContentChanged()
        self.currentImageIndex = 0
        self.stopped = False
        self.graphicsView.setIsAnimationOn(True)
        self.animationToggled.connect(partial(self.handler.toggleGifSlider, self.stopped))
        self.__speed = 50

    def dockSeriesContentChanged(self):
        self.stopAnimation()
        self.currentSeriesIndex = self.dockSeries.currentSelectedSeriesIndex
        self.currentSeries = self.handler.srcList[self.currentSeriesIndex][1]
        self.seriesSize = self.currentSeries.size

    def startAnimation(self):
        self.timer.start(self.__speed)

    def stopAnimation(self):
        self.timer.stop()

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
                self.graphicsView.setIsAnimationOn(False)
                self.stopAnimation()
                self.stopped = True
                self.animationToggled.emit()
            else:
                self.stopped = False
                self.graphicsView.setIsAnimationOn(True)
                self.currentImageIndex = self.dockSeries.currentPosition
                self.startAnimation()
                self.animationToggled.emit()

    @classmethod
    def prepareGIFExport(cls, data):
        GIFExporter.setGIFData(data)

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        if speed > 0:
            self.__speed = abs(speed - 201)
            self.stopAnimation()
            self.startAnimation()
