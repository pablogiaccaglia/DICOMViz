from enum import Enum

from PyQt6 import QtWidgets, QtCore
from functools import partial
from builtins import tuple

from GUI.menus.AbstractMenu import AbstractMenu


class ZoomAmount(tuple, Enum):
    ZOOM_100 = (400, -49)
    ZOOM_200 = (300, -98)
    ZOOM_400 = (250, -119)
    ZOOM_800 = (120, -182)


class MenuZoom(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuZoom")
        self.graphicsView = menuBar.window.graphicsView

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()
        self.actions = [self._actionZoom100,
                        self._actionZoom200,
                        self._actionZoom400,
                        self._actionZoom800,
                        self._actionZoomIn,
                        self._actionZoomOut,
                        self.actionFillViewport]

        self.toggleActions(False)

    def toggleActions(self, value: bool, dicomContainer = None) -> None:
        for action in self.actions:
            action.setEnabled(value)

    def __defineActions(self) -> None:
        self.actionFillViewport = QtWidgets.QWidgetAction(self.menuBar)
        self.actionFillViewport.setObjectName("actionFillViewport")
        self.actionFillViewport.triggered.connect(self.graphicsView.autoRange)

        self._actionZoom100 = QtWidgets.QWidgetAction(self.menuBar)
        self._actionZoom100.setObjectName("actionZoom100")
        self._actionZoom100.triggered.connect(
                partial(self.graphicsView.setViewSize,
                        ZoomAmount.ZOOM_100.value[1],
                        ZoomAmount.ZOOM_100.value[1],
                        ZoomAmount.ZOOM_100.value[0],
                        ZoomAmount.ZOOM_100.value[0]))

        self._actionZoom200 = QtWidgets.QWidgetAction(self.menuBar)
        self._actionZoom200.setObjectName("_actionZoom200")
        self._actionZoom200.triggered.connect(
                partial(self.graphicsView.setViewSize,
                        ZoomAmount.ZOOM_200.value[1],
                        ZoomAmount.ZOOM_200.value[1],
                        ZoomAmount.ZOOM_200.value[0],
                        ZoomAmount.ZOOM_200.value[0]))

        self._actionZoom400 = QtWidgets.QWidgetAction(self.menuBar)
        self._actionZoom400.setObjectName("_actionZoom400")
        self._actionZoom400.triggered.connect(
                partial(self.graphicsView.setViewSize,
                        ZoomAmount.ZOOM_400.value[1],
                        ZoomAmount.ZOOM_400.value[1],
                        ZoomAmount.ZOOM_400.value[0],
                        ZoomAmount.ZOOM_400.value[0]))

        self._actionZoom800 = QtWidgets.QWidgetAction(self.menuBar)
        self._actionZoom800.setObjectName("_actionZoom800")
        self._actionZoom800.triggered.connect(
                partial(self.graphicsView.setViewSize,
                        ZoomAmount.ZOOM_800.value[1],
                        ZoomAmount.ZOOM_800.value[1],
                        ZoomAmount.ZOOM_800.value[0],
                        ZoomAmount.ZOOM_800.value[0]))

        self._actionZoomIn = QtWidgets.QWidgetAction(self.menuBar)
        self._actionZoomIn.setObjectName("_actionZoomIn")
        self._actionZoomIn.triggered.connect(self.graphicsView.zoomIn)

        self._actionZoomOut = QtWidgets.QWidgetAction(self.menuBar)
        self._actionZoomOut.setObjectName("_actionZoomOut")
        self._actionZoomOut.triggered.connect(self.graphicsView.zoomOut)

    def __addActions(self) -> None:
        self.addAction(self.actionFillViewport)
        self.addAction(self._actionZoom100)
        self.addAction(self._actionZoom200)
        self.addAction(self._actionZoom400)
        self.addAction(self._actionZoom800)
        self.addSeparator()
        self.addAction(self._actionZoomIn)
        self.addAction(self._actionZoomOut)

    def __retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Zoom"))

        self.actionFillViewport.setText(_translate("MainWindow", "Fill viewport"))
        self.actionFillViewport.setStatusTip(_translate("MainWindow", "Fill the whole visible viewport"))
        # self.actionFillViewport.setShortcut(_translate("MainWindow", "Ctrl+0"))

        self._actionZoom100.setText(_translate("MainWindow", "100%"))
        self._actionZoom100.setStatusTip(_translate("MainWindow", "100% zoom in"))
        # self._actionZoom100.setShortcut(_translate("MainWindow", "Ctrl+1"))

        self._actionZoom200.setText(_translate("MainWindow", "200%"))
        # self._actionZoom200.setShortcut(_translate("MainWindow", "Ctrl+"))
        self._actionZoom200.setStatusTip(_translate("MainWindow", "200% zoom in"))

        self._actionZoom400.setText(_translate("MainWindow", "400%"))
        self._actionZoom400.setStatusTip(_translate("MainWindow", "400% zoom in"))

        self._actionZoom800.setText(_translate("MainWindow", "800%"))
        self._actionZoom800.setStatusTip(_translate("MainWindow", "800% zoom in"))

        self._actionZoomIn.setText(_translate("MainWindow", "Zoom in"))
        self._actionZoomIn.setStatusTip(_translate("MainWindow", "zooms in"))
        # self._actionZoomIn.setShortcut(_translate("MainWindow", "Ctrl++"))

        self._actionZoomOut.setText(_translate("MainWindow", "Zoom out"))
        self._actionZoomOut.setStatusTip(_translate("MainWindow", "zooms out"))
        # self._actionZoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))
