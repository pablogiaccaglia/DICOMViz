import pyqtgraph
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMenu
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
