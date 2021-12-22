import qdarktheme
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow
from pyqtgraph.exporters import Exporter
from pyqtgraph.exporters import MatplotlibExporter
from DicomViz import DICOM
from DicomViz.DICOM.DicomAbstractContainer import ViewMode
from ..GUI.containers.SeriesSelection import SeriesSelection
from ..GUI.containers.TagsContainer import TagsContainer
from ..GUI.docks.DockFiles import DockFiles
from ..GUI.docks.DockSeries import DockSeries
from ..GUI.menus.MenuBar import MenuBar
from ..GUI.graphics.DICOMGraphicsView import DICOMGraphicsView
from ..GUI.containers.TagsGroupBox import TagsGroupBox
from ..GUI.containers.SeriesTableView import SeriesTableView


class GUIMainWindow(QMainWindow):
    """ Main Window from where all the magic is coordinated :) """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DICOM Visualizer")

        """creation of all Main Window QWidgets"""

        self._centralWidget = QtWidgets.QWidget(self)
        self._horizontalLayout = QtWidgets.QHBoxLayout(self._centralWidget)
        self._mainGroupBox = QtWidgets.QGroupBox(self._centralWidget)
        self._gridLayoutSeriesAndView = QtWidgets.QGridLayout(self._mainGroupBox)

        self._seriesSelectionSplitter = QtWidgets.QSplitter(self._mainGroupBox)
        self._seriesSelectionSplitter.setOrientation(QtCore.Qt.Orientation.Vertical)

        self.seriesSelectionGroup = QtWidgets.QGroupBox(self._seriesSelectionSplitter)
        self.seriesSelectionGroup.setMaximumSize(QtCore.QSize(16777215, 16777215))

        self._gridLayoutSeriesSelectionGroup = QtWidgets.QGridLayout(self.seriesSelectionGroup)
        self.seriesSelectionWidget = SeriesTableView(self.seriesSelectionGroup)
        self._gridLayoutSeriesSelectionGroup.addWidget(self.seriesSelectionWidget, 0, 0, 1, 1)

        self.seriesSelectionModel = SeriesSelection(columnNames = DICOM.dicom.seriesListColumns)

        self.seriesSelectionWidget.setModel(self.seriesSelectionModel)
        self.seriesSelectionModel.layoutChanged.connect(self.seriesSelectionWidget.resizeColumns)

        self._horizontalLayoutWidget = QtWidgets.QWidget(self._seriesSelectionSplitter)

        self._imageViewAndTagsHorizontalLayout = QtWidgets.QHBoxLayout(self._horizontalLayoutWidget)
        self._imageViewAndTagsHorizontalLayout.setContentsMargins(0, 0, 0, 0)

        self._imageViewAndTagsSplitter = QtWidgets.QSplitter(self._horizontalLayoutWidget)
        self._imageViewAndTagsSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)

        self._graphicsBox = QtWidgets.QGroupBox(self._imageViewAndTagsSplitter)
        self._gridLayoutGraphicsBox = QtWidgets.QGridLayout(self._graphicsBox)
        self.graphicsView = DICOMGraphicsView(self._graphicsBox)
        self._gridLayoutGraphicsBox.addWidget(self.graphicsView, 0, 0, 1, 1)

        self._tagsContainer = TagsContainer(self)
        self.tagsGroupBox = TagsGroupBox(self._imageViewAndTagsSplitter, tagsContainer = self._tagsContainer)

        self._imageViewAndTagsHorizontalLayout.addWidget(self._imageViewAndTagsSplitter)
        self._gridLayoutSeriesAndView.addWidget(self._seriesSelectionSplitter, 0, 0, 1, 1)
        self._horizontalLayout.addWidget(self._mainGroupBox)

        self.dicomHandler = DICOM.Handler()
        self.seriesFilesDock = DockSeries(self)
        self.singleFilesDock = DockFiles(self)
        self.menuBar = MenuBar(self)

        self.isDarkStyleOn = True
        self.updateStylesheet()
        self.seriesSelectionWidget.clicked.connect(self.dicomHandler.seriesClicked)

        self.setupUI()

    def setupUI(self):
        """ Setup of all created Widgets """

        self.setObjectName("MainWindow")
        self.resize(1414, 749)
        self.setMinimumSize(QtCore.QSize(929, 515))
        self.seriesSelectionGroup.resize(QtCore.QSize(200, 50))
        self._graphicsBox.resize(QtCore.QSize(1300, 3000))

        self.__setupCentralWidget()

        self.dicomHandler.menus = self.menuBar.menus
        self.setMenuBar(self.menuBar)
        self.__setupDocks()

        self.__setObjectsNames()

        self.__retranslateUI()

        self.__removeUnsupportedExportFormats()
        self.show()

    def start(self):
        self.show()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if self.graphicsView.animationHandler is not None:
            self.graphicsView.animationHandler.keyPressEvent(a0)

    def updateStylesheet(self):

        self.isDarkStyleOn = not self.isDarkStyleOn

        if self.isDarkStyleOn:
            self.setStyleSheet(qdarktheme.load_stylesheet(theme = 'light'))

        else:
            self.setStyleSheet(qdarktheme.load_stylesheet(theme = 'dark'))

        self.update()

    def changeViewMode(self, mode: ViewMode):

        if self.dicomHandler.currentViewMode is ViewMode.NEGATIVE and mode is ViewMode.NEGATIVE:
            mode = ViewMode.ORIGINAL

        self.dicomHandler.currentViewMode = mode
        self.graphicsView.setImageToView(self.dicomHandler.currentShownDicomFileObject, mode, False)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.seriesSelectionGroup.setTitle(_translate("MainWindow", "Series"))
        self._graphicsBox.setTitle(_translate("MainWindow", "DICOM View"))
        self.seriesFilesDock.setWindowTitle(_translate("MainWindow", "Dicom Series Files"))
        self.singleFilesDock.setWindowTitle(_translate("MainWindow", "Dicom Files"))

    def __setupCentralWidget(self):
        self._centralWidget.setMaximumSize((QtCore.QSize(2000, 2000)))
        self._centralWidget.setEnabled(True)
        self._centralWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._centralWidget.setAutoFillBackground(True)
        self.setCentralWidget(self._centralWidget)

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
        self._centralWidget.setObjectName("centralWidget")
        self._horizontalLayout.setObjectName("horizontalLayout")
        self._mainGroupBox.setObjectName("mainGroupBox")
        self._gridLayoutSeriesAndView.setObjectName("gridLayoutSeriesAndView")
        self._seriesSelectionSplitter.setObjectName("gridLayoutSeriesAndViewSplitter")
        self.seriesSelectionGroup.setObjectName("seriesSelectionGroup")
        self._gridLayoutSeriesSelectionGroup.setObjectName("gridLayoutSeriesSelectionGroup")
        self._horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self._imageViewAndTagsHorizontalLayout.setObjectName("horizontalLayout_10")
        self._imageViewAndTagsSplitter.setObjectName("splitter")
        self._graphicsBox.setObjectName("graphicsBox")
        self._gridLayoutGraphicsBox.setObjectName("gridLayoutGraphicsBox")
        self.graphicsView.setObjectName("_graphicsView")


    def __removeUnsupportedExportFormats(self):

        toRemove = [MatplotlibExporter]

        for exporterToRemove in toRemove:
            try:
                Exporter.Exporters.remove(exporterToRemove)
            except ValueError:
                pass  # do nothing! Thread safe, better than an if check