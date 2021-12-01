from PyQt6 import QtCore
from GUI.menus.AbstractMenu import AbstractMenu


class MenuAnnotations(AbstractMenu):
    def __init__(self, menuBar):
        super().__init__(menuBar, "menuAnnotations")

        self.__retranslateUI()

    def __defineActions(self):
        pass

    def __addActions(self):
        #  self.menuBar.addAction(self.QMenu.menuAction())
        pass

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "Annotations"))
