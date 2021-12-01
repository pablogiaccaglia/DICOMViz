from collections import namedtuple
from enum import Enum

import numpy
import pyqtgraph
from GUI.graphics.CustomViewBox import CustomViewBox
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

transformationTuple = namedtuple("transformationTuple", ["function", "partial_params"])


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
        super(CustomImageView, self).__init__(parent, view = CustomViewBox())
        self.autoRangeOption = False
        self.autoLevelsOption = True
        self.autoHistogramRangeOption = True
        self.__addSliderButtonToImageView()
        self.__addOptionsButtonToImageView()
        self.currentOriginalImageData = None

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

        self.ui.test = QtWidgets.QSlider(parent = self.ui.sliderGroup, orientation = Qt.Orientation.Horizontal)
        self.ui.test.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.ui.test.setRange(400, 700)
        self.ui.test.setSingleStep(2)
        self.ui.test.setTickInterval(2)
        self.ui.test.setValue(630)
        self.ui.test.setObjectName("test")

        self.ui.gridLayoutSlider.addWidget(self.ui.test, 0, 2, 1, 1)
        self.ui.gridLayout_3.addWidget(self.ui.sliderGroup, 15, 0, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        self.ui.sliderb.setText(_translate("Form", "Slider"))
        self.ui.sliderGroup.setTitle(_translate("Form", "Slider Frame"))
        self.ui.sliderGroup.hide()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.ui.sliderb.clicked.connect(self.__sliderButtonClicked)

    def __addOptionsButtonToImageView(self):
        self.ui.optionsButton = QtWidgets.QPushButton(self.ui.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ui.sliderb.sizePolicy().hasHeightForWidth())
        self.ui.optionsButton.setSizePolicy(sizePolicy)
        self.ui.optionsButton.setCheckable(True)
        self.ui.optionsButton.setObjectName("slider")
        self.ui.gridLayout.addWidget(self.ui.optionsButton, 2, 1, 1, 1)

        self.ui.optionsGroup = QtWidgets.QGroupBox(self)
        self.ui.optionsGroup.setObjectName("optionsGroup")
        self.ui.gridLayout_3.addWidget(self.ui.optionsGroup, 30, 0, 1, 1)

        self.ui.gridLayoutOptions = QtWidgets.QGridLayout(self.ui.optionsGroup)
        self.ui.gridLayoutOptions.setContentsMargins(0, 0, 0, 0)
        self.ui.gridLayoutOptions.setSpacing(0)
        self.ui.gridLayoutOptions.setObjectName("gridLayoutOptions")

        self.ui.autoRangeRadioButton = QtWidgets.QRadioButton(self.ui.optionsGroup)
        self.ui.autoRangeRadioButton.setChecked(False)
        self.ui.autoRangeRadioButton.setObjectName("autoRangeRadioButton")
        self.ui.gridLayoutOptions.addWidget(self.ui.autoRangeRadioButton, 0, 1, 1, 1)
        self.ui.labelOptions = QtWidgets.QLabel(self.ui.optionsGroup)

        self.ui.autoLevelsRadioButton = QtWidgets.QRadioButton(self.ui.optionsGroup)
        self.ui.autoLevelsRadioButton.setChecked(False)
        self.ui.autoLevelsRadioButton.setObjectName("autoLevelsRadioButton")
        self.ui.gridLayoutOptions.addWidget(self.ui.autoLevelsRadioButton, 0, 2, 1, 1)

        self.ui.autoHistogramRangeRadioButton = QtWidgets.QRadioButton(self.ui.optionsGroup)
        self.ui.autoHistogramRangeRadioButton.setChecked(False)
        self.ui.autoHistogramRangeRadioButton.setObjectName("autoHistogramRangeRadioButton")
        self.ui.gridLayoutOptions.addWidget(self.ui.autoHistogramRangeRadioButton, 0, 3, 1, 1)

        self.ui.groupAutoLevels = QtWidgets.QButtonGroup()
        self.ui.groupAutoLevels.addButton(self.ui.autoLevelsRadioButton)
        self.ui.groupAutoLevels.setExclusive(False)

        self.ui.groupAutoRange = QtWidgets.QButtonGroup()
        self.ui.groupAutoRange.addButton(self.ui.autoRangeRadioButton)
        self.ui.groupAutoRange.setExclusive(False)

        self.ui.groupAutoHistogramRange = QtWidgets.QButtonGroup()
        self.ui.groupAutoHistogramRange.addButton(self.ui.autoHistogramRangeRadioButton)
        self.ui.groupAutoHistogramRange.setExclusive(False)

        font = QtGui.QFont()
        font.setBold(True)
        self.ui.labelOptions.setFont(font)
        self.ui.labelOptions.setObjectName("labelOptions")
        self.ui.gridLayoutOptions.addWidget(self.ui.labelOptions, 0, 0, 1, 1)

        _translate = QtCore.QCoreApplication.translate
        self.ui.optionsButton.setText(_translate("Form", "Options"))
        self.ui.optionsGroup.setTitle(_translate("Form", "Options Frame"))
        self.ui.labelOptions.setText(_translate("Form", "Options"))
        self.ui.autoRangeRadioButton.setText(_translate("Form", "Auto Range"))
        self.ui.autoLevelsRadioButton.setText(_translate("Form", "Auto Levels"))
        self.ui.autoHistogramRangeRadioButton.setText(_translate("Form", "Auto Histogram Range"))

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
