import os
import threading

from DICOM.dicom import loadDicomDir, loadDicomZip, loadDicomFile
from queue import Queue, Empty


class Handler:
   # statusSignal = QtCore.pyqtSignal(str, int, int)  # signal for updating the status bar asynchronously

    def __init__(self):
        # create the directory queue and loading thread objects
     #   super().__init__()
        self.srcList = []  # list of source directories
        self.srcFiles = []
        self.srcQueue = Queue()  # queue of directories to load
        self.loadDirThread = threading.Thread(target=self._loadSourceThread)
        self.loadDirThread.daemon = True  # clean shutdown possible with daemon threads
        self.loadDirThread.start()  # start the thread now, it will wait until something is put on self.srcQueue
        self.setStatus("")
        self.lastLoadFolderDir = None
        self.lastLoadFileDir = None
       # self.statusSignal.connect(self.setStatus)

    def setStatus(self, msg, progress=0, progressmax=0):
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

    def addFile(self, path):
        self.srcFiles.append(loadDicomFile(path))
        self.lastLoadFileDir = os.path.dirname(path)

    def _loadSourceThread(self):
        """
        This is run in a daemon thread and continually checks self.srcQueue for a queued directory or zip file to scan
        for Dicom files. It calls loadDicomDir() for a given directory or loadDicomZip() for a zip file and adds the
        results the self.srclist member.
        """
        while True:
            try:
                src = self.srcQueue.get(True, 0.5)
                loader = loadDicomDir if os.path.isdir(src) else loadDicomZip
              #  series = loader(src, self.statusSignal.emit)
                series = loader(src)

                if series and all(len(s.filenames) > 0 for s in series):
                    for s in series:
                        # sort series contents by filename
                        s.filenames, s.loadTags = zip(*sorted(zip(s.filenames, s.loadTags)))

                    self.srcList.append((src, series))

              #  self.updateSignal.emit()
            except Empty:
                pass
