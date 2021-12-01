from PyQt6 import QtWidgets, QtCore
from GUI.menus.AbstractMenu import AbstractMenu


class MenuAdjustments(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuAdjustements")

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    def __defineActions(self):
        self.actionDefaultWindow = QtWidgets.QWidgetAction(self.menuBar)
        self.actionDefaultWindow.setObjectName("actionDefaultWindow")

        self.actionFullDynamic = QtWidgets.QWidgetAction(self.menuBar)
        self.actionFullDynamic.setObjectName("actionFullDynamic")

        self.actionCTAbdomen = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCTAbdomen.setObjectName("actionCTAbdomen")

        self.actionCTAngio = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCTAngio.setObjectName("actionCTAngio")

        self.actionCTBone = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCTBone.setObjectName("actionCTBone")

        self.actionCTBrain = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCTBrain.setObjectName("actionCTBrain")

        self.actionCTChest = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCTChest.setObjectName("actionCTChest")

        self.actionCTLungs = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCTLungs.setObjectName("actionCTLungs")

        self.actionNegative = QtWidgets.QWidgetAction(self.menuBar)
        self.actionNegative.setObjectName("actionNegative")

        self.actionCustomWindow = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCustomWindow.setObjectName("actionCustomWindow")

    def __addActions(self):
        self.addAction(self.actionDefaultWindow)
        self.addAction(self.actionFullDynamic)

        self.addSeparator()

        self.addAction(self.actionCTAbdomen)
        self.addAction(self.actionCTAngio)
        self.addAction(self.actionCTBone)
        self.addAction(self.actionCTBrain)
        self.addAction(self.actionCTChest)
        self.addAction(self.actionCTLungs)

        self.addSeparator()

        self.addAction(self.actionNegative)

        self.addSeparator()

        self.addAction(self.actionCustomWindow)

        pass

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "Adjustements"))

        self.actionDefaultWindow.setText(_translate("MainWindow", "Default window"))
        self.actionDefaultWindow.setStatusTip(_translate("MainWindow", "default window"))
        self.actionDefaultWindow.setShortcut(_translate("MainWindow", "0"))

        self.actionFullDynamic.setText(_translate("MainWindow", "Full dynamic"))
        self.actionFullDynamic.setStatusTip(_translate("MainWindow", "full dynamic"))
        self.actionFullDynamic.setShortcut(_translate("MainWindow", "1"))

        self.actionCTAbdomen.setText(_translate("MainWindow", "CT Abdomen"))
        self.actionCTAbdomen.setStatusTip(_translate("MainWindow", "CT Abdomen"))
        self.actionCTAbdomen.setShortcut(_translate("MainWindow", "2"))

        self.actionCTAngio.setText(_translate("MainWindow", "CT Angio"))
        self.actionCTAngio.setStatusTip(_translate("MainWindow", "CT Angio"))
        self.actionCTAngio.setShortcut(_translate("MainWindow", "3"))

        self.actionCTBone.setText(_translate("MainWindow", "CT Bone"))
        self.actionCTBone.setStatusTip(_translate("MainWindow", "CT Bone"))
        self.actionCTBone.setShortcut(_translate("MainWindow", "4"))

        self.actionCTBrain.setText(_translate("MainWindow", "CT Brain"))
        self.actionCTBrain.setStatusTip(_translate("MainWindow", "CT Brain"))
        self.actionCTBrain.setShortcut(_translate("MainWindow", "5"))

        self.actionCTChest.setText(_translate("MainWindow", "CT Chest"))
        self.actionCTChest.setStatusTip(_translate("MainWindow", "CT Chest"))
        self.actionCTChest.setShortcut(_translate("MainWindow", "6"))

        self.actionCTLungs.setText(_translate("MainWindow", "CT Lungs"))
        self.actionCTLungs.setStatusTip(_translate("MainWindow", "CT Lungs"))
        self.actionCTLungs.setShortcut(_translate("MainWindow", "7"))

        self.actionNegative.setText(_translate("MainWindow", "Negative"))
        self.actionNegative.setStatusTip(_translate("MainWindow", "Negative filter"))

        self.actionCustomWindow.setText(_translate("MainWindow", "Custom window"))
        self.actionCustomWindow.setStatusTip(_translate("MainWindow", "Custom window settings"))