from collections import namedtuple, OrderedDict
from enum import Enum
from functools import partial

import numpy
import pyqtgraph
from PyQt6.QtWidgets import QApplication
from pyqtgraph.graphicsItems.GradientEditorItem import Gradients

from GUI.graphics.ColorDialog import ColorAction
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
        self.__addMoreActionsToImageViewMenu()
        self.__addMoreColorMaps()

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

        self.ui.sliderButton = QtWidgets.QPushButton(self.ui.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.ui.sliderButton.sizePolicy().hasHeightForWidth())
        self.ui.sliderButton.setSizePolicy(sizePolicy)
        self.ui.sliderButton.setCheckable(True)
        self.ui.sliderButton.setObjectName("slider")
        self.ui.gridLayout.addWidget(self.ui.sliderButton, 2, 2, 1, 1)

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

        self.ui.sliderButton.setText(self._translate("Form", "Slider"))
        self.ui.sliderGroup.setTitle(self._translate("Form", "Slider Frame"))
        self.ui.sliderGroup.hide()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.ui.sliderButton.clicked.connect(self.__sliderButtonClicked)

        self.__additionalGradients = None

    def __addOptionsButtonToImageView(self):

        self.ui.optionsButton = QtWidgets.QPushButton(self.ui.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui.sliderButton.sizePolicy().hasHeightForWidth())
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

    def __addMoreActionsToImageViewMenu(self):
        self.buildMenu()
        self.__addChangeBackgroundColorActionToImageViewMenu()
        self.__addCopyActionToImageViewMenu()

    def __addCopyActionToImageViewMenu(self):
        self.copyAction = QtGui.QAction(translate("ImageView", "Copy"), self.menu)
        self.copyAction.triggered.connect(self.copyImageToClipboard)
        self.menu.addAction(self.copyAction)

    def __addChangeBackgroundColorActionToImageViewMenu(self):
        self.changeBgColorAction = ColorAction(translate("ImageView", "Change Background Color"), self.menu)
        self.menu.addAction(self.changeBgColorAction)

        self.changeBgColorAction.colorChangedSignal.connect(self.setBackgroundColorOnSignal)

    def setBackgroundColorOnSignal(self):
        self.view.setBackgroundColor(self.changeBgColorAction.color)

    def getQImage(self):
        return self.imageItem.qimage

    def copyImageToClipboard(self):
        qImage = self.getQImage()
        QApplication.clipboard().setImage(qImage)

    def __addMoreColorMaps(self):

        self.additionalGradients = OrderedDict()
        list_of_maps = pyqtgraph.colormap.listMaps('matplotlib')
        list_of_maps = sorted(list_of_maps, key = lambda x: x.lower())

        for map_name in list_of_maps:
            cm = pyqtgraph.colormap.get(map_name, source = 'matplotlib', skipCache = True)

            entry = {
                'ticks': [],
                'mode':  'rgb'
            }

            stops = cm.getStops()

            for i in range(len(stops)):
                entry['ticks'].append((stops[0][i], tuple(stops[1][i])))

            self.additionalGradients.update({map_name.lower(): entry})

        self.ui.histogram.gradient.menu.removeAction(self.ui.histogram.gradient.rgbAction)
        self.ui.histogram.gradient.menu.removeAction(self.ui.histogram.gradient.hsvAction)

        for g in self.additionalGradients:
            act = self.__createBoxForColorAction(g)
            self.ui.histogram.gradient.menu.addAction(act)

        self.ui.histogram.gradient.menu.addAction(self.ui.histogram.gradient.rgbAction)
        self.ui.histogram.gradient.menu.addAction(self.ui.histogram.gradient.hsvAction)
        self.ui.histogram.gradient.menu.addSeparator()
        self.ui.histogram.gradient.restoreState(Gradients['grey'])

    def __createBoxForColorAction(self, grName) -> QtWidgets.QWidgetAction:
        px = QtGui.QPixmap(100, 15)
        p = QtGui.QPainter(px)
        self.ui.histogram.gradient.restoreState(self.additionalGradients[grName])
        grad = self.ui.histogram.gradient.getGradient()
        brush = QtGui.QBrush(grad)
        p.fillRect(QtCore.QRect(0, 0, 100, 15), brush)
        p.end()
        label = QtWidgets.QLabel()
        label.setPixmap(px)
        label.setContentsMargins(1, 1, 1, 1)
        labelName = QtWidgets.QLabel(grName)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(labelName)
        hbox.addWidget(label)
        widget = QtWidgets.QWidget()
        widget.setLayout(hbox)
        act = QtWidgets.QWidgetAction(self.ui.histogram.gradient)
        act.setDefaultWidget(widget)
        act.triggered.connect(self.ui.histogram.gradient.contextMenuClicked)
        act.name = grName

        return act
