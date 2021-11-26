from enum import Enum

from DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
from GUI.graphics.CustomImageView import CustomImageView

# VIEW MODES
from GUI.graphics.GIFHandler import GIFHandler


class ViewModeBgColor(Enum):
    ORIGINAL = "black"
    LUNGS_MASK = "black"
    SEGMENTED_LUNGS = "w"
    SEGMENTED_LUNGS_W_INTERNAL = "white"


class DICOMGraphicsView(CustomImageView):

    def __init__(self, window):

        super().__init__(window)
        self.window = window
        self.currentImageData = None
        self.scene.contextMenuItem = self.view
        self.view.setMenuEnabled(False)
        self.currentViewMode = None
        self.optImageLevels = None
        self.ui.histogram.sigLevelChangeFinished.connect(self.__updateHisto)
        self.ui.test.valueChanged.connect(self.__valueChange)
        self.gifHandler = None
        self.ui.sliderb.setDisabled(True)
        self.ui.sliderGroup.hide()

    def _setImageToView(self, img, mode: ViewMode, isFirstImage: bool):

        if img is None:  # if the image is None use the default "no image" object
            #  img = self.noImg
            self.view.setMenuEnabled(False)
            self.view.setBackgroundColor('black')
            return

        if mode == ViewMode.ORIGINAL:
            self.ui.sliderb.setDisabled(True)
            self.ui.sliderGroup.hide()
        else:
            self.ui.sliderb.setDisabled(False)

        bgColor = ViewModeBgColor[ViewMode(mode).name]

        self.view.setBackgroundColor(bgColor.value)
        self.view.setMenuEnabled(True)
        self.setImage(img.T, autoRange = self.autoRangeOption, autoHistogramRange = self.autoHistogramRangeOption,
                      autoLevels = self.autoLevelsOption, levelMode = 'mono')

        if isFirstImage:
            self.autoLevels()
            self.optImageLevels = self._imageLevels
            self.autoLevelsOption = False

    def setImageToView(self, DicomContainer: 'DicomAbstractContainerClass', viewMode: ViewMode, isFirstImage: bool):
        try:
            if viewMode is not None:
                self.currentViewMode = viewMode

            self.window.setWindowTitle("DICOM Visualizer : " + DicomContainer.filename)
            self.currentImageData = DicomContainer.getPixelData(mode = viewMode)
            self._setImageToView(img = self.currentImageData, mode = viewMode, isFirstImage = isFirstImage)

            if DicomContainer is not None:
                self.window.dicomHandler.currentShownDicomFileObject = DicomContainer

        except Exception as exc:
            print(exc)
            self._setImageToView(None, viewMode.ORIGINAL, False)
            self.window.setWindowTitle("DICOM Visualizer: No image")

    def __valueChange(self):
        size = self.ui.test.value()
        dcm = self.window.dicomHandler.currentShownDicomFileObject
        dcm.updateMasks(size - 700)
        self.setImageToView(dcm, self.currentViewMode, isFirstImage = False)

    def __updateHisto(self):
        self.optImageLevels = self._imageLevels

    def addGifHandler(self):
            self.gifHandler = GIFHandler(self.window.seriesFilesDock, self, self.window.dicomHandler)
            self.gifHandler.start()

