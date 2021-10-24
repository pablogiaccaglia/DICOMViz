from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenu


class MenuAnnotations(QMenu):
    def __init__(self, menuBar):
        super().__init__()
        self.menuBar = menuBar
        self.setObjectName("menuAnnotations")

        self.__retranslateUI()

    def __defineActions(self):
        pass

    def __addActions(self):
      #  self.menuBar.addAction(self.QMenu.menuAction())
        pass

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "Annotations"))
