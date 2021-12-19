import pyqtgraph
from PyQt6 import QtCore, QtGui

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
        self._DEFAULT_WIDTH = 512
        self._DEFAULT_HEIGHT = 512
        self._DEFAULT_LEFT = 0.0
        self._DEFAULT_TOP = 0.0
        self._currentWidth = self._DEFAULT_WIDTH
        self._currentHeight = self._DEFAULT_HEIGHT
        self._currentLeft = self._DEFAULT_LEFT
        self._currentTop = self._DEFAULT_TOP

    def zoomOut(self) -> None:
        self.zoom(-7, -7, 15, 15)

    def zoomIn(self) -> None:
        self.zoom(7, 7, -15, -15)

    def setViewSize(self, left, top, width, height) -> None:
        self._currentWidth = width
        self._currentHeight = height

        self._currentLeft = left
        self._currentTop = top

        rect = QtCore.QRectF(self._currentLeft,
                             self._currentTop,
                             self._currentWidth,
                             self._currentHeight)
        self.setRange(rect = rect)

    def zoom(self, deltaLeft, deltaTop, deltaWidth, deltaHeight) -> None:
        self.setViewSize(self._currentLeft + deltaLeft,
                         self._currentTop + deltaTop,
                         self._currentWidth + deltaWidth,
                         self._currentHeight + deltaHeight)

    def resetSize(self) -> None:
        self._currentWidth = self._DEFAULT_WIDTH
        self._currentHeight = self._DEFAULT_HEIGHT

    def emitShowT0(self) -> None:
        """
            Emit signalShowT0
            """
        self.signalShowT0.emit()

    def emitShowS0(self) -> None:
        """
            Emit signalShowS0
            """
        self.signalShowS0.emit()

    def setRectMode(self) -> None:
        """
            Set mouse mode to rect
            """
        self.setMouseMode(self.RectMode)

    def setPanMode(self) -> None:
        """
            Set mouse mode to pan
            """
        self.setMouseMode(self.PanMode)

    def raiseContextMenu(self, ev) -> None:
        menu = self.getMenu(ev)
        actionNames = [action.objectName() for action in menu.actions()]

        if menu is not None and "Copy" not in actionNames:
            self.__addCopyActionToViewBoxMenu()
            self.scene().addParentContextMenus(self, menu, ev)

        menu.popup(ev.screenPos().toPoint())

    def __addCopyActionToViewBoxMenu(self) -> None:
        self.menu.copyAction = QtGui.QAction(translate("ViewBox", "Copy"), self.menu)
        self.menu.copyAction.setObjectName("Copy")
        self.menu.copyAction.triggered.connect(self.imageView.copyImageToClipboard)
        self.menu.addAction(self.menu.copyAction)
