from enum import Enum

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

from DICOM import DicomAbstractContainer
from DICOM.DicomAbstractContainer import ViewMode
from GUI.graphics.CustomImageView import CustomImageView
import pyqtgraph


# VIEW MODES
class ViewModeBgColor(Enum):
    ORIGINAL = "black"
    LUNGS_MASK = "black"
    SEGMENTED_LUNGS = "white"
    SEGMENTED_LUNGS_W_INTERNAL = "white"


class DICOMGraphicsView(CustomImageView):

    def __init__(self, window):

        super().__init__(window)
        self.window = window
        self.currentImageData = None
        self.scene.contextMenuItem = self.view
        self.view.setMenuEnabled(False)
        self.__addSliderButtonToImageView()
        self.currentViewMode = None

    def _setImageToView(self, img, mode: ViewMode):

        if img is None:  # if the image is None use the default "no image" object
            #  img = self.noImg
            self.view.setMenuEnabled(False)
            self.view.setBackgroundColor('black')
            return

        bgColor = ViewModeBgColor[ViewMode(mode).name]
        self.view.setBackgroundColor(bgColor.value)
        self.view.setMenuEnabled(True)
        self.setImage(img.T, autoHistogramRange = False, autoRange=True, autoLevels=True)

    def setImageToView(self, DicomContainer: 'DicomAbstractContainer', viewMode: ViewMode,
                       index = None):
        try:
            if viewMode is not None:
                self.currentViewMode = viewMode

            if DicomContainer.getInstanceType() == "DicomSeries":
                self.window.setWindowTitle("DICOM Visualizer : " + DicomContainer.dicomFilesList[index].filename)
                self.currentImageData = DicomContainer.getPixelData(index = index, mode = viewMode)
                self._setImageToView(self.currentImageData, viewMode)
                self.window.dicomHandler.currentShownDicomFileObject = DicomContainer.getDicomFileAt(index)

            elif DicomContainer.getInstanceType() == "DicomFile":
                self.window.setWindowTitle("DICOM Visualizer : " + DicomContainer.filename)
                self.currentImageData = DicomContainer.getPixelData(mode = viewMode)
                self._setImageToView(self.currentImageData, viewMode)
                self.window.dicomHandler.currentShownDicomFileObject = DicomContainer
            else:
                raise Exception


        except Exception as exc:
            print(exc)
            self._setImageToView(None, viewMode.ORIGINAL)
            self.window.setWindowTitle("DICOM Visualizer: No image")

    def showExportDialog(self):
        self.scene.showExportDialog()

    def __addSliderButtonToImageView(self):

        self.ui.sliderb = QtWidgets.QPushButton(self.ui.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ui.sliderb.sizePolicy().hasHeightForWidth())
        self.ui.sliderb.setSizePolicy(sizePolicy)
        self.ui.sliderb.setCheckable(True)
        self.ui.sliderb.setObjectName("slider")
        self.ui.gridLayout.addWidget(self.ui.sliderb, 2, 2, 1, 1)

        self.ui.sliderGroup = QtWidgets.QGroupBox(self)
        self.ui.sliderGroup.setObjectName("normGroup")

        self.ui.gridLayoutSlider = QtWidgets.QGridLayout(self.ui.sliderGroup)
        self.ui.gridLayoutSlider.setContentsMargins(0, 0, 0, 0)
        self.ui.gridLayoutSlider.setSpacing(0)
        self.ui.gridLayoutSlider.setObjectName("gridLayoutSlider")

        self.ui.test = QtWidgets.QSlider(parent = self.ui.sliderGroup, orientation = Qt.Orientation.Horizontal)
        self.ui.test.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.ui.test.setRange(400, 700)
        self.ui.test.setSingleStep(2)
        self.ui.test.setTickInterval(2)
        self.ui.test.setValue(630)
        self.ui.test.valueChanged.connect(self.__valueChange)
        self.ui.test.setObjectName("test")

        self.ui.gridLayoutSlider.addWidget(self.ui.test, 0, 2, 1, 1)
        self.ui.gridLayout_3.addWidget(self.ui.sliderGroup, 1, 0, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        self.ui.sliderb.setText(_translate("Form", "Slider"))
        self.ui.sliderGroup.setTitle(_translate("Form", "Slider Frame"))
        self.ui.sliderGroup.hide()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.ui.sliderb.clicked.connect(self.__sliderToggled)

    def __sliderToggled(self, b):
        self.ui.sliderGroup.setVisible(b)

    def __valueChange(self):
        size = self.ui.test.value()
        dcm = self.window.dicomHandler.currentShownDicomFileObject
        dcm.updateMasks(size - 700)
        self.setImageToView(dcm, self.currentViewMode)
