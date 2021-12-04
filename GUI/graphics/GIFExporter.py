import threading

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
from pyqtgraph.exporters import Exporter
from pyqtgraph.parametertree import Parameter
import imageio

translate = QtCore.QCoreApplication.translate

__all__ = ['GIFExporter']


class GIFExporter(Exporter, QWidget):
    Name = "Graphic Interchange Format"
    windows = []
    GIFData = None
    exportGIFSignal = QtCore.pyqtSignal()
    speed = 50

    def __init__(self, item):

        Exporter.__init__(self, item)
        QWidget.__init__(self)
        tr = self.getTargetRect()

        self.width = int(tr.width())
        self.height = int(tr.height())
        self.speed = GIFExporter.speed
        self.exportGIFSignal.connect(self.saveGIF)

        self.params = Parameter(name = 'params', type = 'group', children = [
            {'name':   'width', 'title': translate("Exporter", 'width'), 'type': 'int', 'value': self.width,
             'limits': (0, None)},
            {'name':   'height', 'title': translate("Exporter", 'height'), 'type': 'int', 'value': self.height,
             'limits': (0, None)},
            {'name':   'speed', 'title': translate("Exporter", 'speed'), 'type': 'int', 'value': self.speed,
             'limits': [1, None]}
        ])

        self.params.param('width').sigValueChanged.connect(self.widthChanged)
        self.params.param('height').sigValueChanged.connect(self.heightChanged)
        # self.params.param('speed').sigValueChanged.connect(self.speedChanged)
        self.fileName = None

    @classmethod
    def setGIFData(cls, gifData):
        GIFExporter.GIFData = gifData

    @classmethod
    def unregister(cls):
        try:
            Exporter.Exporters.remove(cls)
        except ValueError:
            pass  # do nothing! Thread safe, better than an if check

    def speedChanged(self):
        # self.params.param('speed').setValue()
        pass

    def widthChanged(self):
        sr = self.getSourceRect()
        ar = float(sr.height()) / sr.width()
        self.height = int(self.params['width'] * ar)
        self.params.param('height').setValue(self.height, blockSignal = self.heightChanged)

    def heightChanged(self):
        sr = self.getSourceRect()
        ar = float(sr.width()) / sr.height()
        self.width = int(self.params['height'] * ar)
        self.params.param('width').setValue(self.width, blockSignal = self.widthChanged)

    def parameters(self):
        return self.params

    def export(self, fileName = None, toBytes = False, copy = False):
        if fileName is None and not toBytes and not copy:
            self.fileSaveDialog(filter = ['*.gif'])
            return

        w = int(self.params['width'])
        h = int(self.params['height'])
        s = int(self.params['speed'])

        if w == 0 or h == 0:
            raise Exception("Cannot export gifs with size=0 (requested "
                            "export size is %dx%d)" % (w, h))

        if s == 0:
            raise Exception("Cannot export gifs with speed=0 (requested " "export speed is %d)" % s)

        self.fileName = fileName
        self.exportGIFSignal.emit()

    def saveGIF(self):
        imageio.mimsave(f'./{self.fileName}', GIFExporter.GIFData, duration = self.speed)
