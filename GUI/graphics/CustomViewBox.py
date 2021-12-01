import pyqtgraph
from PyQt6 import QtCore
from pyqtgraph.graphicsItems.ViewBox.ViewBoxMenu import ViewBoxMenu


class CustomViewBox(pyqtgraph.ViewBox):
    """
        Subclass of ViewBox
        """
    signalShowT0 = QtCore.pyqtSignal()
    signalShowS0 = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        """
            Constructor of the CustomViewBox
            """
        super().__init__(parent)
        # self.setRectMode()  # Set mouse mode to rect for convenient zooming
        self.menu = ViewBoxMenu(self)  # Create the menu
        self.DEFAULT_WIDTH = 512
        self.DEFAULT_HEIGHT = 512
        self.DEFAULT_LEFT = 0.0
        self.DEFAULT_TOP = 0.0
        self.currentWidth = self.DEFAULT_WIDTH
        self.currentHeight = self.DEFAULT_HEIGHT
        self.currentLeft = self.DEFAULT_LEFT
        self.currentTop = self.DEFAULT_TOP

    def zoomOut(self):
        self.zoom(-7, -7, 15, 15)

    def zoomIn(self):
        self.zoom(7, 7, -15, -15)

    def setViewSize(self, left, top, width, height):
        self.currentWidth = width
        self.currentHeight = height

        # currentQRect = self.viewRect()
        self.currentLeft = left
        self.currentTop = top

        rect = QtCore.QRectF(self.currentLeft, self.currentTop, self.currentWidth, self.currentHeight)
        self.setRange(rect = rect)

    def zoom(self, deltaLeft, deltaTop, deltaWidth, deltaHeight):
        self.setViewSize(self.currentLeft + deltaLeft, self.currentTop + deltaTop, self.currentWidth + deltaWidth,
                         self.currentHeight + deltaHeight)

    def resetSize(self):
        self.currentWidth = self.DEFAULT_WIDTH
        self.currentHeight = self.DEFAULT_HEIGHT

    def emitShowT0(self):
        """
            Emit signalShowT0
            """
        self.signalShowT0.emit()

    def emitShowS0(self):
        """
            Emit signalShowS0
            """
        self.signalShowS0.emit()

    def setRectMode(self):
        """
            Set mouse mode to rect
            """
        self.setMouseMode(self.RectMode)

    def setPanMode(self):
        """
            Set mouse mode to pan
            """
        self.setMouseMode(self.PanMode)
