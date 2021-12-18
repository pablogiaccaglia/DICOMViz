import os
import threading
import zipfile
from collections import OrderedDict
from itertools import chain
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal
from pyqtgraph.exporters import Exporter

from DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
from DICOM.DicomSeries import DicomSeries
from DICOM.dicom import loadDicomDir, loadDicomZip, loadDicomFile, seriesListColumns
from queue import Queue, Empty

from GUI.docks.Dock import Dock
from GUI.docks.DockFiles import DockFiles
from GUI.docks.DockSeries import DockSeries
from GUI.graphics.CustomImageView import TRANSFORMATION
from GUI.graphics.GIFExporter import GIFExporter
from GUI.graphics.GIFHandler import GIFHandler


class Handler(QObject):
    # statusSignal = QtCore.pyqtSignal(str, int, int)  # signal for updating the status bar asynchronously

    loadFilesIsComplete = pyqtSignal()
    loadSeriesIsComplete = pyqtSignal()

    def __init__(self, window):
        # create the directory queue and loading thread objects
        super().__init__()
        self._currentSelectedSeriesIndex = -1
        self.currentViewMode = ViewMode.ORIGINAL
        self.window = window
        self.srcList = []  # list of tuples -> (src directory, DicomSeries object)
        self.seriesMap = OrderedDict()  # key -> series tags, value -> DicomSeries object
        self.currentSeries = []  # list of series of the currently selected
        self.srcDicomFileObjectsDict = {}  # dict of DicomFile objects -> filePath : DicomFile object
        self.srcQueue = Queue()  # queue of directories to load
        self.loadDirThread = threading.Thread(target = self._loadSourceThread)
        self.loadDirThread.daemon = True  # clean shutdown possible with daemon threads
        self.loadDirThread.start()  # start the thread now, it will wait until something is put on self.srcQueue
        self.setStatus("")
        self.lastLoadFolderDir = None
        self.lastLoadFileDir = None
        self.fileIsLoadedFunction = None
        self.connectSignals()
        self.currentShownDicomFileObject = None
        self.isFirstLoad = True
        self.menus = None
        self.newSeriesAddedAmount = 0
        self.currentSeriesObject = None
        self.currentDicomObject = None

    def connectSignals(self):
        self.loadSeriesIsComplete.connect(self.__addToSeriesTable)
        self.loadFilesIsComplete.connect(self.__handleDockFilesLoad)
        self.window.seriesSelectionWidget.clicked.connect(self.seriesClicked)

    # self.statusSignal.connect(self.setStatus)

    def __handleDockFilesLoad(self):
        self.window.seriesFilesDock.unselectCurrentSelected()
        self.window.singleFilesDock.loadFiles(self.fileIsLoadedFunction)
        self.toggleFilesMenuOptions(True)

    def __handleDockSeriesLoad(self):
        self.window.seriesFilesDock.loadFiles(self.currentSeries)
        self.window.singleFilesDock.unselectCurrentSelected()
        self.toggleFilesMenuOptions(True)

    def setImageToView(self, DicomContainer: 'DicomAbstractContainerClass', viewMode: ViewMode, isFirstImage: bool):

        if self.isFirstLoad:
            self.isFirstLoad = False
            self.toggleMenuOptions(True)

        self.window.tagsGroupBox.fillTagsTree(dicomFile = DicomContainer)
        self.window.graphicsView.setImageToView(DicomContainer, viewMode, isFirstImage)

    def prepareGifExporter(self):
        data = (self.srcList[self._currentSelectedSeriesIndex][1]).getPixelDataList(mode = self.currentViewMode)
        GIFHandler.prepareGIFExport(data)

    def removeSeries(self):
        removedRowTuple = self.window.seriesSelectionModel.removeRow(self.currSelectedSeriesIndex)
        removedDicomSeriesObject = self.seriesMap.pop(removedRowTuple)
        self.__removeDicomSeriesObjectFromSrcList(dicomSeriesObject = removedDicomSeriesObject)
        self.removeImageFromView()
        self.__removeSeriesFilesFromDock()

    def __removeDicomSeriesObjectFromSrcList(self, dicomSeriesObject: DicomSeries):

        for entry in self.srcList:
            if entry[1] == dicomSeriesObject:
                del entry

    def __removeSeriesFilesFromDock(self):
        self.window.seriesFilesDock.removeSeriesFiles()

    def removeImageFromView(self):
        self.window.graphicsView.removeImageFromView()
        self.window.seriesFilesDock.deselectItem()
        self.window.singleFilesDock.deselectItem()
        self.toggleMenuOptions(False)

    def setStatus(self, msg, progress = 0, progressmax = 0):
        return
        """
        Set the status bar with message `msg' with progress set to `progress' out of `progressmax', or hide the status
        elements if `msg' is empty or None.
        """
        if not msg:
            progress = 0
            progressmax = 0

        self.statusText.setText(msg)
        self.statusText.setVisible(bool(msg))
        self.importDirButton.setVisible(not bool(msg))
        self.importZipButton.setVisible(not bool(msg))
        self.statusProgressBar.setVisible(progressmax > 0)
        self.statusProgressBar.setRange(0, progressmax)
        self.statusProgressBar.setValue(progress)

    def addSource(self, rootDir):
        """Add the given directory to the queue of directories to load and set the self.lastDir value to its parent."""
        self.srcQueue.put(rootDir)
        self.lastLoadFolderDir = os.path.dirname(rootDir)

    def _loadSourceThread(self):
        """
        This is run in a daemon thread and continually checks self.srcQueue for a queued directory or zip file to scan
        for Dicom files. It calls loadDicomDir() for a given directory or loadDicomZip() for a zip file and adds the
        results the self.srclist member.
        """
        while True:
            try:
                src = self.srcQueue.get(True, 0.5)
                # self.toggleFilesMenuOptions(False)
                if os.path.isdir(src):
                    loader = loadDicomDir

                elif zipfile.is_zipfile(src):
                    loader = loadDicomZip
                else:
                    dicomFile = loadDicomFile(src)
                    self.srcDicomFileObjectsDict[src] = dicomFile
                    self.lastLoadFileDir = src
                    self.fileIsLoadedFunction = [self.srcDicomFileObjectsDict[self.lastLoadFileDir]]
                    self.loadFilesIsComplete.emit()
                    continue

                seriesInDir = loader(src)

                prevLen = len(self.srcList)

                for series in seriesInDir:
                    self.srcList.append((src, series))

                self.newSeriesAddedAmount = len(self.srcList) - prevLen

                self.currentSeries = seriesInDir[0].sortedFileNamesList
                self.currentSelectedSeriesIndex = prevLen
                self.loadSeriesIsComplete.emit()

            except Empty:
                pass

    @property
    def currSelectedSeriesIndex(self):
        return self._currentSelectedSeriesIndex

    @classmethod
    def is_dicom_file(self, path: str) -> bool:
        """Fast way to check whether file is DICOM."""
        if not os.path.isfile(path):
            return False
        try:
            with open(path, "rb") as f:
                return f.read(132).decode("ASCII")[-4:] == "DICM"
        except:
            return False

    def dicom_files_in_dir(self, directory: str = ".") -> List[str]:
        """Full paths of all DICOM files in the directory."""
        directory = os.path.expanduser(directory)
        files = [os.path.join(directory, f) for f in sorted(os.listdir(directory))]
        return [f for f in files if self.is_dicom_file(f)]

    @currSelectedSeriesIndex.setter
    def currSelectedSeriesIndex(self, value):
        if value >= 0 or value is None:
            self._currentSelectedSeriesIndex = value

    def isSomeImageShown(self) -> bool:
        return self.getCurrentShownImage() is not None

    def getCurrentShownImage(self):
        return self.window.graphicsView.img

    def applyTransformationToShownImage(self, transformation: TRANSFORMATION):
        self.window.graphicsView.applyTransformation(transformation)

    def clearTransformationsToShownImage(self):
        self.window.graphicsView.clearTransformations()

    def toggleMenuOptions(self, value: bool):
        for menu in self.menus:
            menu.toggleActions(value = value, dicomContainer = self.currentDicomObject)

    def toggleFilesMenuOptions(self, value: bool):
        self.window.menuBar.menuFiles.toggleFilesActions(value)

    @property
    def menus(self) -> List:
        return self._menus

    @menus.setter
    def menus(self, value):
        self._menus = value

    def handleFilesFromFolder(self, folderPath):
        self.addSource(folderPath)

    def handleSingleFiles(self, filePath):
        self.addSource(filePath)

    def handleGIFExporter(self) -> None:

        if self.isSeriesImageSelected() and GIFExporter not in Exporter.Exporters:
            GIFExporter.register()

        elif self.isSingleFileSelected():
            GIFExporter.unregister()

    def isSeriesImageSelected(self) -> bool:
        return self.window.seriesFilesDock.isSomethingSelected()

    def isSingleFileSelected(self) -> bool:
        return self.window.singleFilesDock.isSomethingSelected()

    def handleDocksClicks(self, dock: Dock) -> None:

        try:
            if isinstance(dock, DockSeries):

                if self.window.graphicsView.isAnimationOn():
                    self.toggleGifSlider(True)
                else:
                    self.toggleGifSlider(False)
                self.window.singleFilesDock.deselectItem()
                self.window.graphicsView.updateExportDialog()
                self.window.menuBar.menuFiles.toggleActionRemoveSeries(True)

            elif isinstance(dock, DockFiles):
                self.window.graphicsView.updateExportDialog()
                self.toggleGifSlider(False)
                self.window.seriesFilesDock.deselectItem()
                self.window.menuBar.menuCine.toggleActions(False)
                self.window.menuBar.menuFiles.toggleActionRemoveSeries(False)

        except Exception as e:
            print(str(e))
            pass

    def toggleGifSlider(self, value: bool):
        self.window.graphicsView.toggleGifSlider(value)

    def updateGifSpeedOnDialog(self, value):
        GIFExporter.speed = value
        self.window.graphicsView.updateExportDialog()
        exportersLen = self.window.graphicsView.scene.exportDialog.ui.formatList.count() - 1
        self.window.graphicsView.scene.exportDialog.ui.formatList.setCurrentRow(exportersLen)

    def copyImageToClipboard(self):
        return self.window.graphicsView.copyImageToClipboard()

    def enableNegativeImageAction(self):
        self.window.menuBar.menuAlterations.enableNegativeImageAction()

    def __addToSeriesTable(self):

        lenght = len(self.srcList)

        newDictPart = OrderedDict()

        if lenght > 0:
            for entry in self.srcList[lenght - self.newSeriesAddedAmount: lenght]:
                tags = entry[1].getTagValues(seriesListColumns)
                newDictPart[tags] = entry[1]

            self.window.seriesSelectionModel.updateTable(seriesEntries = newDictPart.keys())
            self.window.seriesSelectionModel.layoutChanged.emit()
            self.seriesMap = OrderedDict(chain(self.seriesMap.items(), newDictPart.items()))

        self.window.seriesSelectionWidget.clickRow(index = 0)

    def seriesClicked(self, item):
        """Called when a series is clicked on, set the viewed image to be from the clicked series."""

        if item.row() == self._currentSelectedSeriesIndex:
            return

        self._currentSelectedSeriesIndex = item.row()
        selectionModel = self.window.seriesSelectionModel
        selectionModel.currentSelectedRowIndex = self._currentSelectedSeriesIndex
        self.currentSeriesObject = self.seriesMap[
            selectionModel.getRowContent(index = self._currentSelectedSeriesIndex)]
        self.currentDicomObject = self.currentSeriesObject

        self.currentSeries = self.currentSeriesObject.sortedFileNamesList
        self.__handleDockSeriesLoad()

        if self.window.graphicsView.gifHandler:
            self.window.graphicsView.addGifHandler()

    def changeAnimateActionText(self):
        self.window.menuBar.menuCine.changeAnimateActionText(isAnimationOn = self.window.graphicsView.isAnimationOn())
