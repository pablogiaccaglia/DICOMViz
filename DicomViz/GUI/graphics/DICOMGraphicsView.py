from enum import Enum
from typing import Optional

import numpy
from numpy import ndarray
from ...DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
from .. import windowSingleton
from ..graphics.CustomImageView import CustomImageView, ROTATION_TRANSFORMATION
from pyqtgraph.GraphicsScene.exportDialog import ExportDialog

# VIEW MODES
from ..graphics.AnimationHandler import AnimationHandler
from ..graphics.imageUtils import FLIP_TRANSFORMATION


class ViewModeBgColor(Enum):
    ORIGINAL = "black"
    LUNGS_MASK = "black"
    SEGMENTED_LUNGS = "w"
    SEGMENTED_LUNGS_W_INTERNAL = "#e9e9e9"
    NEGATIVE = "white"


class ViewModeBgColorWhenNegative(Enum):
    ORIGINAL = "white"
    LUNGS_MASK = "white"
    SEGMENTED_LUNGS = "w"
    SEGMENTED_LUNGS_W_INTERNAL = "#151515"
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
        self.ui.gifSlider.valueChanged.connect(self._animationSliderValueChange)
        self._animationHandler = None
        self._toggleButtons(value = False)
        self.toggleGifSlider(value = False)
        self._isNegative = False
        self._previousMode = None
        self._isAnimationOn = False
        self.scene.exportDialog = ExportDialog(self.scene)
        self._currentBgColor = "black"
        self._bgColorBeforeNegative = None
        self._negativeImage = None
        self._settedImageWithoutTransformations = None

    @property
    def currentViewMode(self) -> ViewMode:
        return self._currentViewMode

    @property
    def animationHandler(self):
        return self._animationHandler

    def toggleOnceAutoLevels(self) -> None:
        try:
            self.autoLevels()
            self._optionImageLevels = self._imageLevels
            self._autoLevelsOption = False
        except:
            pass

    def setImageToView(self, DicomContainer: 'DicomAbstractContainerClass', viewMode: ViewMode,
                       isFirstImage: bool) -> None:
        try:

            windowSingleton.mainWindow.setWindowTitle("DICOM Visualizer : " + DicomContainer.filename)

            if viewMode is ViewMode.NEGATIVE:
                imageData = DicomContainer.getPixelData(mode = self._previousMode)
                self._isNegative = not self._isNegative
            else:
                imageData = DicomContainer.getPixelData(mode = viewMode)

            if self._isNegative:
                image = numpy.invert(imageData)
                self._negativeImage = image

            else:
                image = imageData

            self._currentOriginalImageData = imageData

            if viewMode is not self._previousMode:
                isFirstImage = True

            if viewMode is not ViewMode.NEGATIVE:
                self._previousMode = viewMode

            self._settedImageWithoutTransformations = image

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
            self._setImageToView(None, ViewMode.ORIGINAL, False)
            windowSingleton.mainWindow.setWindowTitle("DICOM Visualizer: No image")

    def removeImageFromView(self) -> None:
        self._setImageToView(None, ViewMode.ORIGINAL, True)

    def toggleGifSlider(self, value: bool) -> None:
        self.ui.gifSlider.setEnabled(value)

    def toggleAnimationButton(self, value: bool) -> None:
        self.ui.gifButton.setEnabled(value)

    def stopAnimationHandler(self) -> None:
        self._animationHandler.stopAnimation()

    def addAnimationHandler(self) -> None:

        if self._animationHandler:
            self._animationHandler.dockSeriesContentChanged()
            return

        self._animationHandler = AnimationHandler(dockSeries = windowSingleton.mainWindow.seriesFilesDock)

    def destroyAnimationHandler(self) -> None:

        self._animationHandler.stopAnimation()
        del self._animationHandler

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

            image = self._settedImageWithoutTransformations

            if self._currentEffectiveRotationTransformation is ROTATION_TRANSFORMATION.ROTATE_0:
                transformedImage = None
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
            if self._isSomeTransformationAlreadyAppliedToCurrentImg or self._currentViewMode != ViewMode.NEGATIVE:
                image = self._settedImage
            else:
                image = self._negativeImage

        rotatedImage = self.applyRotationTransformations(transformation = rotationTransformation, image = image,
                                                         fromAction = fromAction)

        if rotatedImage is None:
            # if self._isSomeTransformationAlreadyAppliedToCurrentImg:
            imageToFlip = self._settedImageWithoutTransformations
            # else:
            #    imageToFlip = self._negativeImage
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

        self._isSomeTransformationOn = True

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
            self._currentBgColor = ViewModeBgColorWhenNegative[ViewMode(mode).name].value

        else:
            self._currentBgColor = ViewModeBgColor[ViewMode(self._previousMode).name].value

        if not self._isAnimationOn:
            self.view.setBackgroundColor(self._currentBgColor)
            self.autoHistogramRangeOption = False

        self.view.setMenuEnabled(True)

        self._settedImage = img

        self.setImage(img.T, autoRange = self._autoRangeOption,
                      autoHistogramRange = self._autoHistogramRangeOption,
                      autoLevels = self._autoLevelsOption, levelMode = 'mono')

        self._currentViewMode = mode
        windowSingleton.mainWindow.dicomHandler.currentViewMode = mode

        if isFirstImage:
            self.toggleOnceAutoLevels()
            windowSingleton.mainWindow.dicomHandler.enableNegativeImageAction()

    def _sliderValueChange(self) -> None:
        size = self.ui.slider.value()
        dcm = windowSingleton.mainWindow.dicomHandler.currentShownDicomFileObject
        dcm.updateMasks(size - 700)
        self.setImageToView(dcm, self._currentViewMode, isFirstImage = False)

    def _animationSliderValueChange(self) -> None:
        speed = self.ui.gifSlider.value()
        windowSingleton.mainWindow.dicomHandler.updateGifSpeedOnDialog(value = speed)
        self._animationHandler.speed = speed

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
