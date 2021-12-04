import pyqtgraph
from PyQt6 import QtCore, QtGui
from pyqtgraph.graphicsItems.ViewBox.ViewBoxMenu import ViewBoxMenu

translate = QtCore.QCoreApplication.translate


class CustomViewBox(pyqtgraph.ViewBox):
    """
        Subclass of ViewBox
        """
    signalShowT0 = QtCore.pyqtSignal()
    signalShowS0 = QtCore.pyqtSignal()

    def __init__(self, parent = None, imageView = None):
        """
            Constructor of the CustomViewBox
            """
        super().__init__(parent)
        self.imageView = imageView
        # self.setRectMode()  # Set mouse mode to rect for convenient zooming
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

    def raiseContextMenu(self, ev):
        menu = self.getMenu(ev)
        actionNames = [action.objectName() for action in menu.actions()]

        if menu is not None and "Copy" not in actionNames:
            self.__addCopyActionToViewBoxMenu()
            self.scene().addParentContextMenus(self, menu, ev)

        menu.popup(ev.screenPos().toPoint())

    def __addCopyActionToViewBoxMenu(self):
        self.menu.copyAction = QtGui.QAction(translate("ViewBox", "Copy"), self.menu)
        self.menu.copyAction.setObjectName("Copy")
        self.menu.copyAction.triggered.connect(self.imageView.copyImageToClipboard)
        self.menu.addAction(self.menu.copyAction)
