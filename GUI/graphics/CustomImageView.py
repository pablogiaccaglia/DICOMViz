from collections import namedtuple
from enum import Enum

import numpy
import pyqtgraph
from PyQt6.QtWidgets import QApplication
from pyqtgraph import GraphicsScene

from GUI.graphics.CustomViewBox import CustomViewBox
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

transformationTuple = namedtuple("transformationTuple", ["function", "partial_params"])
translate = QtCore.QCoreApplication.translate


class TRANSFORMATION(Enum):
    ROTATE_90_CCW = transformationTuple(function = numpy.rot90, partial_params = (1, (1, 0)))
    ROTATE_90_CW = transformationTuple(function = numpy.rot90, partial_params = (1, (0, 1)))
    ROTATE_180 = transformationTuple(function = numpy.rot90, partial_params = (2, (1, 0)))
    FLIP_HORIZONTAL = transformationTuple(function = numpy.fliplr, partial_params = None)
    FLIP_VERTICAL = transformationTuple(function = numpy.flipud, partial_params = None)


class CustomImageView(pyqtgraph.ImageView):
    """
    Subclass of PlotWidget
    """

    def __init__(self, parent = None):
        """
        Constructor of the widget
        """
        super(CustomImageView, self).__init__(parent, view = CustomViewBox(imageView = self))
        self._translate = QtCore.QCoreApplication.translate
        self.autoRangeOption = False
        self.autoLevelsOption = True
        self.autoHistogramRangeOption = True
        self.__addSliderButtonToImageView()
        self.__addOptionsButtonToImageView()
        self.currentOriginalImageData = None
        self.ui.gifSlider.valueChanged.connect(self.__updateSliderOptionsValue)
        self.__addCopyActionToImageViewMenu()

    def executeTransformation(self, transformationEnum: TRANSFORMATION):

        if self.image is None:
            return

        transformation = transformationEnum.value.function
        partial_params = transformationEnum.value.partial_params

        if partial_params is not None:
            alteredImage = transformation(self.image, partial_params[0], partial_params[1])
        else:
            alteredImage = transformation(self.image)

        return alteredImage

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
        self.ui.sliderGroup.setObjectName("sliderGroup")

        self.ui.gridLayoutSlider = QtWidgets.QGridLayout(self.ui.sliderGroup)
        self.ui.gridLayoutSlider.setContentsMargins(0, 0, 0, 0)
        self.ui.gridLayoutSlider.setSpacing(0)
        self.ui.gridLayoutSlider.setObjectName("gridLayoutSlider")

        self.ui.slider = QtWidgets.QSlider(parent = self.ui.sliderGroup, orientation = Qt.Orientation.Horizontal)
        self.ui.slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.ui.slider.setRange(400, 700)
        self.ui.slider.setSingleStep(2)
        self.ui.slider.setTickInterval(2)
        self.ui.slider.setValue(630)
        self.ui.slider.setObjectName("slider")

        self.ui.gridLayoutSlider.addWidget(self.ui.slider, 0, 2, 1, 1)
        self.ui.gridLayout_3.addWidget(self.ui.sliderGroup, 15, 0, 1, 1)

        self.ui.sliderb.setText(self._translate("Form", "Slider"))
        self.ui.sliderGroup.setTitle(self._translate("Form", "Slider Frame"))
        self.ui.sliderGroup.hide()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.ui.sliderb.clicked.connect(self.__sliderButtonClicked)

    def __addOptionsButtonToImageView(self):

        self.ui.optionsButton = QtWidgets.QPushButton(self.ui.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.sliderb.sizePolicy().hasHeightForWidth())
        self.ui.optionsButton.setSizePolicy(sizePolicy)
        self.ui.optionsButton.setCheckable(True)
        self.ui.optionsButton.setObjectName("slider")
        self.ui.gridLayout.addWidget(self.ui.optionsButton, 2, 1, 1, 1)

        self.ui.optionsGroup = QtWidgets.QGroupBox(self)
        self.ui.optionsGroup.setObjectName("optionsGroup")
        self.ui.gridLayout_3.addWidget(self.ui.optionsGroup, 30, 0, 1, 1)
        self.ui.gridLayoutOptions = QtWidgets.QGridLayout(self.ui.optionsGroup)

        self.ui.hboxOptions = QtWidgets.QHBoxLayout(self.ui.optionsGroup)
        self.ui.gridLayoutOptions.addLayout(self.ui.hboxOptions, 0, 0)

        self.ui.hboxOptions.setContentsMargins(0, 0, 0, 0)
        self.ui.hboxOptions.setSpacing(20)
        self.ui.hboxOptions.setObjectName("hboxOptions")

        font = QtGui.QFont()
        font.setBold(True)

        self.ui.labelOptions = QtWidgets.QLabel(self.ui.optionsGroup)
        self.ui.labelOptions.setFont(font)
        self.ui.labelOptions.setObjectName("labelOptions")
        self.ui.hboxOptions.addWidget(self.ui.labelOptions)

        self.ui.autoRangeRadioButton = QtWidgets.QRadioButton(self.ui.optionsGroup)
        self.ui.autoRangeRadioButton.setChecked(False)
        self.ui.autoRangeRadioButton.setObjectName("autoRangeRadioButton")
        self.ui.hboxOptions.addWidget(self.ui.autoRangeRadioButton, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.ui.autoLevelsRadioButton = QtWidgets.QRadioButton(self.ui.optionsGroup)
        self.ui.autoLevelsRadioButton.setChecked(False)
        self.ui.autoLevelsRadioButton.setObjectName("autoLevelsRadioButton")
        self.ui.hboxOptions.addWidget(self.ui.autoLevelsRadioButton, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.ui.autoHistogramRangeRadioButton = QtWidgets.QRadioButton(self.ui.optionsGroup)
        self.ui.autoHistogramRangeRadioButton.setChecked(False)
        self.ui.autoHistogramRangeRadioButton.setObjectName("autoHistogramRangeRadioButton")
        self.ui.hboxOptions.addWidget(self.ui.autoHistogramRangeRadioButton, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.ui.groupAutoLevels = QtWidgets.QButtonGroup()
        self.ui.groupAutoLevels.addButton(self.ui.autoLevelsRadioButton)
        self.ui.groupAutoLevels.setExclusive(False)

        self.ui.groupAutoRange = QtWidgets.QButtonGroup()
        self.ui.groupAutoRange.addButton(self.ui.autoRangeRadioButton)
        self.ui.groupAutoRange.setExclusive(False)

        self.ui.groupAutoHistogramRange = QtWidgets.QButtonGroup()
        self.ui.groupAutoHistogramRange.addButton(self.ui.autoHistogramRangeRadioButton)
        self.ui.groupAutoHistogramRange.setExclusive(False)

        self.ui.hboxSlider = QtWidgets.QHBoxLayout()
        self.ui.gridLayoutOptions.addLayout(self.ui.hboxSlider, 1, 0)

        self.ui.labelGifSlider = QtWidgets.QLabel(self.ui.optionsGroup)

        self.ui.labelGifSlider.setFont(font)
        self.ui.labelGifSlider.setObjectName("labelGifSlider")
        self.ui.hboxSlider.addWidget(self.ui.labelGifSlider)
        self.ui.hboxSlider.setObjectName("hboxSlider")

        self.ui.gifSlider = QtWidgets.QSlider(parent = self.ui.optionsGroup, orientation = Qt.Orientation.Horizontal)
        self.ui.gifSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.ui.gifSlider.setRange(1, 200)
        self.ui.gifSlider.setSingleStep(2)
        self.ui.gifSlider.setTickInterval(2)
        self.ui.gifSlider.setValue(50)
        self.ui.gifSlider.setSliderPosition(50)
        self.ui.gifSlider.setObjectName("test")
        self.ui.hboxSlider.addWidget(self.ui.gifSlider)

        self.ui.labelGifSliderValue = QtWidgets.QLabel(self.ui.optionsGroup)

        self.ui.labelGifSliderValue.setFont(font)
        self.ui.labelGifSliderValue.setObjectName("labelGifSliderValue")
        self.ui.hboxSlider.addWidget(self.ui.labelGifSliderValue)

        self.ui.optionsButton.setText(self._translate("Form", "Options"))
        self.ui.optionsGroup.setTitle(self._translate("Form", "Options Frame"))
        self.ui.labelOptions.setText(self._translate("Form", "Options"))
        self.ui.autoRangeRadioButton.setText(self._translate("Form", "Auto Range"))
        self.ui.autoLevelsRadioButton.setText(self._translate("Form", "Auto Levels"))
        self.ui.autoHistogramRangeRadioButton.setText(self._translate("Form", "Auto Histogram Range"))
        self.ui.labelGifSliderValue.setText(self._translate("Form", str(self.ui.gifSlider.value())))

        self.ui.labelGifSlider.setText(self._translate("Form", "Speed"))
        self.ui.optionsGroup.hide()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.ui.optionsButton.clicked.connect(self.__optionsButtonClicked)
        self.ui.autoHistogramRangeRadioButton.clicked.connect(self.__autoHistogramRangeRadioButtonClicked)
        self.ui.autoRangeRadioButton.clicked.connect(self.__autoRangeRadioButtonClicked)
        self.ui.autoLevelsRadioButton.clicked.connect(self.__autoLevelsRadioButtonClicked)

    def autoRange(self):
        super(CustomImageView, self).autoRange()
        self.view.resetSize()

    def __sliderButtonClicked(self, b):
        self.ui.sliderGroup.setVisible(b)

    def __optionsButtonClicked(self, b):
        self.ui.optionsGroup.setVisible(b)

    def __updateSliderOptionsValue(self):
        self.ui.labelGifSliderValue.setText(self._translate("Form", str(self.ui.gifSlider.value())))

    def showExportDialog(self):
        self.scene.showExportDialog()

    def __autoHistogramRangeRadioButtonClicked(self):
        self.autoHistogramRangeOption = self.ui.autoHistogramRangeRadioButton.isChecked()
        if self.autoHistogramRangeOption:
            self.updateImage()

    def __autoRangeRadioButtonClicked(self):
        self.autoRangeOption = self.ui.autoRangeRadioButton.isChecked()
        if self.autoRangeOption:
            self.autoRange()

    def __autoLevelsRadioButtonClicked(self):
        self.autoLevelsOption = self.ui.autoLevelsRadioButton.isChecked()
        if self.autoLevelsOption:
            self.autoLevels()

    def __addCopyActionToImageViewMenu(self):
        self.buildMenu()
        self.copyAction = QtGui.QAction(translate("ImageView", "Copy"), self.menu)
        self.copyAction.triggered.connect(self.copyImageToClipboard)
        self.menu.addAction(self.copyAction)

    def getQImage(self):
        return self.imageItem.qimage

    def copyImageToClipboard(self):
        qImage = self.getQImage()
        QApplication.clipboard().setImage(qImage)