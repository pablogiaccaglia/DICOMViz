import os
import threading
import zipfile
from typing import List

from DICOM.DicomAbstractContainer import ViewMode
from DICOM.dicom import loadDicomDir, loadDicomZip, loadDicomFile
from multiprocessing import Queue
from queue import Empty


class Handler:
    # statusSignal = QtCore.pyqtSignal(str, int, int)  # signal for updating the status bar asynchronously

    def __init__(self, window):
        # create the directory queue and loading thread objects
        #   super().__init__()
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
        self.loadIsComplete = False
        self.currentShownDicomFileObject = None

    # self.statusSignal.connect(self.setStatus)

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
                if os.path.isdir(src):
                    loader = loadDicomDir
                elif zipfile.is_zipfile(src):
                    loader = loadDicomZip
                else:
                    dicomFile = loadDicomFile(src)
                    self.srcDicomFileObjectsDict[src] = dicomFile
                    self.loadIsComplete = True
                    continue

                #  series = loader(src, self.statusSignal.emit)
                series = loader(src)
                self.srcList.append((src, series))
                self.currentSeries = series[0].sortedFileNamesList
                self.loadIsComplete = True

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
        if value >= 0:
            self._currentSelectedSeriesIndex = value
