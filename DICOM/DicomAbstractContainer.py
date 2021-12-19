from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

import numpy


# VIEW MODES
class ViewMode(Enum):
    ORIGINAL = "ORIGINAL"
    LUNGS_MASK = "LUNGS_MASK"
    SEGMENTED_LUNGS = "SEGMENTED_LUNGS"
    SEGMENTED_LUNGS_W_INTERNAL = "SEGMENTED_LUNGS_W_INTERNAL"
    NEGATIVE = "NEGATIVE"


class DicomAbstractContainerClass(ABC):

    def __init__(self):
        self._filename = None

    @classmethod
    def getPixelsArray(cls, scans):

        try:
            image = numpy.stack([s.pixel_array for s in scans])
            image = image.astype(numpy.int16)
            # Set outside-of-scan pixels to 0
            # The intercept is usually -1024, so air is approximately 0
            image[image == -2000] = 0

            # Convert to Hounsfield units (HU)
            try:  # TODO HANDLE FOR RGB
                intercept = scans[0].RescaleIntercept
                slope = scans[0].RescaleSlope

                if slope != 1:
                    image = slope * image.astype(numpy.float64)
                    image = image.astype(numpy.int16)

                image += numpy.int16(intercept)
            except:
                pass

            return numpy.array(image, dtype = numpy.int16)
        except Exception:
            return None

    @abstractmethod
    def addFile(self, filename, loadTag):
        pass

    @abstractmethod
    def getDicomFile(self, index):
        pass

    @abstractmethod
    def getExtraTagValues(self):
        pass

    @abstractmethod
    def getTagValues(self, names, index = 0):
        pass

    @abstractmethod
    def getPixelData(self, mode: ViewMode, index = 0):
        pass

    @property
    def filename(self) -> Optional[str]:
        return self._filename

    def getInstanceType(self) -> str:
        return self.__class__.__name__
        pass
