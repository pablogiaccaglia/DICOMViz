import time
from typing import List

import qdarktheme
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QMenu
import DICOM
from DICOM.DicomAbstractContainer import ViewMode
from GUI.containers.SeriesSelection import SeriesSelection
from GUI.containers.TagsContainer import TagsContainer
from GUI.docks.DockFiles import DockFiles
from GUI.docks.DockSeries import DockSeries
from GUI.menus.MenuBar import MenuBar
from GUI.graphics.DICOMGraphicsView import DICOMGraphicsView
from GUI.containers.TagsGroupBox import TagsGroupBox
from GUI.containers.SeriesTableView import SeriesTableView


class GUIMainWindow(QMainWindow):
    """ Main Window from where all the magic is coordinated :) """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Visualizer")

        """creation of all Main Window QWidgets"""

        self.centralWidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.mainGroupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.gridLayoutSeriesAndView = QtWidgets.QGridLayout(self.mainGroupBox)

        self.seriesSelectionSplitter = QtWidgets.QSplitter(self.mainGroupBox)
        self.seriesSelectionSplitter.setOrientation(QtCore.Qt.Orientation.Vertical)

        self.seriesSelectionGroup = QtWidgets.QGroupBox(self.seriesSelectionSplitter)
        self.seriesSelectionGroup.setMaximumSize(QtCore.QSize(16777215, 16777215))

        self.gridLayoutSeriesSelectionGroup = QtWidgets.QGridLayout(self.seriesSelectionGroup)
        self.seriesSelectionWidget = SeriesTableView(self.seriesSelectionGroup)
        self.gridLayoutSeriesSelectionGroup.addWidget(self.seriesSelectionWidget, 0, 0, 1, 1)

        self.seriesSelectionModel = SeriesSelection(columnNames = DICOM.dicom.seriesListColumns)

        self.seriesSelectionWidget.setModel(self.seriesSelectionModel)
        self.seriesSelectionModel.layoutChanged.connect(self.seriesSelectionWidget.resizeColumns)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.seriesSelectionSplitter)

        self.imageViewAndTagshorizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.imageViewAndTagshorizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.imageViewAndTagsSplitter = QtWidgets.QSplitter(self.horizontalLayoutWidget)
        self.imageViewAndTagsSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)

        self.graphicsBox = QtWidgets.QGroupBox(self.imageViewAndTagsSplitter)
        self.gridLayoutGraphicsBox = QtWidgets.QGridLayout(self.graphicsBox)
        self.graphicsView = DICOMGraphicsView(self, self.graphicsBox)
        self.gridLayoutGraphicsBox.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.tagsContainer = TagsContainer(self)
        self.tagsGroupBox = TagsGroupBox(self.imageViewAndTagsSplitter, tagsContainer = self.tagsContainer)

        self.imageViewAndTagshorizontalLayout.addWidget(self.imageViewAndTagsSplitter)
        self.gridLayoutSeriesAndView.addWidget(self.seriesSelectionSplitter, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.mainGroupBox)

        self.statusBar = QtWidgets.QStatusBar(self)
        self.dicomHandler = DICOM.Handler(self)
        self.seriesFilesDock = DockSeries(self)
        self.singleFilesDock = DockFiles(self)
        self.menuBar = MenuBar(window = self)

        self.isDarkStyleOn = True
        self.updateStylesheet()

        self.setupUI()

    def setupUI(self):
        """ Setup of all created Widgets """

        self.setObjectName("MainWindow")
        self.resize(1414, 749)
        self.setMinimumSize(QtCore.QSize(929, 515))
        self.seriesSelectionGroup.resize(QtCore.QSize(200, 50))
        self.graphicsBox.resize(QtCore.QSize(1300, 3000))

        self.__setupCentralWidget()

        self.dicomHandler.menus = self.menuBar.menus
        self.setMenuBar(self.menuBar)
        self.__setupDocks()

        self.statusBar.setObjectName("statusbar")
        self.setStatusBar(self.statusBar)

        self.__setObjectsNames()

        self.__retranslateUI()

        self.show()

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.seriesSelectionGroup.setTitle(_translate("MainWindow", "Series"))
        self.graphicsBox.setTitle(_translate("MainWindow", "DICOM View"))
        self.seriesFilesDock.setWindowTitle(_translate("MainWindow", "Dicom Series Files"))
        self.singleFilesDock.setWindowTitle(_translate("MainWindow", "Dicom Files"))

    def __setupCentralWidget(self):
        self.centralWidget.setMaximumSize((QtCore.QSize(2000, 2000)))
        self.centralWidget.setEnabled(True)
        self.centralWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.centralWidget.setAutoFillBackground(True)
        self.setCentralWidget(self.centralWidget)

    def __setupDocks(self):
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.seriesFilesDock)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singleFilesDock.sizePolicy().hasHeightForWidth())

        self.singleFilesDock.setSizePolicy(sizePolicy)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.singleFilesDock)

    def __setObjectsNames(self):
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainGroupBox.setObjectName("mainGroupBox")
        self.gridLayoutSeriesAndView.setObjectName("gridLayoutSeriesAndView")
        self.seriesSelectionSplitter.setObjectName("gridLayoutSeriesAndViewSplitter")
        self.seriesSelectionGroup.setObjectName("seriesSelectionGroup")
        self.gridLayoutSeriesSelectionGroup.setObjectName("gridLayoutSeriesSelectionGroup")
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.imageViewAndTagshorizontalLayout.setObjectName("horizontalLayout_10")
        self.imageViewAndTagsSplitter.setObjectName("splitter")
        self.graphicsBox.setObjectName("graphicsBox")
        self.gridLayoutGraphicsBox.setObjectName("gridLayout_4")
        self.graphicsView.setObjectName("graphicsView")

    def changeViewMode(self, mode: ViewMode):
        self.dicomHandler.currentViewMode = mode
        self.graphicsView.setImageToView(self.dicomHandler.currentShownDicomFileObject, mode, False)

    def start(self):
        self.show()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.graphicsView.gifHandler is not None:
            self.graphicsView.gifHandler.keyPressEvent(a0)

    def updateStylesheet(self):

        self.isDarkStyleOn = not self.isDarkStyleOn

        if self.isDarkStyleOn:
            self.setStyleSheet(qdarktheme.load_stylesheet(theme = 'light'))

        else:
            self.setStyleSheet(qdarktheme.load_stylesheet(theme = 'dark'))

        self.update()
