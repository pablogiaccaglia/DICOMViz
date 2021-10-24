from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenu


class MenuAlterations(QMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar)
        self.menuBar = menuBar
        self.setObjectName("menuAlterations")

        self.__retranslateUI()

    def __defineActions(self):
        pass

    def __addActions(self):
        pass

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "Alterations"))
