import numpy as np
import pydicom
from pydicom import dicomio
from DICOM import DicomAbstractContainer


class DicomSeries(DicomAbstractContainer.DicomAbstractContainerClass):

    """
    This type represents a Dicom series as a list of Dicom files sharing a series UID. The assumption is that the images
    of a series were captured together and so will always have a number of fields in common, such as patient name, so
    Dicoms should be organized by series. This type will also cache loaded Dicom tags and images
    """

    def __init__(self, seriesID, rootDir):

        self.seriesID = seriesID  # ID of the series or ???
        self.rootDir = rootDir  # directory Dicoms were loaded from, files for this series may be in subdirectories
        self.filenames = []  # list of filenames for the Dicom associated with this series
        self.sortedFileNames = []  # filenames but sorted
        self.loadTags = []  # loaded abbreviated tag->(name,value) maps, 1 for each of self.filenames
        self.imgCache = {}  # image data cache, mapping index in self.filenames to arrays or None for non-images files
        self.tagCache = {}  # tag values cache, mapping index in self.filenames to OrderedDict of tag->(name,value) maps

    def addFile(self, filename, loadTag):
        """Add a filename and abbreviated tag map to the series."""
        self.filenames.append(filename)
        self.loadTags.append(loadTag)

    def getTagObject(self, index):
        """Get the object storing tag information from Dicom file at the given index."""
        if index not in self.tagCache:
            dcm = dicomio.read_file(self.filenames[index], stop_before_pixels=True)
            self.tagCache[index] = dcm

        return self.tagCache[index]

    def getExtraTagValues(self):
        """Return the extra tag values calculated from the series tag info stored in self.filenames."""
        start, interval, numTimes = self.getTimestepSpec()
        extraVals = {
            "NumImages": len(self.filenames),
            "TimestepSpec": "start: %i, interval: %i, # Steps: %i"
                            % (start, interval, numTimes),
            "StartTime": start,
            "NumTimesteps": numTimes,
            "TimeInterval": interval,
        }

        return extraVals

    def getTagValues(self, names, index=0):
        """Get the tag values for tag names listed in `names' for image at the given index."""
        if not self.filenames:
            return ()

        dcm = self.getTagObject(index)
        extraVals = self.getExtraTagValues()

        # TODO: kludge? More general solution of telling series apart
        # dcm.SeriesDescription=dcm.get('SeriesDescription',dcm.get('SeriesInstanceUID','???'))

        return tuple(str(dcm.get(n, extraVals.get(n, ""))) for n in names)

    def getPixelData(self, index):
        """Get the pixel data array for file at position `index` in self.filenames, or None if no pixel data."""
        if index not in self.imgCache:
            try:
                dcm = dicomio.read_file(self.filenames[index])
                rslope = float(dcm.get("RescaleSlope", 1) or 1)
                rinter = float(dcm.get("RescaleIntercept", 0) or 0)
                img = dcm.pixel_array * rslope + rinter
            except:
                img = None  # exceptions indicate that the pixel data doesn't exist or isn't readable so ignore

            self.imgCache[index] = img

        return self.imgCache[index]

    def addSeries(self, series):
        """Add every loaded dcm file from DicomSeries object `series` into this series."""
        for f, loadTag in zip(series.filenames, series.loadTags):
            self.addFile(f, loadTag)

    def getTimestepSpec(self, tag="TriggerTime"):
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

        # skip files with no SliceLocation (eg scout views)
        skipCount = 0
        for f in self.filenames:
            fData = pydicom.dcmread(f)
            if hasattr(fData, 'SliceLocation'):
                self.sortedFileNames.append((fData, f))
            else:
                skipCount = skipCount + 1

        print("skipped, no SliceLocation: {}".format(skipCount))

        # ensure they are in the correct order
        self.sortedFileNames = sorted(self.sortedFileNames, key = lambda s: s[0].SliceLocation, reverse = True)

        for i in range(0, len(self.sortedFileNames)):
            self.sortedFileNames[i] = (self.sortedFileNames[i][1])

      #  print(self.sortedFileNames)
