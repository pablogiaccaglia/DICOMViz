import os
import threading
import zipfile
from typing import List

from PyQt6.QtCore import QObject, pyqtSignal
from pyqtgraph.exporters import Exporter

from DICOM.DicomAbstractContainer import ViewMode, DicomAbstractContainerClass
from DICOM.dicom import loadDicomDir, loadDicomZip, loadDicomFile
from multiprocessing import Queue
from queue import Empty

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
        self._currentSelectedSeriesIndex = 0
        self.currentViewMode = ViewMode.ORIGINAL
        self.window = window
        self.srcList = []  # list of tuples -> (src directory, DicomSeries object)
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

    def connectSignals(self):
        self.loadSeriesIsComplete.connect(self.__handleDockSeriesLoad)
        self.loadFilesIsComplete.connect(self.__handleDockFilesLoad)

    # self.statusSignal.connect(self.setStatus)

    def __handleDockFilesLoad(self):
        self.window.seriesFilesDock.unselectCurrentSelected()
        self.window.singleFilesDock.loadFiles(self.fileIsLoadedFunction)
        self.toggleFilesMenuOptions(True)

    def __handleDockSeriesLoad(self):
        self.window.singleFilesDock.unselectCurrentSelected()
        self.window.seriesFilesDock.loadFiles(self.currentSeries)
        self.toggleFilesMenuOptions(True)

    def setImageToView(self, DicomContainer: 'DicomAbstractContainerClass', viewMode: ViewMode, isFirstImage: bool):

        if self.isFirstLoad:
            self.isFirstLoad = False
            self.toggleMenuOptions(True)

        self.window.graphicsView.setImageToView(DicomContainer, viewMode, isFirstImage)

    def prepareGifExporter(self):
        data = (self.srcList[self._currentSelectedSeriesIndex][1][0]).getPixelDataList(mode = self.currentViewMode)
        GIFHandler.prepareGIFExport(data)

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
                self.toggleFilesMenuOptions(False)
                if os.path.isdir(src):
                    loader = loadDicomDir
                    self._currentSelectedSeriesIndex = 0

                elif zipfile.is_zipfile(src):
                    loader = loadDicomZip
                    self._currentSelectedSeriesIndex = 0
                else:
                    dicomFile = loadDicomFile(src)
                    self.srcDicomFileObjectsDict[src] = dicomFile
                    self._currentSelectedSeriesIndex = None
                    self.lastLoadFileDir = src
                    self.fileIsLoadedFunction = [self.srcDicomFileObjectsDict[self.lastLoadFileDir]]
                    self.loadFilesIsComplete.emit()
                    continue

                #  series = loader(src, self.statusSignal.emit)
                series = loader(src)
                self.srcList.append((src, series))
                self.currentSeries = series[0].sortedFileNamesList
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
            menu.toggleActions(value)

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
        else:
            GIFExporter.unregister()

    def isSeriesImageSelected(self) -> bool:
        return self.window.seriesFilesDock.isSomethingSelected()



