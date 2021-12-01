import numpy as np
import pydicom
from pydicom import dicomio

from DICOM import DicomAbstractContainer
from DICOM.DicomAbstractContainer import ViewMode
from DICOM.DicomFile import DicomFile


class DicomSeries(DicomAbstractContainer.DicomAbstractContainerClass):
    """
    This type represents a Dicom series as a list of Dicom files sharing a series UID. The assumption is that the images
    of a series were captured together and so will always have a number of fields in common, such as patient name, so
    Dicoms should be organized by series. This type will also cache loaded Dicom tags and images
    """

    def __init__(self, seriesID, rootDir):

        super().__init__()
        self.seriesID = seriesID  # ID of the series or ???
        self.rootDir = rootDir  # directory Dicoms were loaded from, files for this series may be in subdirectories
        self.filenames = []  # list of filenames for the Dicom associated with this series
        self.dicomFilesList = []
        self.sortedFileNamesList = []  # list of filenames but sorted according to SliceLocation field
        self.dicomFilesIndexesDict = {}
        self.dicomFilesPathsDicts = {}
        self.loadTags = []  # loaded abbreviated tag->(name,value) maps, 1 for each of self.filenames
        self.imgCache = {}  # image data cache, mapping index in self.filenames to arrays or None for non-images files
        self.tagCache = {}  # tag values cache, mapping index in self.filenames to OrderedDict of tag->(name,value) maps
        self._size = 0

    @property
    def size(self):
        return self._size

    def addFile(self, filename, loadTag):
        """Add a filename and abbreviated tag map to the series."""
        self.filenames.append(filename)
        self.loadTags.append(loadTag)

    def getTagObject(self, index):
        """Get the object storing tag information from Dicom file at the given index."""
        if index not in self.tagCache:
            dcm = dicomio.read_file(self.filenames[index], stop_before_pixels = True)
            self.tagCache[index] = dcm

        return self.tagCache[index]

    def getExtraTagValues(self):
        """Return the extra tag values calculated from the series tag info stored in self.filenames."""
        start, interval, numTimes = self.getTimestepSpec()
        extraVals = {
            "NumImages":    len(self.filenames),
            "TimestepSpec": "start: %i, interval: %i, # Steps: %i"
                            % (start, interval, numTimes),
            "StartTime":    start,
            "NumTimesteps": numTimes,
            "TimeInterval": interval,
        }

        return extraVals

    def getTagValues(self, names, index = 0):
        """Get the tag values for tag names listed in `names' for image at the given index."""
        if not self.filenames:
            return ()

        dcm = self.getTagObject(index)
        extraVals = self.getExtraTagValues()

        # TODO: kludge? More general solution of telling series apart
        # dcm.SeriesDescription=dcm.get('SeriesDescription',dcm.get('SeriesInstanceUID','???'))

        return tuple(str(dcm.get(n, extraVals.get(n, ""))) for n in names)

    def getPixelData(self, index, mode: ViewMode = ViewMode.ORIGINAL):
        """Get the pixel data array for file at position `index` in self.filenames, or None if no pixel data."""
        return self.getDicomFileAt(index).getPixelData(mode)

    def getPixelDataList(self, mode: ViewMode = ViewMode.ORIGINAL):

        pixelData = []

        for index in range(0, self._size):
            data = self.getPixelData(index, mode)[0, :, :]
            pixelData.append(np.uint8(data))

        return pixelData

    def getDicomFileAt(self, index):
        return self.dicomFilesList[index]

    def getPixelDataFromPath(self, path, mode: ViewMode = ViewMode.ORIGINAL):
        try:
            index = self.getIndexFromPath(path)
            return self.getPixelData(index, mode)
        except:
            return None

    def getIndexFromPath(self, path):
        try:
            return self.dicomFilesPathsDicts.get(path)
        except:
            return None

    def addSeries(self, series):
        """Add every loaded dcm file from DicomSeries object `series` into this series."""
        for f, loadTag in zip(series.filenames, series.loadTags):  # TODO FIX THIS
            self.addFile(f, loadTag)

    def getTimestepSpec(self, tag = "TriggerTime"):
        """Returns (start time, interval, num timesteps) triple."""
        times = sorted(set(int(loadTag.get(tag, 0)) for loadTag in self.loadTags))

        if not times or times == [0]:
            return 0.0, 0.0, 0.0
        else:
            if len(times) == 1:
                times = times * 2

            avgSpan = np.average([b - a for a, b in zip(times, times[1:])])
            return times[0], avgSpan, len(times)

    def sortSeries(self):

        support = []
        # skip files with no SliceLocation (eg scout views)

        for i in range(len(self.filenames)):
            dcm = pydicom.dcmread(self.filenames[i])
            if "SliceLocation" in dcm:
                filename = self.filenames[i]
                support.append((dcm, filename))

        # ensure they are in the correct order
        support = sorted(support, key = lambda s: s[0].SliceLocation, reverse = True)

        cleanSupport = []

        for i in range(len(support)):
            self.sortedFileNamesList.append(support[i][1])
            cleanSupport.append(support[i][0])

        support = cleanSupport

        try:
            slice_thickness = np.abs(support[0].ImagePositionPatient[2] - support[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(support[0].SliceLocation - support[1].SliceLocation)

        for i in range(0, len(support)):
            support[i].SliceThickness = slice_thickness

        pixelsData = self.get_pixels_hu(support)

        for i in range(0, len(support)):
            currentSlice = support[i]
            originalImg = pixelsData[i]

            dcmFile = DicomFile(fileName = self.sortedFileNamesList[i], dicomData = currentSlice,
                                originalImg = originalImg)
            self.dicomFilesList.append(dcmFile)
            self.dicomFilesPathsDicts[self.sortedFileNamesList[i]] = i
            self.dicomFilesIndexesDict[i] = dcmFile

        self._size = len(self.dicomFilesList)
