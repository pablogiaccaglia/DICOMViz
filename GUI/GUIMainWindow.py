import time

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene
import DICOM
from DICOM.DicomAbstractContainer import ViewMode
from GUI.docks.DockFiles import DockFiles
from GUI.docks.DockSeries import DockSeries
from GUI.menus.MenuBar import MenuBar
from GUI.graphics.DICOMGraphicsView import DICOMGraphicsView
from GUI.containers.TagsGroupBox import TagsGroupBox


class GUIMainWindow(QMainWindow):
    """ Main Window from where all the magic is coordinated :) """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Visualizer")
        self.dicomHandler = DICOM.Handler(self)

        """creation of all Main Window QWidgets"""

        self.centralWidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.graphicsView = DICOMGraphicsView(self)
        self.tagsGroupBox = TagsGroupBox(self.centralWidget)
        self.scene = QGraphicsScene()
        self.menuBar = MenuBar(self)
        self.statusBar = QtWidgets.QStatusBar(self)

        self.seriesFilesDock = DockSeries(self)
        self.singleFilesDock = DockFiles(self)

        self.setupUI()

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
      #  self.horizontalLayout.addWidget(self.tagsGroupBox)

        self.setMenuBar(self.menuBar)
        self.setupDocks()

        self.statusBar.setObjectName("statusbar")
        self.setStatusBar(self.statusBar)
        self.show()

    def setupDocks(self):
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.seriesFilesDock)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singleFilesDock.sizePolicy().hasHeightForWidth())

        self.singleFilesDock.setSizePolicy(sizePolicy)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.singleFilesDock)

    def handleFilesFromFolder(self, folderPath):
        self.dicomHandler.addSource(folderPath)
        time.sleep(30)
        self.seriesFilesDock.loadFiles(self.dicomHandler.currentSeries)
        self.dicomHandler.loadIsComplete = False  # TODO remove this

    def handleSingleFiles(self, filePath):
        self.dicomHandler.addSource(filePath)
        time.sleep(4)
        self.singleFilesDock.loadFiles([self.dicomHandler.srcDicomFileObjectsDict[filePath]])
        self.dicomHandler.loadIsComplete = False  # TODO remove this

    def changeViewMode(self, mode: ViewMode):
        self.dicomHandler.currentViewMode = mode
        self.graphicsView.setImageToView(self.dicomHandler.currentShownDicomFileObject, mode, True)

    def start(self):
        self.show()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.graphicsView.gifHandler.keyPressEvent(a0)
