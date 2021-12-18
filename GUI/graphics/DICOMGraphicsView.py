from enum import Enum

import numpy

from DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
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

    def __init__(self, window, fatherWidget):

        super().__init__(fatherWidget)
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
        self.previousMode = None
        self._isAnimationOn = False

        self.scene.exportDialog = ExportDialog(self.scene)

        self.currentBgColor = "black"
        self.bgColorBeforeNegative = None
        self.negativeImage = None

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

        if self.isNegative:
            self.currentBgColor = ViewModeBgColor[ViewMode(mode).name].value
        else:
            if mode != ViewMode.NEGATIVE:
                self.previousMode = mode
            self.currentBgColor = self.bgColorBeforeNegative \
                if self.bgColorBeforeNegative is not None else ViewModeBgColor[ViewMode(self.previousMode).name].value

        if not self.setIsAnimationOn and not self.currentBgColor == 'white':
            self.view.setBackgroundColor(self.currentBgColor)
            self.autoHistogramRangeOption = False

        self.view.setMenuEnabled(True)

        self.settedImage = img

        self.setImage(img.T, autoRange = self.autoRangeOption,
                      autoHistogramRange = self.autoHistogramRangeOption,
                      autoLevels = self.autoLevelsOption, levelMode = 'mono')

        if mode == ViewMode.NEGATIVE and self.previousMode != ViewMode.NEGATIVE:
            self.toggleOnceAutoLevels()

        if isFirstImage:
            self.toggleOnceAutoLevels()
            self.window.dicomHandler.enableNegativeImageAction()
            self.previousMode = mode

    def toggleOnceAutoLevels(self):
        self.autoLevels()
        self.optImageLevels = self._imageLevels
        self.autoLevelsOption = False

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

            if not numpy.array_equal(image, self.negativeImage):
                self.negativeImage = image

            if self.isSomeTransformationOn:
                self.applyTransformations(flipTransformation = self.currentActiveFlipTransformation,
                                          rotationTransformation = self.currentEffectiveRotationTransformation,
                                          image = image)

            else:
                self._setImageToView(img = image, mode = viewMode, isFirstImage = isFirstImage)

            if DicomContainer is not None:
                self.window.dicomHandler.currentShownDicomFileObject = DicomContainer
                self.window.dicomHandler.currentDicomObject = DicomContainer

        except Exception as e:
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
        self.gifHandler.speed = speed

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

    def stopGifHandler(self):
        self.gifHandler.stopAnimation()

    def addGifHandler(self):

        if self.gifHandler:
            self.gifHandler.dockSeriesContentChanged()
            return

        self.gifHandler = GIFHandler(dockSeries = self.window.seriesFilesDock, graphicsView = self,
                                     handler = self.window.dicomHandler)

    def zoomIn(self):
        self.view.zoomIn()

    def zoomOut(self):
        self.view.zoomOut()

    def setViewSize(self, left, top, width, height):
        self.view.setViewSize(left = left, top = top, width = width, height = height)

    def applyRotationTransformations(self, transformation: ROTATION_TRANSFORMATION, image = None,
                                     fromAction: bool = False):

        if transformation is None:
            return None

        if image is None:
            image = self.negativeImage

        self.isSomeTransformationOn = True
        self.currentActiveRotationTransformation = transformation
        self.autoRangeOption = False

        if fromAction:
            self.determineTransformation(transformation)

        if self.currentEffectiveRotationTransformation is None:
            transformedImage = image
        else:
            transformedImage = self.executeTransformation(image, self.currentEffectiveRotationTransformation)

        if transformedImage is None:
            transformedImage = image

        return transformedImage

    def applyFlipTransformation(self, transformation: FLIP_TRANSFORMATION, image = None):

        if transformation is None:
            return

        if image is None:
            image = self.negativeImage

        self.isSomeTransformationOn = True
        self.currentActiveFlipTransformation = transformation
        self.autoRangeOption = False

        transformedImage = self.executeTransformation(image, self.currentActiveFlipTransformation)

        if transformedImage is None:
            transformedImage = image

        return transformedImage

    def applyTransformations(self, flipTransformation: FLIP_TRANSFORMATION = None,
                             rotationTransformation: ROTATION_TRANSFORMATION = None, image = None,
                             fromAction: bool = False):

        print(str(self.isSomeTransformationAlreadyAppliedToCurrentImg))

        if image is None:
            if self.isSomeTransformationAlreadyAppliedToCurrentImg:
                image = self.settedImage
            else:
                image = self.negativeImage

        rotatedImage = self.applyRotationTransformations(transformation = rotationTransformation, image = image,
                                                         fromAction = fromAction)

        if rotatedImage is None:
            if self.isSomeTransformationAlreadyAppliedToCurrentImg:
                imageToFlip = self.settedImage
            else:
                imageToFlip = self.negativeImage
        else:
            imageToFlip = rotatedImage
            self.isSomeTransformationAlreadyAppliedToCurrentImg = True

        flippedImage = self.applyFlipTransformation(transformation = flipTransformation, image = imageToFlip)

        if flippedImage is None:
            imageToSet = imageToFlip
        else:
            imageToSet = flippedImage
            self.isSomeTransformationAlreadyAppliedToCurrentImg = True

        self._setImageToView(img = imageToSet, mode = self.currentViewMode,
                             isFirstImage = False)

        if fromAction:
            self.isSomeTransformationAlreadyAppliedToCurrentImg = True
        else:
            self.isSomeTransformationAlreadyAppliedToCurrentImg = False

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
        except BaseException:
            pass

    def isAnimationOn(self):
        return self._isAnimationOn

    def setIsAnimationOn(self, value):
        self._isAnimationOn = value
