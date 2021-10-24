from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMenu


class MenuTransformations(QMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar)
        self.menuBar = menuBar
        self.setObjectName("menuTransformations")

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    def __defineActions(self):
        self.actionRotate90degreesCCW = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRotate90degreesCCW.setObjectName("actionRotate90degreesCCW")

        self.actionRotate90DegreesCW = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRotate90DegreesCW.setObjectName("actionRotate90DegreesCW")

        self.actionRotate180Degrees = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRotate180Degrees.setObjectName("actionRotate180Degrees")

        self.actionFlipHorizontal = QtWidgets.QWidgetAction(self.menuBar)
        self.actionFlipHorizontal.setObjectName("actionFlipHorizontal")

        self.actionFlip_vertical = QtWidgets.QWidgetAction(self.menuBar)
        self.actionFlip_vertical.setObjectName("actionFlip_vertical")

        self.actionClearTransformations = QtWidgets.QWidgetAction(self.menuBar)
        self.actionClearTransformations.setObjectName("actionClearTransformations")

    def __addActions(self):
        self.addAction(self.actionRotate90degreesCCW)
        self.addAction(self.actionRotate90DegreesCW)
        self.addAction(self.actionRotate180Degrees)

        self.addSeparator()

        self.addAction(self.actionFlipHorizontal)
        self.addAction(self.actionFlip_vertical)

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

        self.actionFlip_vertical.setText(_translate("MainWindow", "Flip vertical"))
        self.actionFlip_vertical.setStatusTip(_translate("MainWindow", "Flip vertical"))
        self.actionFlip_vertical.setShortcut(_translate("MainWindow", "Ctrl+W"))

        self.actionClearTransformations.setText(_translate("MainWindow", "Clear transformations"))
        self.actionClearTransformations.setStatusTip(_translate("MainWindow", "Clear transformations"))
        self.actionClearTransformations.setShortcut(_translate("MainWindow", "Ctrl+Ù"))
