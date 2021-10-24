from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow

import DICOM
from GUI.menus.MenuBar import MenuBar


class GUIMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.dicomHandler = DICOM.Handler()

    def setupUI(self):
        self.setObjectName("MainWindow")
        self.resize(925, 715)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.setCentralWidget(self.centralWidget)

        self.menuBar = MenuBar(self)
        self.setMenuBar(self.menuBar)

        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusbar")
        self.setStatusBar(self.statusBar)
        self.show()

    def start(self):
        self.show()
