from functools import partial

from PyQt6 import QtCore, QtWidgets

from GUI.graphics.CustomImageView import ROTATION_TRANSFORMATION
from GUI.graphics.imageUtils import FLIP_TRANSFORMATION
from GUI.menus.AbstractMenu import AbstractMenu


class MenuTransformations(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuTransformations")
        self.handler = menuBar.window.dicomHandler

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

        self.actions = [self.actionFlipVertical,
                        self.actionFlipHorizontal,
                        self.actionClearTransformations,
                        self.actionRotate90DegreesCW,
                        self.actionRotate180Degrees,
                        self.actionRotate90degreesCCW]

        self.toggleActions(False)

    def __defineActions(self):
        self.actionRotate90degreesCCW = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRotate90degreesCCW.setObjectName("actionRotate90degreesCCW")
        self.actionRotate90degreesCCW.triggered.connect(
            partial(self.handler.applyTransformationToShownImage, ROTATION_TRANSFORMATION.ROTATE_90_CCW))

        self.actionRotate90DegreesCW = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRotate90DegreesCW.setObjectName("actionRotate90DegreesCW")
        self.actionRotate90DegreesCW.triggered.connect(
            partial(self.handler.applyTransformationToShownImage, ROTATION_TRANSFORMATION.ROTATE_90_CW))

        self.actionRotate180Degrees = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRotate180Degrees.setObjectName("actionRotate180Degrees")
        self.actionRotate180Degrees.triggered.connect(
            partial(self.handler.applyTransformationToShownImage, ROTATION_TRANSFORMATION.ROTATE_180))

        self.actionFlipHorizontal = QtWidgets.QWidgetAction(self.menuBar)
        self.actionFlipHorizontal.setObjectName("actionFlipHorizontal")
        self.actionFlipHorizontal.triggered.connect(
            partial(self.handler.applyTransformationToShownImage, FLIP_TRANSFORMATION.FLIP_HORIZONTAL))

        self.actionFlipVertical = QtWidgets.QWidgetAction(self.menuBar)
        self.actionFlipVertical.setObjectName("actionFlip_vertical")
        self.actionFlipVertical.triggered.connect(
            partial(self.handler.applyTransformationToShownImage, FLIP_TRANSFORMATION.FLIP_VERTICAL))

        self.actionClearTransformations = QtWidgets.QWidgetAction(self.menuBar)
        self.actionClearTransformations.setObjectName("actionClearTransformations")
        self.actionClearTransformations.triggered.connect(self.handler.clearTransformationsToShownImage)

    def __addActions(self):
        self.addAction(self.actionRotate90degreesCCW)
        self.addAction(self.actionRotate90DegreesCW)
        self.addAction(self.actionRotate180Degrees)

        self.addSeparator()

        self.addAction(self.actionFlipHorizontal)
        self.addAction(self.actionFlipVertical)

        self.addSeparator()

        self.addAction(self.actionClearTransformations)
        pass

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Transformations"))

        self.actionRotate90degreesCCW.setText(_translate("MainWindow", "Rotate 90° CCW"))
        self.actionRotate90degreesCCW.setStatusTip(_translate("MainWindow", "Rotate 90 degrees counter clock wise"))
        self.actionRotate90degreesCCW.setShortcut(_translate("MainWindow", "Ctrl+Alt+T"))

        self.actionRotate90DegreesCW.setText(_translate("MainWindow", "Rotate 90° CW"))
        self.actionRotate90DegreesCW.setStatusTip(_translate("MainWindow", "Rotate 90 degrees clockwise"))
        self.actionRotate90DegreesCW.setShortcut(_translate("MainWindow", "Meta+Ctrl+T"))

        self.actionRotate180Degrees.setText(_translate("MainWindow", "Rotate 180°"))
        self.actionRotate180Degrees.setStatusTip(_translate("MainWindow", "Rotate 180 degrees clockwise"))
        self.actionRotate180Degrees.setShortcut(_translate("MainWindow", "Ctrl+F"))

        self.actionFlipHorizontal.setText(_translate("MainWindow", "Flip horizontal"))
        self.actionFlipHorizontal.setStatusTip(_translate("MainWindow", "Flip Horizontal"))
        self.actionFlipHorizontal.setShortcut(_translate("MainWindow", "Ctrl+J"))

        self.actionFlipVertical.setText(_translate("MainWindow", "Flip vertical"))
        self.actionFlipVertical.setStatusTip(_translate("MainWindow", "Flip vertical"))
        self.actionFlipVertical.setShortcut(_translate("MainWindow", "Ctrl+W"))

        self.actionClearTransformations.setText(_translate("MainWindow", "Clear transformations"))
        self.actionClearTransformations.setStatusTip(_translate("MainWindow", "Clear transformations"))
        self.actionClearTransformations.setShortcut(_translate("MainWindow", "Ctrl+Ù"))

    def toggleActions(self, value: bool, dicomContainer = None):
        for action in self.actions:
            action.setEnabled(value)

