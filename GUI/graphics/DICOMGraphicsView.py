from enum import Enum

import numpy
from PyQt6.QtGui import QPixmap
from pyqtgraph import ImageItem

from DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
from GUI.graphics.CustomImageView import CustomImageView, TRANSFORMATION

# VIEW MODES
from GUI.graphics.GIFHandler import GIFHandler


class ViewModeBgColor(Enum):
    ORIGINAL = "black"
    LUNGS_MASK = "black"
    SEGMENTED_LUNGS = "w"
    SEGMENTED_LUNGS_W_INTERNAL = "white"
    NEGATIVE = "white"


class DICOMGraphicsView(CustomImageView):

    def __init__(self, window):

        super().__init__(window)
        self.window = window
        self.scene.contextMenuItem = self.view
        self.view.setMenuEnabled(False)
        self.currentViewMode = None
        self.optImageLevels = None
        self.ui.histogram.sigLevelChangeFinished.connect(self.__updateHisto)
        self.ui.slider.valueChanged.connect(self.__sliderValueChange)
        self.ui.gifSlider.valueChanged.connect(self.__gifSliderValueChange)
        self.gifHandler = None
        self.__toggleButtons(value = False)
        self.toggleGifSlider(value = False)
        self.isNegative = False

        from pyqtgraph.GraphicsScene.exportDialog import ExportDialog
        self.scene.exportDialog = ExportDialog(self.scene)

        self.currentBgColor = "black"

    def _setImageToView(self, img, mode: ViewMode, isFirstImage: bool):

        if img is None:  # if the image is None use the default "no image" object
            #  img = self.noImg
            self.clear()
            self.view.setMenuEnabled(False)
            self.view.setBackgroundColor('black')
            self.__toggleButtons(value = False)
            self.__hideActiveSections()
            self.optImageLevels = self._imageLevels
            self.autoLevelsOption = False

            return

        self.__toggleButtons(value = True)

        if mode == ViewMode.ORIGINAL:
            self.ui.sliderButton.setDisabled(True)
            self.ui.sliderGroup.hide()
        else:
            self.ui.sliderButton.setDisabled(False)

        if not (self.isNegative and mode is ViewMode.NEGATIVE):
            self.currentBgColor = ViewModeBgColor[ViewMode(mode).name].value

        self.view.setBackgroundColor(self.currentBgColor)
        self.view.setMenuEnabled(True)
        self.setImage(img.T, autoRange = self.autoRangeOption, autoHistogramRange = self.autoHistogramRangeOption,
                      autoLevels = self.autoLevelsOption, levelMode = 'mono')

        if isFirstImage:
            self.autoLevels()
            self.optImageLevels = self._imageLevels
            self.autoLevelsOption = False
            self.window.dicomHandler.enableNegativeImageAction()

    def setImageToView(self, DicomContainer: 'DicomAbstractContainerClass', viewMode: ViewMode, isFirstImage: bool):
        try:

            if viewMode is not None and viewMode is not ViewMode.NEGATIVE:
                    self.currentViewMode = viewMode

            self.window.setWindowTitle("DICOM Visualizer : " + DicomContainer.filename)

            if viewMode is ViewMode.NEGATIVE:
                self.currentOriginalImageData = DicomContainer.getPixelData(mode = self.currentViewMode)
                self.isNegative = not self.isNegative

            else:
                self.currentOriginalImageData = DicomContainer.getPixelData(mode = viewMode)

            image = self.currentOriginalImageData

            if self.isNegative:
                image = numpy.invert(self.currentOriginalImageData)

            self._setImageToView(img = image, mode = viewMode, isFirstImage = isFirstImage)

            if DicomContainer is not None:
                self.window.dicomHandler.currentShownDicomFileObject = DicomContainer

        except Exception as e:
            print(str(e))
            self._setImageToView(None, ViewMode.ORIGINAL, False)
            self.window.setWindowTitle("DICOM Visualizer: No image")

    def removeImageFromView(self):
        self._setImageToView(None, ViewMode.ORIGINAL, True)

    def __sliderValueChange(self):
        size = self.ui.slider.value()
        dcm = self.window.dicomHandler.currentShownDicomFileObject
        dcm.updateMasks(size - 700)
        self.setImageToView(dcm, self.currentViewMode, isFirstImage = False)

    def __gifSliderValueChange(self):
        speed = self.ui.gifSlider.value()
        self.window.dicomHandler.updateGifSpeedOnDialog(value = speed)

    def __updateHisto(self):
        self.optImageLevels = self._imageLevels

    def __toggleButtons(self, value: bool):

        self.ui.sliderButton.setDisabled(True)

        self.ui.optionsButton.setEnabled(value)
        self.ui.roiBtn.setEnabled(value)
        self.ui.menuBtn.setEnabled(value)
        self.ui.normSubtractRadio.setEnabled(value)
        self.ui.normDivideRadio.setEnabled(value)

    def toggleGifSlider(self, value: bool):
        self.ui.gifSlider.setEnabled(value)

    def toggleGifButton(self, value: bool):
        self.ui.gifButton.setEnabled(value)
        if value:
            self.ui.sliderGroup.hide()

    def addGifHandler(self):
        self.gifHandler = GIFHandler(dockSeries = self.window.seriesFilesDock, graphicsView = self,
                                     handler = self.window.dicomHandler)
        self.gifHandler.start()

    def zoomIn(self):
        self.view.zoomIn()

    def zoomOut(self):
        self.view.zoomOut()

    def setViewSize(self, left, top, width, height):
        self.view.setViewSize(left = left, top = top, width = width, height = height)

    def applyTransformation(self, transformation: TRANSFORMATION):
        self._setImageToView(img = self.executeTransformation(transformation).T, mode = self.currentViewMode,
                             isFirstImage = False)

    def clearTransformations(self):
        self._setImageToView(img = self.currentOriginalImageData, mode = self.currentViewMode, isFirstImage = False)

    def __hideActiveSections(self):
        self.ui.sliderGroup.hide()
        self.ui.optionsGroup.hide()
        self.ui.normGroup.hide()
        self.roi.hide()
        self.normRgn.hide()

    def updateExportDialog(self):
        try:
            self.scene.exportDialog.ui.formatList.clear()
            self.scene.exportDialog.updateFormatList()
        except:
            pass
