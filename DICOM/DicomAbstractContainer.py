from abc import ABC, abstractmethod


class DicomAbstractContainerClass(ABC):

    @abstractmethod
    def addFile(self, filename, loadTag):
        pass

    @abstractmethod
    def getTagObject(self, index):
        pass

    @abstractmethod
    def getExtraTagValues(self):
        pass

    @abstractmethod
    def getTagValues(self, names, index=0):
        pass

    @abstractmethod
    def getPixelData(self, index):
        pass