from typing import Optional

import numpy as np
from numpy import ndarray
import pydicom

from DICOM import DicomAbstractContainer
from DICOM.DicomAbstractContainer import ViewMode
from DICOM.DicomFileWrapper import DicomFileWrapper


class DicomSeries(DicomAbstractContainer.DicomAbstractContainerClass):
    """
    This type represents a Dicom series as a list of Dicom files sharing a series UID. The assumption is that the images
    of a series were captured together and so will always have a number of fields in common, such as patient name, so
    Dicoms should be organized by series.
    """

    def __init__(self, seriesID, rootDir):

        super().__init__()
        self._seriesID = seriesID  # ID of the series or ???
        self._rootDirectory = rootDir  # directory Dicoms were loaded from, files for this series may be in subdirectories
        self._filenames = []  # list of filenames for the Dicom associated with this series
        self._sortedFileNamesList = []  # list of filenames but sorted according to SliceLocation field
        self._dicomFilesIndexesDict = {}
        self._dicomFilesPathsDicts = {}
        self._loadedTagsTuplesList = []  # loaded abbreviated tag->(name,value) maps, 1 for each of self.filenames
        self._imgCache = {}  # image data cache, mapping index in self.filenames to arrays or None for non-images files
        self._tagCache = {}  # tag values cache, mapping index in self.filenames to OrderedDict of tag->(name,value) maps
        self._seriesSize = 0
        self._seriesPixelsDataTuple = None
        self._dicomFileIndexesCache = []
        self._supportDcmFiles = None
        self._sliceThickness = None

    @property
    def seriesSize(self) -> int:
        return self._seriesSize

    @property
    def seriesID(self) -> int:
        return self._seriesID

    @property
    def rootDirectory(self) -> str:
        return self._rootDirectory

    @property
    def loadedTagsTuplesList(self) -> list[tuple]:
        return self._loadedTagsTuplesList

    @property
    def sortedFileNamesList(self) -> list[str]:
        return self._sortedFileNamesList

    @property
    def dicomFilesIndexesDict(self) -> dict:
        return self._dicomFilesIndexesDict

    @property
    def dicomFilesPathsDict(self) -> dict:
        return self._dicomFilesPathsDicts

    @property
    def seriesSlicesThickness(self):
        return self._sliceThickness

    def addFile(self, filename, loadTag) -> None:
        """Add a filename and abbreviated tag map to the series."""
        self._filenames.append(filename)
        self._loadedTagsTuplesList.append(loadTag)
        self._seriesSize = self._seriesSize + 1

    def getExtraTagValues(self) -> dict:
        """Return the extra tag values calculated from the series tag info stored in self.filenames."""
        start, interval, numTimes = self.getTimestepSpec()
        extraVals = {
            "NumImages":    len(self._filenames),
            "TimestepSpec": "start: %i, interval: %i, # Steps: %i"
                            % (start, interval, numTimes),
            "StartTime":    start,
            "NumTimesteps": numTimes,
            "TimeInterval": interval,
        }

        return extraVals

    def getTagValues(self, names, index = 0) -> tuple:
        """Get the tag values for tag names listed in `names' for image at the given index."""
        if not self._filenames:
            return ()

        if self._seriesPixelsDataTuple is None:
            dcm = self.getDicomRawImage(index = index).getDicomFile()

        else:
            dcm = self.getDicomFile(index)

        extraVals = self.getExtraTagValues()

        return tuple(str(dcm.get(n, extraVals.get(n, ""))) for n in names)

    def getPixelData(self, index, mode: ViewMode = ViewMode.ORIGINAL) -> ndarray:
        """Get the pixel data array for file at position `index` in self.filenames, or None if no pixel data."""

        return self.getDicomFile(index).getPixelData(mode)

    def computeDicomFile(self, index) -> None:

        currentSlice = self._supportDcmFiles[index]
        currentSlice.SliceThickness = self._sliceThickness
        originalImg = self._seriesPixelsDataTuple[index]

        dcmFile = DicomFileWrapper(fileName = self._sortedFileNamesList[index], dicomData = currentSlice,
                                   originalImg = originalImg)

        self._dicomFilesIndexesDict[index] = dcmFile

    def loadPixelDataTuple(self) -> None:
        if self._seriesPixelsDataTuple is None:
            self._seriesPixelsDataTuple = self.getPixelsArray(self._supportDcmFiles)

    def getPixelDataList(self, mode: ViewMode = ViewMode.ORIGINAL) -> list:

        pixelData = []

        for index in range(0, self._seriesSize):
            data = self.getPixelData(index, mode)[0, :, :]
            pixelData.append(np.uint8(data))

        return pixelData

    def getDicomFile(self, index):

        if index not in self._dicomFileIndexesCache:
            self.computeDicomFile(index = index)
            self._dicomFileIndexesCache.append(index)

        return self._dicomFilesIndexesDict[index]

    def getDicomRawImage(self, index: int) -> DicomFileWrapper:
        if self._seriesPixelsDataTuple is None:
            return DicomFileWrapper(fileName = self._sortedFileNamesList[index])
        else:
            return self.getDicomFile(index = 0)

    def getPixelDataFromPath(self, path, mode: ViewMode = ViewMode.ORIGINAL) -> Optional[ndarray]:
        try:
            index = self.getIndexFromPath(path)
            return self.getPixelData(index, mode)
        except:
            return None

    def getIndexFromPath(self, path) -> Optional[int]:
        try:
            return self._dicomFilesPathsDicts.get(path)
        except:
            return None

    def addSeries(self, series) -> None:
        """Add every loaded dcm file from DicomSeries object `series` into this series."""
        for f, loadTag in zip(series.sortedFileNames, series.loadedTagsTuplesList):  # TODO FIX THIS
            self.addFile(f, loadTag)

    def getTimestepSpec(self, tag = "TriggerTime") -> tuple:
        """Returns (start time, interval, num timesteps) triple."""
        times = sorted(set(int(loadTag.get(tag, 0)) for loadTag in self.loadedTagsTuplesList))

        if not times or times == [0]:
            return 0.0, 0.0, 0.0
        else:
            if len(times) == 1:
                times = times * 2

            avgSpan = np.average([b - a for a, b in zip(times, times[1:])])
            return times[0], avgSpan, len(times)

    def computeSliceThickness(self) -> None:
        if self._sliceThickness is None:
            try:
                self._sliceThickness = np.abs(
                        self._supportDcmFiles[0].ImagePositionPatient[2] - self._supportDcmFiles[1].ImagePositionPatient[2])
            except:
                self._sliceThickness = np.abs(self._supportDcmFiles[0].SliceLocation - self._supportDcmFiles[1].SliceLocation)

    def sortSeries(self) -> None:

        self._supportDcmFiles = []
        # skip files with no SliceLocation

        for i in range(len(self._filenames)):
            dcm = pydicom.dcmread(self._filenames[i])
            if "SliceLocation" in dcm:
                filename = self._filenames[i]
                self._supportDcmFiles.append((dcm, filename))

        # sort files according to SliceLocation field
        self._supportDcmFiles = sorted(self._supportDcmFiles, key = lambda s: s[0].SliceLocation, reverse = True)

        cleanSupport = []

        for i in range(len(self._supportDcmFiles)):
            self._sortedFileNamesList.append(self._supportDcmFiles[i][1])
            cleanSupport.append(self._supportDcmFiles[i][0])
            self._dicomFilesPathsDicts[self._sortedFileNamesList[i]] = i

        self._supportDcmFiles = cleanSupport

        self._seriesSize = len(self._supportDcmFiles)
