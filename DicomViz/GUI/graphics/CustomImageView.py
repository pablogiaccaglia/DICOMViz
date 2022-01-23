from collections import OrderedDict
from functools import partial
from typing import Optional

from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication
from numpy import ndarray
from pyqtgraph.graphicsItems.GradientEditorItem import Gradients
import pyqtgraph

from ...DICOM.DicomAbstractContainer import ViewMode
from ..graphics import imageUtils
from ..graphics.ColorDialog import ColorDialogAction
from ..graphics.CustomViewBox import CustomViewBox
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt

from ..graphics.imageUtils import ROTATION_TRANSFORMATION

translate = QtCore.QCoreApplication.translate


class CustomImageView(pyqtgraph.ImageView):
    """
    Subclass of ImageView
    """

    def __init__(self, parent = None):
        """
        Constructor of the widget
        """
        super(CustomImageView, self).__init__(parent, view = CustomViewBox(imageView = self))
        self._translate = QtCore.QCoreApplication.translate
        self._autoRangeOption = False
        self._autoLevelsOption = True
        self._autoHistogramRangeOption = True
        self._addSliderButtonToImageView()
        self._addOptionsButtonToImageView()
        self._currentOriginalImageData = None
        self.ui.gifSlider.valueChanged.connect(self._updateSliderOptionsValue)
        self._addMoreActionsToImageViewMenu()
        self._addMoreColorMaps()
        self.ui.gifSlider.setEnabled(False)
        self._currentRotationDegrees = 0
        self._isSomeTransformationOn = False
        self._currentActiveRotationTransformation = None
        self._currentActiveFlipTransformation = None
        self._currentEffectiveRotationTransformation = None
        self._settedImage = None
        self._negativeImage = None
        self._isSomeTransformationAlreadyAppliedToCurrentImg = False
        self._backgroundColor = 'black'

    @property
    def isSomeTransformationAlreadyAppliedToCurrentImg(self) -> bool:
        return self._isSomeTransformationAlreadyAppliedToCurrentImg

    @property
    def backgroundColor(self) -> str:
        return self._backgroundColor

    def setBackgroundColor(self, color: str) -> None:
        if color:
            self._backgroundColor = self.changeBgColorAction.color

    @isSomeTransformationAlreadyAppliedToCurrentImg.setter
    def isSomeTransformationAlreadyAppliedToCurrentImg(self, value: bool) -> None:
        self._isSomeTransformationAlreadyAppliedToCurrentImg = value

    @classmethod
    def executeTransformation(cls, image, transformation) -> Optional[ndarray]:

        if image is None:
            return image

        partial_params = transformation.value.partial_params

        if partial_params is not None:
            alteredImage = transformation.value.function(image.T, partial_params[0], partial_params[1])
        else:
            alteredImage = transformation.value.function(image.T)

        return alteredImage.T

    def determineTransformation(self, transformationEnum: ROTATION_TRANSFORMATION) -> None:

            rotationDegreesOfCurrentTransformation = imageUtils.getRotationDegreesFromTransformation(
                    transformation = transformationEnum)
            self._currentRotationDegrees = self._currentRotationDegrees + rotationDegreesOfCurrentTransformation

            if (self._currentRotationDegrees >= 360) or (self._currentRotationDegrees <= -360) or (self._currentRotationDegrees == 0):
                self.clearTransformations()
                self._currentEffectiveRotationTransformation = ROTATION_TRANSFORMATION.ROTATE_0
                return

            transformationTuple = imageUtils.getTransformationFromRotationDegrees(self._currentRotationDegrees)
            transformation = transformationTuple[0]
            self._currentRotationDegrees = transformationTuple[1]

            if transformation is None:
                self.clearTransformations()
                return
            else:
                self._currentEffectiveRotationTransformation = transformation

    def autoRange(self) -> None:
        super(CustomImageView, self).autoRange()
        self.view.resetSize()

    def showExportDialog(self) -> None:
        self.scene.showExportDialog()

    def setBackgroundColorOnSignal(self) -> None:
        self.view.setBackgroundColor(self.changeBgColorAction.color)

    def restoreBackgroundColorOnSignal(self) -> None:
        self.view.setBackgroundColor(self._backgroundColor)

    def getQImage(self) -> Optional[QImage]:
        return self.imageItem.qimage

    def copyImageToClipboard(self) -> None:
        qImage = self.getQImage()
        QApplication.clipboard().setImage(qImage)

    def clearTransformations(self):
        self._isSomeTransformationOn = False
        self._isSomeTransformationAlreadyAppliedToCurrentImg = False
        self._currentActiveRotationTransformation = None
        self._currentEffectiveRotationTransformation = None
        self._currentActiveFlipTransformation = None
        self._currentRotationDegrees = 0
        self._settedImage = self._negativeImage
        self._setImageToView(img = self._currentOriginalImageData, mode = self.currentViewMode, isFirstImage = False)

    def _addMoreColorMaps(self) -> None:

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
            Gradients.update({map_name.lower(): entry})

        self.ui.histogram.gradient.menu.removeAction(self.ui.histogram.gradient.rgbAction)
        self.ui.histogram.gradient.menu.removeAction(self.ui.histogram.gradient.hsvAction)

        for g in self.additionalGradients:
            act = self._createBoxForColorAction(g)
            self.ui.histogram.gradient.menu.addAction(act)

        self.ui.histogram.gradient.menu.addAction(self.ui.histogram.gradient.rgbAction)
        self.ui.histogram.gradient.menu.addAction(self.ui.histogram.gradient.hsvAction)
        self.ui.histogram.gradient.menu.addSeparator()
        self.ui.histogram.gradient.restoreState(Gradients['grey'])

    def _createBoxForColorAction(self, grName) -> QtWidgets.QWidgetAction:
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

    def _setImageToView(self, img, mode: ViewMode, isFirstImage: bool):
        pass

    def _autoHistogramRangeRadioButtonClicked(self) -> None:
        self._autoHistogramRangeOption = self.ui.autoHistogramRangeRadioButton.isChecked()
        if self._autoHistogramRangeOption:
            self.updateImage()

    def _autoRangeRadioButtonClicked(self) -> None:
        self._autoRangeOption = self.ui.autoRangeRadioButton.isChecked()
        if self._autoRangeOption:
            self.autoRange()

    def _autoLevelsRadioButtonClicked(self) -> None:
        self._autoLevelsOption = self.ui.autoLevelsRadioButton.isChecked()
        if self._autoLevelsOption:
            self.autoLevels()

    def _addMoreActionsToImageViewMenu(self) -> None:
        self.buildMenu()
        self._addChangeBackgroundColorActionToImageViewMenu()
        self._addCopyActionToImageViewMenu()

    def _addCopyActionToImageViewMenu(self) -> None:
        self.copyAction = QtGui.QAction(translate("ImageView", "Copy"), self.menu)
        self.copyAction.triggered.connect(self.copyImageToClipboard)
        self.menu.addAction(self.copyAction)

    def _addChangeBackgroundColorActionToImageViewMenu(self) -> None:
        self.changeBgColorAction = ColorDialogAction(translate("ImageView", "Change Background Color"), self.menu)
        self.menu.addAction(self.changeBgColorAction)
        self.changeBgColorAction.colorChangedSignal.connect(self.setBackgroundColorOnSignal)
        self.changeBgColorAction.dialogCancelClickedSignal.connect(self.restoreBackgroundColorOnSignal)
        self.changeBgColorAction.dialogOkClickedSignal.connect(partial(self.setBackgroundColor, self.changeBgColorAction.color))

    def _sliderButtonClicked(self, b) -> None:
        self.ui.sliderGroup.setVisible(b)

    def _optionsButtonClicked(self, b) -> None:
        self.ui.optionsGroup.setVisible(b)

    def _updateSliderOptionsValue(self) -> None:
        self.ui.labelGifSliderValue.setText(self._translate("Form", str(self.ui.gifSlider.value())))

    def _addSliderButtonToImageView(self) -> None:

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
        self.ui.sliderGroup.setTitle(self._translate("Form", "Slider Frame"))

        self.ui.gridLayoutSlider = QtWidgets.QGridLayout(self.ui.sliderGroup)
        self.ui.gridLayoutSlider.setContentsMargins(4, 4, 4, 4)
        self.ui.gridLayoutSlider.setSpacing(0)
        self.ui.gridLayoutSlider.setObjectName("gridLayoutSlider")

        self.ui.slider = QtWidgets.QSlider(parent = self.ui.sliderGroup, orientation = Qt.Orientation.Horizontal)
        self.ui.slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.ui.slider.setRange(400, 700)
        self.ui.slider.setSingleStep(2)
        self.ui.slider.setTickInterval(2)
        self.ui.slider.setValue(630)
        self.ui.slider.setObjectName("slider")

        self.ui.gridLayoutSlider.addWidget(self.ui.slider, 2, 2, 1, 1)
        self.ui.gridLayout_3.addWidget(self.ui.sliderGroup, 15, 0, 1, 1)

        self.ui.sliderButton.setText(self._translate("Form", "Slider"))

        self.ui.sliderGroup.hide()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.ui.sliderButton.clicked.connect(self._sliderButtonClicked)

        self._additionalGradients = None

    def _addOptionsButtonToImageView(self) -> None:

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
        self.ui.gifSlider.setObjectName("gifSlider")
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

        self.ui.labelGifSlider.setText(self._translate("Form", "Animation Speed"))
        self.ui.optionsGroup.hide()

        QtCore.QMetaObject.connectSlotsByName(self)

        self.ui.optionsButton.clicked.connect(self._optionsButtonClicked)
        self.ui.autoHistogramRangeRadioButton.clicked.connect(self._autoHistogramRangeRadioButtonClicked)
        self.ui.autoRangeRadioButton.clicked.connect(self._autoRangeRadioButtonClicked)
        self.ui.autoLevelsRadioButton.clicked.connect(self._autoLevelsRadioButtonClicked)
