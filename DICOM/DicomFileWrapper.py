from typing import Optional
from typing import Union

import pydicom
import os

from pydicom import FileDataset
from pydicom.dicomdir import DicomDir

from DICOM.DicomAbstractContainer import DicomAbstractContainerClass, ViewMode
import numpy
from numpy import ndarray

from alterations import utils


class DicomFileWrapper(DicomAbstractContainerClass):

    def __init__(self, fileName, dicomData = None, dicomMasks = None, originalImg = None, segmentedLungsImg = None):
        super().__init__()

        self._rootDir = None
        self._dicomData = None
        self._originalImgNpArray = None
        self._dicomMasks = None
        self._segmentedLungsImg = None
        self._loadTag = None
        self._lungsMaskImg = None
        self._modes = None

        self._setupFileWrapper(fileName = fileName,
                               dicomData = dicomData,
                               dicomMasks = dicomMasks,
                               originalImg = originalImg,
                               segmentedLungsImg = segmentedLungsImg)

    @property
    def rootDirectory(self) -> str:
        return self._rootDir

    @property
    def dicomData(self) -> Union[FileDataset, DicomDir]:
        return self._dicomData

    @property
    def originalImgNumpyArray(self) -> ndarray:
        return self._originalImgNpArray

    @property
    def dicomMasks(self) -> tuple:
        return self._dicomMasks

    @property
    def segmentedLungsImage(self) -> ndarray:
        return self._segmentedLungsImg

    @property
    def segmentedLungsImg(self) -> ndarray:
        return self._segmentedLungsImg

    @property
    def viewModes(self) -> dict:
        return self._modes

    def _setupFileWrapper(self, fileName,
                          dicomData = None,
                          dicomMasks = None,
                          originalImg = None,
                          segmentedLungsImg = None):

        self._rootDir = os.path.dirname(
                fileName)  # directory Dicoms were loaded from, files for this series may be in subdirectories
        self._filename = fileName  # DicomFile Object associated file path

        if dicomData is None:
            self._dicomData = pydicom.dcmread(self._filename)
        else:
            self._dicomData = dicomData

        if originalImg is None:
            self._originalImgNpArray = self.getPixelsArray([self._dicomData])
        else:
            self._originalImgNpArray = numpy.array([originalImg], numpy.int16)

        if dicomMasks is None:
            try:  # TODO HANDLE THIS FOR RGB
                self._dicomMasks = utils.getDicomMasks(self._originalImgNpArray, -70)
            except:
                self._dicomMasks = None
                pass
        else:
            self._dicomMasks = dicomMasks

        if segmentedLungsImg is None and self._dicomMasks is not None:
            self._segmentedLungsImg = utils.getSegmentedLungPixels(self._originalImgNpArray,
                                                                   self._dicomMasks.segmentedLungsFill)
        else:
            self._segmentedLungsImg = segmentedLungsImg

        self._loadTag = ("", "")  # loaded abbreviated tag->(name,value)

        self._lungsMaskImg = self._dicomMasks.segmentedLungsFill if self._dicomMasks is not None else None

        self._modes = {
            ViewMode.ORIGINAL:                   self._originalImgNpArray,
            ViewMode.LUNGS_MASK:                 self._lungsMaskImg,
            ViewMode.SEGMENTED_LUNGS:            self._segmentedLungsImg,
            ViewMode.SEGMENTED_LUNGS_W_INTERNAL: "SegmentedLungsWithInternalStructure",
        }

    def addFile(self, filename, loadTag) -> None:
        """Add a filename and abbreviated tag map, previously stored file will be lost."""
        self._filename = filename
        self._loadTag = loadTag

    def getDicomFile(self, index = None) -> Union[FileDataset, DicomDir]:
        """Get the object storing tag information from Dicom file."""
        return self._dicomData

    def getExtraTagValues(self) -> dict:
        return {}

    def getTagValues(self, names, index = None) -> tuple:
        """Get the tag values for tag names listed in `names' for image at the given index."""
        if not self._filename:
            return ()

        dcm = self.getDicomFile(index)
        extraVals = self.getExtraTagValues()

        return tuple(str(dcm.get(n, extraVals.get(n, ""))) for n in names)

    def getPixelData(self, mode: ViewMode, index = 0) -> Optional[ndarray]:
        if mode in self._modes:
            return self._modes[mode]
        else:
            return None

    def updateMasks(self, param) -> None:
        self._dicomMasks = utils.getDicomMasks(self._originalImgNpArray, param)
        self._segmentedLungsImg = utils.getSegmentedLungPixels(self._originalImgNpArray,
                                                               self._dicomMasks.segmentedLungsFill)
        self._lungsMaskImg = self._dicomMasks.segmentedLungsFill

        self._modes[ViewMode.LUNGS_MASK] = self._lungsMaskImg
        self._modes[ViewMode.SEGMENTED_LUNGS] = self._segmentedLungsImg
