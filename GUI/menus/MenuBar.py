from typing import List

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMenuBar

from GUI.menus import MenuAdjustments
from GUI.menus import MenuAlterations
from GUI.menus import MenuAnnotations
from GUI.menus import MenuCine
from GUI.menus import MenuExport
from GUI.menus import MenuFiles
from GUI.menus import MenuTransformations
from GUI.menus import MenuZoom


class MenuBar(QMenuBar):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.setObjectName("menubar")
        self.__initMenuBar()
        self.menus = [self.menuFiles,
                      self.menuAdjustments,
                      self.menuExport,
                      self.menuCine,
                      self.menuZoom,
                      self.menuAnnotations,
                      self.menuTransformations,
                      self.menuAlterations]

    def __initMenuBar(self):

        self.setGeometry(QtCore.QRect(0, 0, 925, 22))

        self.menuFiles = MenuFiles(self)
        self.addAction(self.menuFiles.menuAction())

        self.menuExport = MenuExport(self)
        self.addAction(self.menuExport.menuAction())

        self.menuAnnotations = MenuAnnotations(self)
        self.addAction(self.menuAnnotations.menuAction())

        self.menuZoom = MenuZoom(self)
        self.addAction(self.menuZoom.menuAction())

        self.menuAlterations = MenuAlterations(self)
        self.addAction(self.menuAlterations.menuAction())

        self.menuAdjustments = MenuAdjustments(self)
        self.addAction(self.menuAdjustments.menuAction())

        self.menuTransformations = MenuTransformations(self)
        self.addAction(self.menuTransformations.menuAction())

        self.menuCine = MenuCine(self)
        self.addAction(self.menuCine.menuAction())

        self.__retranslateUI()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

    @property
    def menus(self) -> List:
        return self._menus

    @menus.setter
    def menus(self, value):
        self._menus = value