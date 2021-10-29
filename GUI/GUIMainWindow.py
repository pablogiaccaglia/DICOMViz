from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene

import DICOM
from GUI.docks.Dock import Dock
from GUI.menus.MenuBar import MenuBar
from GUI.graphics.GraphicsView import GraphicsView


class GUIMainWindow(QMainWindow):
    """ Main Window from where all the magic is coordinated :) """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Viewer")

        """creation of all Main Window QWidgets"""

        self.centralWidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.graphicsView = GraphicsView(self.centralWidget)
        self.scene = QGraphicsScene()
        self.menuBar = MenuBar(self)
        self.statusBar = QtWidgets.QStatusBar(self)

        self.seriesFilesDock = Dock("dockSeriesContents", self)
        self.singleFilesDock = Dock("dockFilesContents", self)

        self.setupUI()
        self.dicomHandler = DICOM.Handler()

    def setupUI(self):
        """ Setup of all created Widgets """

        self.setObjectName("MainWindow")
        self.resize(929, 515)
        self.setMinimumSize(QtCore.QSize(929, 515))
        self.centralWidget.setMaximumSize((QtCore.QSize(2000, 2000)))

        self.centralWidget.setEnabled(True)
        self.centralWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.centralWidget.setAutoFillBackground(True)
        self.centralWidget.setObjectName("centralWidget")

        self.setCentralWidget(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.horizontalLayout.addWidget(self.graphicsView)

        self.setMenuBar(self.menuBar)
        self.setupDocks()

        self.statusBar.setObjectName("statusbar")
        self.setStatusBar(self.statusBar)
        self.show()

    def setupDocks(self):
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.seriesFilesDock.dockWidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singleFilesDock.dockWidget.sizePolicy().hasHeightForWidth())

        self.singleFilesDock.dockWidget.setSizePolicy(sizePolicy)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.singleFilesDock.dockWidget)

    def start(self):
        self.show()
