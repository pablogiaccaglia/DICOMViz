import pydicom
import os

from DICOM.DicomAbstractContainer import DicomAbstractContainerClass, ViewMode
import numpy

from alterations import utils


class DicomFile(DicomAbstractContainerClass):

    def __init__(self, fileName, dicomData = None, dicomMasks = None, originalImg = None, segmentedLungsImg = None):
        super().__init__()
        self.rootDir = os.path.dirname(
                fileName)  # directory Dicoms were loaded from, files for this series may be in subdirectories
        self.filename = fileName  # DicomFile Object associated file path

        if dicomData is None:
            self.dicomData = pydicom.dcmread(self.filename)
        else:
            self.dicomData = dicomData

        if originalImg is None:
            self.originalImgNpArray = self.get_pixels_hu([self.dicomData])
        else:
            self.originalImgNpArray = numpy.array([originalImg], numpy.int16)

        if dicomMasks is None:
            self.dicomMasks = utils.getDicomMasks(self.originalImgNpArray, -70)
        else:
            self.dicomMasks = dicomMasks

        if segmentedLungsImg is None:
            self.segmentedLungsImg = utils.getSegmentedLungPixels(self.originalImgNpArray,
                                                                  self.dicomMasks.segmentedLungsFill)
        else:
            self.segmentedLungsImg = segmentedLungsImg

        self.loadTag = ("", "")  # loaded abbreviated tag->(name,value)

        self.modes = {
            ViewMode.ORIGINAL:                   self.originalImgNpArray,
            ViewMode.LUNGS_MASK:                 self.dicomMasks.segmentedLungsFill,
            ViewMode.SEGMENTED_LUNGS:            self.segmentedLungsImg,
            ViewMode.SEGMENTED_LUNGS_W_INTERNAL: "SegmentedLungsWithInternalStructure",
        }

    def addFile(self, filename, loadTag):
        """Add a filename and abbreviated tag map, previously stored file will be lost."""
        self.filename = filename
        self.loadTag = loadTag
        pass

    def getTagObject(self, index = None):
        """Get the object storing tag information from Dicom file."""
        dcm = pydicom.dcmread(self.filename, stop_before_pixels = True)
        return dcm

    def getExtraTagValues(self):
        """Return the extra tag values calculated from the series tag info stored in self.filenames."""
        #  start, interval, numTimes = self.getTimestepSpec()
        extraVals = {
            "blabla": "blabla"
                      """ "NumImages":    len(self.filenames),
            "TimestepSpec": "start: %i, interval: %i, # Steps: %i"
                            % (start, interval, numTimes),
            "StartTime":    start,
            "NumTimesteps": numTimes,
            "TimeInterval": interval,"""
        }

        return extraVals

    def getTagValues(self, names, index = None):
        """Get the tag values for tag names listed in `names' for image at the given index."""
        if not self.filename:
            return ()

        dcm = self.getTagObject(index)
        extraVals = self.getExtraTagValues()

        # TODO: kludge? More general solution of telling series apart
        # dcm.SeriesDescription=dcm.get('SeriesDescription',dcm.get('SeriesInstanceUID','???'))

        return tuple(str(dcm.get(n, extraVals.get(n, ""))) for n in names)

    def getPixelData(self, mode: ViewMode, index = 0):
        if mode in self.modes:
            return self.modes[mode]
        else:
            return None

    def updateMasks(self, param):
        self.dicomMasks = utils.getDicomMasks(self.originalImgNpArray, param)
        self.segmentedLungsImg = utils.getSegmentedLungPixels(self.originalImgNpArray,
                                                              self.dicomMasks.segmentedLungsFill)
        self.modes[ViewMode.LUNGS_MASK] = self.dicomMasks.segmentedLungsFill
        self.modes[ViewMode.SEGMENTED_LUNGS] = self.segmentedLungsImg
