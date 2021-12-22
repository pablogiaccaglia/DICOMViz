from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

from ...GUI.menus.MenuAlterations import MenuAlterations
from ...GUI.menus.MenuCine import MenuCine
from ...GUI.menus.MenuExport import MenuExport
from ...GUI.menus.MenuFiles import MenuFiles
from ...GUI.menus.MenuTransformations import MenuTransformations
from ...GUI.menus.MenuZoom import MenuZoom


class MenuBar(QMenuBar):
    def __init__(self, window):
        super().__init__(window)
        self.setObjectName("menubar")
        self.window = window
        self.__initMenuBar()
        self.menus = [self.menuFiles,
                      self.menuExport,
                      self.menuCine,
                      self.menuZoom,
                      self.menuTransformations,
                      self.menuAlterations]
        self._isDarkTheme = True

    def __initMenuBar(self) -> None:

        self.setGeometry(QtCore.QRect(0, 0, 925, 22))

        self.menuFiles = MenuFiles(menuBar = self)
        self.addAction(self.menuFiles.menuAction())

        self.menuExport = MenuExport(menuBar = self)
        self.addAction(self.menuExport.menuAction())

        self.menuZoom = MenuZoom(menuBar = self)
        self.addAction(self.menuZoom.menuAction())

        self.menuAlterations = MenuAlterations(menuBar = self)
        self.addAction(self.menuAlterations.menuAction())

        self.menuTransformations = MenuTransformations(self)
        self.addAction(self.menuTransformations.menuAction())

        self.menuCine = MenuCine(self)
        self.addAction(self.menuCine.menuAction())

        self.actionStyle = QAction(self)
        self.actionStyle.triggered.connect(self.updateStylesheet)
        self.addAction(self.actionStyle)

        self.__retranslateUI()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.actionStyle.setText(_translate("MainWindow", "Light Theme"))

    def updateStylesheet(self) -> None:
        self._isDarkTheme = not self._isDarkTheme

        _translate = QtCore.QCoreApplication.translate
        if self._isDarkTheme:
            self.actionStyle.setText(_translate("MainWindow", "Light Theme"))
        else:
            self.actionStyle.setText(_translate("MainWindow", "Dark Theme"))

        self.window.updateStylesheet()

    @property
    def menus(self) -> list:
        return self._menus

    @menus.setter
    def menus(self, value) -> None:
        self._menus = value
