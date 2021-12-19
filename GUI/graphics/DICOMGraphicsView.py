from enum import Enum
from typing import Optional

import numpy
from numpy import ndarray
from DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
from GUI import windowSingleton
from GUI.graphics.CustomImageView import CustomImageView, ROTATION_TRANSFORMATION
from pyqtgraph.GraphicsScene.exportDialog import ExportDialog

# VIEW MODES
from GUI.graphics.GIFHandler import GIFHandler
from GUI.graphics.imageUtils import FLIP_TRANSFORMATION


class ViewModeBgColor(Enum):
    ORIGINAL = "black"
    LUNGS_MASK = "black"
    SEGMENTED_LUNGS = "w"
    SEGMENTED_LUNGS_W_INTERNAL = "white"
    NEGATIVE = "white"


class DICOMGraphicsView(CustomImageView):

    def __init__(self, fatherWidget):

        super().__init__(fatherWidget)
        self.scene.contextMenuItem = self.view
        self.view.setMenuEnabled(False)
        self._currentViewMode = None
        self._optionImageLevels = None
        self.ui.histogram.sigLevelChangeFinished.connect(self._updateHistogram)
        self.ui.slider.valueChanged.connect(self._sliderValueChange)
        self.ui.gifSlider.valueChanged.connect(self._gifSliderValueChange)
        self._gifHandler = None
        self._toggleButtons(value = False)
        self.toggleGifSlider(value = False)
        self._isNegative = False
        self._previousMode = None
        self._isAnimationOn = False
        self.scene.exportDialog = ExportDialog(self.scene)
        self._currentBgColor = "black"
        self._bgColorBeforeNegative = None
        self._negativeImage = None

    @property
    def currentViewMode(self) -> ViewMode:
        return self._currentViewMode

    @property
    def gifHandler(self):
        return self._gifHandler

    def toggleOnceAutoLevels(self) -> None:
        self.autoLevels()
        self._optionImageLevels = self._imageLevels
        self._autoLevelsOption = False

    def setImageToView(self, DicomContainer: 'DicomAbstractContainerClass', viewMode: ViewMode,
                       isFirstImage: bool) -> None:
        try:

            if viewMode is not None and viewMode is not ViewMode.NEGATIVE:
                self._currentViewMode = viewMode

            windowSingleton.mainWindow.setWindowTitle("DICOM Visualizer : " + DicomContainer.filename)

            if viewMode is ViewMode.NEGATIVE:
                self._currentOriginalImageData = DicomContainer.getPixelData(mode = self._currentViewMode)
                self._isNegative = not self._isNegative

            else:
                self._currentOriginalImageData = DicomContainer.getPixelData(mode = viewMode)

            image = self._currentOriginalImageData

            if self._isNegative:
                image = numpy.invert(self._currentOriginalImageData)

            if not numpy.array_equal(image, self._negativeImage):
                self._negativeImage = image

            if self._isSomeTransformationOn:
                self.applyTransformations(flipTransformation = self._currentActiveFlipTransformation,
                                          rotationTransformation = self._currentEffectiveRotationTransformation,
                                          image = image)

            else:
                self._setImageToView(img = image, mode = viewMode, isFirstImage = isFirstImage)

            if DicomContainer is not None:
                windowSingleton.mainWindow.dicomHandler.currentShownDicomFileObject = DicomContainer
                windowSingleton.mainWindow.dicomHandler.currentDicomFileObject = DicomContainer

        except Exception as e:
            print(str(e))
            print(str(e.__traceback__))
            self._setImageToView(None, ViewMode.ORIGINAL, False)
            windowSingleton.mainWindow.setWindowTitle("DICOM Visualizer: No image")

    def removeImageFromView(self) -> None:
        self._setImageToView(None, ViewMode.ORIGINAL, True)

    def toggleGifSlider(self, value: bool) -> None:
        self.ui.gifSlider.setEnabled(value)

    def toggleGifButton(self, value: bool) -> None:
        self.ui.gifButton.setEnabled(value)

    def stopGifHandler(self) -> None:
        self._gifHandler.stopAnimation()

    def addGifHandler(self) -> None:

        if self._gifHandler:
            self._gifHandler.dockSeriesContentChanged()
            return

        self._gifHandler = GIFHandler(dockSeries = windowSingleton.mainWindow.seriesFilesDock)

    def zoomIn(self) -> None:
        self.view.zoomIn()

    def zoomOut(self) -> None:
        self.view.zoomOut()

    def setViewSize(self, left, top, width, height) -> None:
        self.view.setViewSize(left = left, top = top, width = width, height = height)

    def applyRotationTransformations(self, transformation: ROTATION_TRANSFORMATION, image = None,
                                     fromAction: bool = False) -> Optional[ndarray]:

        if transformation is None:
            return None

        if image is None:
            image = self._negativeImage

        self._isSomeTransformationOn = True
        self._currentActiveRotationTransformation = transformation
        self._autoRangeOption = False

        if fromAction:
            self.determineTransformation(transformation)

        if self._currentEffectiveRotationTransformation is None:
            transformedImage = image
        else:
            transformedImage = self.executeTransformation(image, self._currentEffectiveRotationTransformation)

        if transformedImage is None:
            transformedImage = image

        return transformedImage

    def applyFlipTransformation(self, transformation: FLIP_TRANSFORMATION, image = None) -> Optional[numpy.ndarray]:
        if transformation is None:
            return

        if image is None:
            image = self._negativeImage

        self._isSomeTransformationOn = True
        self._currentActiveFlipTransformation = transformation
        self._autoRangeOption = False

        transformedImage = self.executeTransformation(image, self._currentActiveFlipTransformation)

        if transformedImage is None:
            transformedImage = image

        return transformedImage

    def applyTransformations(self, flipTransformation: FLIP_TRANSFORMATION = None,
                             rotationTransformation: ROTATION_TRANSFORMATION = None, image = None,
                             fromAction: bool = False) -> None:

        if image is None:
            if self._isSomeTransformationAlreadyAppliedToCurrentImg:
                image = self._settedImage
            else:
                image = self._negativeImage

        rotatedImage = self.applyRotationTransformations(transformation = rotationTransformation, image = image,
                                                         fromAction = fromAction)

        if rotatedImage is None:
            if self._isSomeTransformationAlreadyAppliedToCurrentImg:
                imageToFlip = self._settedImage
            else:
                imageToFlip = self._negativeImage
        else:
            imageToFlip = rotatedImage
            self._isSomeTransformationAlreadyAppliedToCurrentImg = True

        flippedImage = self.applyFlipTransformation(transformation = flipTransformation, image = imageToFlip)

        if flippedImage is None:
            imageToSet = imageToFlip
        else:
            imageToSet = flippedImage
            self._isSomeTransformationAlreadyAppliedToCurrentImg = True

        self._setImageToView(img = imageToSet, mode = self._currentViewMode,
                             isFirstImage = False)

        if fromAction:
            self._isSomeTransformationAlreadyAppliedToCurrentImg = True
        else:
            self._isSomeTransformationAlreadyAppliedToCurrentImg = False

    def updateExportDialog(self) -> None:
        try:
            self.scene.exportDialog.ui.formatList.clear()
            self.scene.exportDialog.updateFormatList()
        except Exception:
            pass

    def isAnimationOn(self) -> bool:
        return self._isAnimationOn

    def setIsAnimationOn(self, value) -> None:
        self._isAnimationOn = value

    def _setImageToView(self, img, mode: ViewMode, isFirstImage: bool) -> None:

        if img is None:  # if the image is None use the default "no image" object
            #  img = self.noImg
            self.clear()
            self.view.setMenuEnabled(False)
            self.view.setBackgroundColor('black')
            self._toggleButtons(value = False)
            self._hideActiveSections()
            self._optionImageLevels = self._imageLevels
            self.autoLevelsOption = False

            return

        self._toggleButtons(value = True)

        if mode == ViewMode.ORIGINAL:
            self.ui.sliderButton.setDisabled(True)
            self.ui.sliderGroup.hide()
        else:
            self.ui.sliderButton.setDisabled(False)

        if self._isNegative:
            self._currentBgColor = ViewModeBgColor[ViewMode(mode).name].value
        else:
            if mode != ViewMode.NEGATIVE:
                self._previousMode = mode
            self._currentBgColor = self._bgColorBeforeNegative \
                if self._bgColorBeforeNegative is not None else ViewModeBgColor[ViewMode(self._previousMode).name].value

        if not self._isAnimationOn and not self._currentBgColor == 'white':
            self.view.setBackgroundColor(self._currentBgColor)
            self.autoHistogramRangeOption = False

        self.view.setMenuEnabled(True)

        self._settedImage = img

        self.setImage(img.T, autoRange = self._autoRangeOption,
                      autoHistogramRange = self._autoHistogramRangeOption,
                      autoLevels = self._autoLevelsOption, levelMode = 'mono')

        if mode == ViewMode.NEGATIVE and self._previousMode != ViewMode.NEGATIVE:
            self.toggleOnceAutoLevels()

        if isFirstImage:
            self.toggleOnceAutoLevels()
            windowSingleton.mainWindow.dicomHandler.enableNegativeImageAction()
            self._previousMode = mode

    def _sliderValueChange(self) -> None:
        size = self.ui.slider.value()
        dcm = windowSingleton.mainWindow.dicomHandler.currentShownDicomFileObject
        dcm.updateMasks(size - 700)
        self.setImageToView(dcm, self._currentViewMode, isFirstImage = False)

    def _gifSliderValueChange(self) -> None:
        speed = self.ui.gifSlider.value()
        windowSingleton.mainWindow.dicomHandler.updateGifSpeedOnDialog(value = speed)
        self._gifHandler.speed = speed

    def _updateHistogram(self) -> None:
        self._optionImageLevels = self._imageLevels

    def _toggleButtons(self, value: bool) -> None:

        self.ui.sliderButton.setDisabled(True)

        self.ui.optionsButton.setEnabled(value)
        self.ui.roiBtn.setEnabled(value)
        self.ui.menuBtn.setEnabled(value)
        self.ui.normSubtractRadio.setEnabled(value)
        self.ui.normDivideRadio.setEnabled(value)

    def _hideActiveSections(self) -> None:
        self.ui.sliderGroup.hide()
        self.ui.optionsGroup.hide()
        self.ui.normGroup.hide()
        self.roi.hide()
        self.normRgn.hide()
