from functools import partial

from PyQt6 import QtCore
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget

from GUI import windowSingleton
from GUI.docks.DockSeries import DockSeries
from GUI.graphics.GIFExporter import GIFExporter


class AnimationHandler(QWidget):
    animationToggled = pyqtSignal()

    def __init__(self, dockSeries: DockSeries):
        super().__init__(parent = windowSingleton.mainWindow.graphicsView)

        self._speed = 50
        self._dockSeries = dockSeries
        self._currentSeriesIndex = dockSeries.currentSelectedSeriesIndex
        self._timer = QTimer()
        self._timer.timeout.connect(self.updateImage)
        self._currentSeries = None
        self._seriesSize = None
        self._dockSeries.setEnabled(False)
        self.dockSeriesContentChanged()
        self._currentImageIndex = 0
        self._stopped = False
        windowSingleton.mainWindow.graphicsView.setIsAnimationOn(True)
        self.animationToggled.connect(partial(windowSingleton.mainWindow.dicomHandler.toggleGifSlider, self._stopped))
        self.animationToggled.connect(windowSingleton.mainWindow.dicomHandler.changeAnimateActionText)

    def dockSeriesContentChanged(self) -> None:

        if self._currentSeries == windowSingleton.mainWindow.dicomHandler.srcTuplesList[self._currentSeriesIndex][1]:
            self.stopAnimation()
            self.startAnimation()
            return

        self.stopAnimationTimer()
        self._currentSeriesIndex = self._dockSeries.currentSelectedSeriesIndex
        self._currentSeries = windowSingleton.mainWindow.dicomHandler.srcTuplesList[self._currentSeriesIndex][1]
        self._seriesSize = self._currentSeries.seriesSize
        self.startAnimationTimer()

    def startAnimationTimer(self) -> None:
        self._timer.start(self._speed)

    def startAnimation(self) -> None:
        self._dockSeries.setEnabled(False)
        self._stopped = False
        windowSingleton.mainWindow.graphicsView.setIsAnimationOn(True)
        self._currentImageIndex = self._dockSeries.currentPosition
        self.startAnimationTimer()
        self.animationToggled.emit()

    def stopAnimation(self) -> None:
        self._dockSeries.setEnabled(True)
        windowSingleton.mainWindow.graphicsView.setIsAnimationOn(False)
        self.stopAnimationTimer()
        self._stopped = True
        self.animationToggled.emit()

    def stopAnimationTimer(self) -> None:
        self._timer.stop()

    def updateImage(self) -> None:
        if self._currentImageIndex == self._seriesSize:
            self._currentImageIndex = 0

        self._dockSeries.setSelectedItem(self._currentImageIndex)

        windowSingleton.mainWindow.graphicsView.setImageToView(
            DicomContainer = self._currentSeries.getDicomFile(self._currentImageIndex),
            viewMode = windowSingleton.mainWindow.dicomHandler.currentViewMode,
            isFirstImage = False)

        self._currentImageIndex = self._currentImageIndex + 1

    def keyPressEvent(self, qKeyEvent) -> None:
        if qKeyEvent.key() == QtCore.Qt.Key.Key_Return:
            if self._stopped is False:
                self.stopAnimation()
            else:
                self.startAnimation()

    @classmethod
    def prepareGIFExport(cls, data) -> None:
        GIFExporter.setGIFData(data)

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, speed) -> None:
        if speed > 0:
            self._speed = abs(speed - 201)
            self.stopAnimationTimer()
            self.startAnimationTimer()
