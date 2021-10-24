from pydicom import dicomio
from DICOM.DicomAbstractContainer import DicomAbstractContainerClass


class DicomFile(DicomAbstractContainerClass):

    def __init__(self, rootDir):
        self.rootDir = rootDir  # directory Dicoms were loaded from, files for this series may be in subdirectories
        self.filename = ""  # list of filenames for the Dicom associated with this series
        self.loadTag = ("", "")  # loaded abbreviated tag->(name,value)
        self.imgCache = []

    def addFile(self, filename, loadTag):
        """Add a filename and abbreviated tag map, previously stored file will be lost."""
        self.filename = filename
        self.loadTag = loadTag
        pass

    def getTagObject(self, index = None):
        """Get the object storing tag information from Dicom file."""
        dcm = dicomio.read_file(self.filename, stop_before_pixels = True)
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

    def getPixelData(self, index = None):
        """Get the pixel data array for file at position `index` in self.filenames, or None if no pixel data."""
        if not self.imgCache:
            try:
                dcm = dicomio.read_file(self.filename)
                rslope = float(dcm.get("RescaleSlope", 1) or 1)
                rinter = float(dcm.get("RescaleIntercept", 0) or 0)
                img = dcm.pixel_array * rslope + rinter
            except:
                img = None  # exceptions indicate that the pixel data doesn't exist or isn't readable so ignore

            self.imgCache = img

        return self.imgCache
