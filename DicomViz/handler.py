import os
import threading
import zipfile
from collections import OrderedDict
from itertools import chain
from typing import Optional, List

from PyQt6.QtCore import QObject, pyqtSignal
from numpy import ndarray
from pyqtgraph.exporters import Exporter

from .DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
from .DICOM.DicomFileWrapper import DicomFileWrapper
from .DICOM.DicomSeries import DicomSeries
from .DICOM.dicom import loadDicomDir, loadDicomZip, loadDicomFile, seriesListColumns
from queue import Queue, Empty

from .DICOM.dicom import loadFilesInDirNotSeries
from .GUI import windowSingleton
from .GUI.docks.Dock import Dock
from .GUI.docks.DockFiles import DockFiles
from .GUI.docks.DockSeries import DockSeries
from .GUI.graphics.imageUtils import ROTATION_TRANSFORMATION
from .GUI.graphics.GIFExporter import GIFExporter
from .GUI.graphics.AnimationHandler import AnimationHandler
from .GUI.graphics.imageUtils import FLIP_TRANSFORMATION


class Handler(QObject):
    loadFilesIsComplete = pyqtSignal()
    loadSeriesIsComplete = pyqtSignal()

    def __init__(self):
        # create the directory queue and loading thread objects
        super().__init__()
        self._currentSelectedSeriesIndex = -1
        self._currentViewMode = ViewMode.ORIGINAL
        self._srcList = []  # list of tuples -> (src directory, DicomSeries object)
        self._seriesMap = OrderedDict()  # key -> series tags, value -> DicomSeries object
        self._currentSeriesFileNames = []  # list of current shown series files names
        self._srcDicomFileObjectsDict = {}  # dict of DicomFile objects -> filePath : DicomFile object
        self._srcQueue = Queue()  # queue of directories to load
        self._loadDirThread = threading.Thread(target = self._loadSourceThread)
        self._loadDirThread.daemon = True  # clean shutdown possible with daemon threads
        self._loadDirThread.start()  # start the thread now, it will wait until something is put on self.srcQueue
        self._lastLoadFolderDir = None
        self._lastLoadFileDir = None
        self._loadedSingleFile = []
        self._connectSignals()
        self._currentShownDicomFileObject = None
        self._isFirstLoad = True
        self._menus = None
        self._newSeriesAddedAmount = 0
        self._currentSeriesObject = None
        self._currentDicomFileObject = None

    @property
    def currSelectedSeriesIndex(self):
        return self._currentSelectedSeriesIndex

    @currSelectedSeriesIndex.setter
    def currSelectedSeriesIndex(self, value):
        if value >= 0 or value is None:
            self._currentSelectedSeriesIndex = value

    @property
    def menus(self) -> list:
        return self._menus

    @menus.setter
    def menus(self, value):
        self._menus = value

    @property
    def currentViewMode(self) -> ViewMode:
        return self._currentViewMode

    @currentViewMode.setter
    def currentViewMode(self, mode: ViewMode) -> None:
        self._currentViewMode = mode

    @property
    def srcTuplesList(self) -> Optional[List[tuple]]:
        return self._srcList

    @property
    def currentSeriesFileNames(self) -> Optional[List]:
        return self._currentSeriesFileNames

    @property
    def srcDicomFileObjectsDict(self) -> Optional[dict]:
        return self._srcDicomFileObjectsDict

    @property
    def lastLoadFolderDirectory(self) -> Optional[str]:
        return self._lastLoadFolderDir

    @property
    def lastLoadFileDirectory(self) -> Optional[str]:
        return self._lastLoadFileDir

    @property
    def loadedSingleFile(self) -> List:
        return self._loadedSingleFile

    @property
    def currentShownDicomFileObject(self) -> Optional[DicomAbstractContainerClass]:
        return self._currentShownDicomFileObject

    @currentShownDicomFileObject.setter
    def currentShownDicomFileObject(self, value) -> None:
        if isinstance(value, DicomAbstractContainerClass):
            self._currentShownDicomFileObject = value

    @property
    def currentSeriesObject(self) -> Optional[DicomSeries]:
        return self._currentSeriesObject

    @property
    def currentDicomFileObject(self) -> Optional[DicomFileWrapper]:
        return self._currentDicomFileObject

    @currentDicomFileObject.setter
    def currentDicomFileObject(self, dicomFileObject) -> None:
        if isinstance(dicomFileObject, DicomFileWrapper):
            self._currentDicomFileObject = dicomFileObject

    @classmethod
    def getCurrentShownImage(cls) -> ndarray:
        return windowSingleton.mainWindow.graphicsView.image

    @classmethod
    def applyTransformationToShownImage(cls, transformation) -> None:

        if isinstance(transformation, ROTATION_TRANSFORMATION):
            windowSingleton.mainWindow.graphicsView.applyTransformations(rotationTransformation = transformation,
                                                                         fromAction = True)
        elif isinstance(transformation, FLIP_TRANSFORMATION):
            windowSingleton.mainWindow.graphicsView.applyTransformations(flipTransformation = transformation,
                                                                         fromAction = True)

    @classmethod
    def clearTransformationsToShownImage(cls) -> None:
        windowSingleton.mainWindow.graphicsView.clearTransformations()

    @classmethod
    def toggleFilesMenuOptions(cls, value: bool) -> None:
        windowSingleton.mainWindow.menuBar.menuFiles.toggleFilesActions(value)

    @classmethod
    def isSeriesImageSelected(cls) -> bool:
        return windowSingleton.mainWindow.seriesFilesDock.isSomethingSelected()

    @classmethod
    def isSingleFileSelected(cls) -> bool:
        return windowSingleton.mainWindow.singleFilesDock.isSomethingSelected()

    @classmethod
    def toggleGifSlider(cls, value: bool) -> None:
        windowSingleton.mainWindow.graphicsView.toggleGifSlider(value)

    @classmethod
    def updateGifSpeedOnDialog(cls, value) -> None:
        GIFExporter.speed = value
        windowSingleton.mainWindow.graphicsView.updateExportDialog()
        exportersLen = windowSingleton.mainWindow.graphicsView.scene.exportDialog.ui.formatList.count() - 1
        windowSingleton.mainWindow.graphicsView.scene.exportDialog.ui.formatList.setCurrentRow(exportersLen)

    @classmethod
    def copyImageToClipboard(cls) -> None:
        windowSingleton.mainWindow.graphicsView.copyImageToClipboard()

    @classmethod
    def enableNegativeImageAction(cls) -> None:
        windowSingleton.mainWindow.menuBar.menuAlterations.enableNegativeImageAction()

    @classmethod
    def _removeSeriesFilesFromDock(cls) -> None:
        windowSingleton.mainWindow.seriesFilesDock.removeSeriesFiles()

    @classmethod
    def changeAnimateActionText(cls) -> None:
        windowSingleton.mainWindow.menuBar.menuCine.changeAnimateActionText(
            isAnimationOn = windowSingleton.mainWindow.graphicsView.isAnimationOn())

    def setImageToView(self, DicomContainer: 'DicomAbstractContainerClass',
                       viewMode: ViewMode,
                       isFirstImage: bool) -> None:

        # windowSingleton.mainWindow.graphicsView.isSomeTransformationAlreadyAppliedToCurrentImg = False
        if self._isFirstLoad:
            self._isFirstLoad = False
            self.toggleMenuOptions(True)

        self.currentViewMode = viewMode
        windowSingleton.mainWindow.tagsGroupBox.fillTagsTree(dicomFile = DicomContainer)
        windowSingleton.mainWindow.graphicsView.setImageToView(DicomContainer, viewMode, isFirstImage)

    def prepareGifExporter(self) -> None:
        print(self.currentViewMode)
        data = (self._srcList[self._currentSelectedSeriesIndex][1]).getPixelDataList(mode = self.currentViewMode)
        AnimationHandler.prepareGIFExport(data)

    def removeSeries(self) -> None:
        removedRowTuple = windowSingleton.mainWindow.seriesSelectionModel.removeRow(self.currSelectedSeriesIndex)
        removedDicomSeriesObject = self._seriesMap.pop(removedRowTuple)
        self._removeDicomSeriesObjectFromSrcList(dicomSeriesObject = removedDicomSeriesObject)
        self.removeImageFromView()
        self._removeSeriesFilesFromDock()

    def removeImageFromView(self) -> None:
        windowSingleton.mainWindow.graphicsView.removeImageFromView()
        windowSingleton.mainWindow.seriesFilesDock.deselectItem()
        windowSingleton.mainWindow.singleFilesDock.deselectItem()
        self.toggleMenuOptions(False)

    def addSource(self, rootDir) -> None:
        """Add the given directory to the queue of directories to load and set the self.lastDir value to its parent."""
        self._srcQueue.put(rootDir)
        self._lastLoadFolderDir = os.path.dirname(rootDir)

    def isSomeImageShown(self) -> bool:
        return self.getCurrentShownImage() is not None

    def toggleMenuOptions(self, value: bool) -> None:
        for menu in self.menus:
            menu.toggleActions(value = value, dicomContainer = self._currentDicomFileObject)

    def handleFilesFromFolder(self, folderPath) -> None:
        self.addSource(folderPath)

    def handleSingleFiles(self, filePath) -> None:
        self.addSource(filePath)

    def handleGIFExporter(self) -> None:

        if self.isSeriesImageSelected() and GIFExporter not in Exporter.Exporters:
            GIFExporter.register()

        elif self.isSingleFileSelected():
            GIFExporter.unregister()

    def handleDocksClicks(self, dock: Dock) -> None:

        try:
            if isinstance(dock, DockSeries):

                if windowSingleton.mainWindow.graphicsView.isAnimationOn():
                    self.toggleGifSlider(True)
                else:
                    self.toggleGifSlider(False)
                windowSingleton.mainWindow.singleFilesDock.deselectItem()
                windowSingleton.mainWindow.graphicsView.updateExportDialog()
                windowSingleton.mainWindow.menuBar.menuFiles.toggleActionRemoveSeries(True)

            elif isinstance(dock, DockFiles):
                windowSingleton.mainWindow.graphicsView.updateExportDialog()
                self.toggleGifSlider(False)
                windowSingleton.mainWindow.seriesFilesDock.deselectItem()
                windowSingleton.mainWindow.menuBar.menuCine.toggleActions(False)
                windowSingleton.mainWindow.menuBar.menuFiles.toggleActionRemoveSeries(False)

        except Exception as e:
            print(str(e))
            pass

    def seriesClicked(self, item) -> None:
        """Called when a series is clicked on, set the viewed image to be from the clicked series."""

        if item.row() == self._currentSelectedSeriesIndex:
            return

        self._currentSelectedSeriesIndex = item.row()
        selectionModel = windowSingleton.mainWindow.seriesSelectionModel
        selectionModel.currentSelectedRowIndex = self._currentSelectedSeriesIndex
        self._currentSeriesObject = self._seriesMap[
            selectionModel.getRowContent(index = self._currentSelectedSeriesIndex)]
        self._currentDicomFileObject = self._currentSeriesObject

        self._currentSeriesFileNames = self._currentSeriesObject.sortedFileNamesList
        self._handleDockSeriesLoad()

        if windowSingleton.mainWindow.graphicsView.animationHandler:
            windowSingleton.mainWindow.graphicsView.addAnimationHandler()

    def _addToSeriesTable(self) -> None:

        lenght = len(self._srcList)

        newDictPart = OrderedDict()

        if lenght > 0:
            for entry in self._srcList[lenght - self._newSeriesAddedAmount: lenght]:
                tags = entry[1].getTagValues(seriesListColumns)
                newDictPart[tags] = entry[1]

            windowSingleton.mainWindow.seriesSelectionModel.updateTable(seriesEntries = newDictPart.keys())
            windowSingleton.mainWindow.seriesSelectionModel.layoutChanged.emit()
            self._seriesMap = OrderedDict(chain(self._seriesMap.items(), newDictPart.items()))

        windowSingleton.mainWindow.seriesSelectionWidget.clickRow(index = 0)

    def _loadFilesThreadJob(self, src) -> None:
        dicomFile = loadDicomFile(src)
        self._srcDicomFileObjectsDict[src] = dicomFile
        self._lastLoadFileDir = src
        self._loadedSingleFile = [self._srcDicomFileObjectsDict[self._lastLoadFileDir]]
        self.loadFilesIsComplete.emit()

    def _loadSourceThread(self) -> None:
        """
        This is run in a daemon thread and continually checks self.srcQueue for a queued directory or zip file to scan
        for Dicom files. It calls loadDicomDir() for a given directory or loadDicomZip() for a zip file and adds the
        results the self.srclist member.
        """
        while True:
            try:
                src = self._srcQueue.get(True, 0.5)
                # self.toggleFilesMenuOptions(False)
                if os.path.isdir(src):
                    loader = loadDicomDir

                elif zipfile.is_zipfile(src):
                    loader = loadDicomZip
                else:
                    self._loadFilesThreadJob(src)
                    continue

                seriesInDir = loader(src)

                prevLen = len(self._srcList)

                if len(seriesInDir) == 0:
                    filesNotSeriesInDir = loadFilesInDirNotSeries(src)

                    self._loadedSingleFile.clear()

                    for file in filesNotSeriesInDir:
                        self._srcDicomFileObjectsDict[file[0]] = file[1]
                        self._lastLoadFileDir = file[0]
                        self._loadedSingleFile.append(self._srcDicomFileObjectsDict[self._lastLoadFileDir])

                    self.loadFilesIsComplete.emit()
                        #time.sleep(1)

                    continue

                for series in seriesInDir:
                    self._srcList.append((src, series))

                self._newSeriesAddedAmount = len(self._srcList) - prevLen

                self._currentSeriesFileNames = seriesInDir[0].sortedFileNamesList
                self.currentSelectedSeriesIndex = prevLen
                self.loadSeriesIsComplete.emit()

            except Empty:
                pass

    def _handleDockFilesLoad(self) -> None:
        windowSingleton.mainWindow.seriesFilesDock.unselectCurrentSelected()
        windowSingleton.mainWindow.singleFilesDock.loadFiles(self._loadedSingleFile)
        self.toggleFilesMenuOptions(True)

    def _handleDockSeriesLoad(self) -> None:
        windowSingleton.mainWindow.seriesFilesDock.loadFiles(self._currentSeriesFileNames)
        windowSingleton.mainWindow.singleFilesDock.unselectCurrentSelected()
        self.toggleFilesMenuOptions(True)

    def _removeDicomSeriesObjectFromSrcList(self, dicomSeriesObject: DicomSeries) -> None:

        for entry in self._srcList:
            if entry[1] == dicomSeriesObject:
                del entry

    def _connectSignals(self) -> None:
        self.loadSeriesIsComplete.connect(self._addToSeriesTable)
        self.loadFilesIsComplete.connect(self._handleDockFilesLoad)
