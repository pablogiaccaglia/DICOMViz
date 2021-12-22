from functools import partial

from PyQt6 import QtCore, QtWidgets

from ..graphics.CustomImageView import ROTATION_TRANSFORMATION
from ..graphics.imageUtils import FLIP_TRANSFORMATION
from ..menus.AbstractMenu import AbstractMenu


class MenuTransformations(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuTransformations")
        self.handler = menuBar.window.dicomHandler

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

        self.actions = [self._actionFlipVertical,
                        self._actionFlipHorizontal,
                        self._actionClearTransformations,
                        self._actionRotate90DegreesCW,
                        self._actionRotate180Degrees,
                        self._actionRotate90degreesCCW]

        self.toggleActions(False)

    def toggleActions(self, value: bool, dicomContainer = None) -> None:
        for action in self.actions:
            action.setEnabled(value)

    def __defineActions(self) -> None:
        self._actionRotate90degreesCCW = QtWidgets.QWidgetAction(self.menuBar)
        self._actionRotate90degreesCCW.setObjectName("actionRotate90degreesCCW")
        self._actionRotate90degreesCCW.triggered.connect(
                partial(self.handler.applyTransformationToShownImage, ROTATION_TRANSFORMATION.ROTATE_90_CCW))

        self._actionRotate90DegreesCW = QtWidgets.QWidgetAction(self.menuBar)
        self._actionRotate90DegreesCW.setObjectName("actionRotate90DegreesCW")
        self._actionRotate90DegreesCW.triggered.connect(
                partial(self.handler.applyTransformationToShownImage, ROTATION_TRANSFORMATION.ROTATE_90_CW))

        self._actionRotate180Degrees = QtWidgets.QWidgetAction(self.menuBar)
        self._actionRotate180Degrees.setObjectName("actionRotate180Degrees")
        self._actionRotate180Degrees.triggered.connect(
                partial(self.handler.applyTransformationToShownImage, ROTATION_TRANSFORMATION.ROTATE_180))

        self._actionFlipHorizontal = QtWidgets.QWidgetAction(self.menuBar)
        self._actionFlipHorizontal.setObjectName("actionFlipHorizontal")
        self._actionFlipHorizontal.triggered.connect(
                partial(self.handler.applyTransformationToShownImage, FLIP_TRANSFORMATION.FLIP_HORIZONTAL))

        self._actionFlipVertical = QtWidgets.QWidgetAction(self.menuBar)
        self._actionFlipVertical.setObjectName("actionFlip_vertical")
        self._actionFlipVertical.triggered.connect(
                partial(self.handler.applyTransformationToShownImage, FLIP_TRANSFORMATION.FLIP_VERTICAL))

        self._actionClearTransformations = QtWidgets.QWidgetAction(self.menuBar)
        self._actionClearTransformations.setObjectName("actionClearTransformations")
        self._actionClearTransformations.triggered.connect(self.handler.clearTransformationsToShownImage)

    def __addActions(self) -> None:
        self.addAction(self._actionRotate90degreesCCW)
        self.addAction(self._actionRotate90DegreesCW)
        self.addAction(self._actionRotate180Degrees)

        self.addSeparator()

        self.addAction(self._actionFlipHorizontal)
        self.addAction(self._actionFlipVertical)

        self.addSeparator()

        self.addAction(self._actionClearTransformations)
        pass

    def __retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Transformations"))

        self._actionRotate90degreesCCW.setText(_translate("MainWindow", "Rotate 90° CCW"))
        self._actionRotate90degreesCCW.setStatusTip(_translate("MainWindow", "Rotate 90 degrees counter clock wise"))
        # self._actionRotate90degreesCCW.setShortcut(_translate("MainWindow", "Ctrl+Alt+T"))

        self._actionRotate90DegreesCW.setText(_translate("MainWindow", "Rotate 90° CW"))
        self._actionRotate90DegreesCW.setStatusTip(_translate("MainWindow", "Rotate 90 degrees clockwise"))
        # self._actionRotate90DegreesCW.setShortcut(_translate("MainWindow", "Meta+Ctrl+T"))

        self._actionRotate180Degrees.setText(_translate("MainWindow", "Rotate 180°"))
        self._actionRotate180Degrees.setStatusTip(_translate("MainWindow", "Rotate 180 degrees clockwise"))
        # self._actionRotate180Degrees.setShortcut(_translate("MainWindow", "Ctrl+F"))

        self._actionFlipHorizontal.setText(_translate("MainWindow", "Flip horizontal"))
        self._actionFlipHorizontal.setStatusTip(_translate("MainWindow", "Flip Horizontal"))
        # self._actionFlipHorizontal.setShortcut(_translate("MainWindow", "Ctrl+J"))

        self._actionFlipVertical.setText(_translate("MainWindow", "Flip vertical"))
        self._actionFlipVertical.setStatusTip(_translate("MainWindow", "Flip vertical"))
        # self._actionFlipVertical.setShortcut(_translate("MainWindow", "Ctrl+W"))

        self._actionClearTransformations.setText(_translate("MainWindow", "Clear transformations"))
        self._actionClearTransformations.setStatusTip(_translate("MainWindow", "Clear transformations"))
        # self._actionClearTransformations.setShortcut(_translate("MainWindow", "Ctrl+Ù"))
