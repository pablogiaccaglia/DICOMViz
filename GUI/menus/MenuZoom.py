from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMenu


class MenuZoom(QMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar)
        self.menuBar = menuBar
        self.setObjectName("menuZoom")

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    def __defineActions(self):
        self.actionFillViewport = QtWidgets.QWidgetAction(self.menuBar)
        self.actionFillViewport.setObjectName("actionFillViewport")

        self.actionZoom100 = QtWidgets.QWidgetAction(self.menuBar)
        self.actionZoom100.setObjectName("actionZoom100")

        self.actionZoom200 = QtWidgets.QWidgetAction(self.menuBar)
        self.actionZoom200.setObjectName("actionZoom200")

        self.actionZoom400 = QtWidgets.QWidgetAction(self.menuBar)
        self.actionZoom400.setObjectName("actionZoom400")

        self.actionZoom800 = QtWidgets.QWidgetAction(self.menuBar)
        self.actionZoom800.setObjectName("actionZoom800")

        self.actionZoomIn = QtWidgets.QWidgetAction(self.menuBar)
        self.actionZoomIn.setObjectName("actionZoomIn")

        self.actionZoomOut = QtWidgets.QWidgetAction(self.menuBar)
        self.actionZoomOut.setObjectName("actionZoomOut")

    def __addActions(self):
        self.addAction(self.actionFillViewport)
        self.addAction(self.actionZoom100)
        self.addAction(self.actionZoom200)
        self.addAction(self.actionZoom400)
        self.addAction(self.actionZoom800)
        self.addSeparator()
        self.addAction(self.actionZoomIn)
        self.addAction(self.actionZoomOut)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Zoom"))

        self.actionFillViewport.setText(_translate("MainWindow", "Fill viewport"))
        self.actionFillViewport.setStatusTip(_translate("MainWindow", "Fill the whole visible viewport"))
        self.actionFillViewport.setShortcut(_translate("MainWindow", "Ctrl+0"))

        self.actionZoom100.setText(_translate("MainWindow", "100%"))
        self.actionZoom100.setStatusTip(_translate("MainWindow", "100% zoom in"))
        self.actionZoom100.setShortcut(_translate("MainWindow", "Ctrl+1"))

        self.actionZoom200.setText(_translate("MainWindow", "200%"))
        self.actionZoom200.setShortcut(_translate("MainWindow", "Ctrl+"))
        self.actionZoom200.setStatusTip(_translate("MainWindow", "200% zoom in"))

        self.actionZoom400.setText(_translate("MainWindow", "400%"))
        self.actionZoom400.setStatusTip(_translate("MainWindow", "400% zoom in"))

        self.actionZoom800.setText(_translate("MainWindow", "800%"))
        self.actionZoom800.setStatusTip(_translate("MainWindow", "800% zoom in"))

        self.actionZoomIn.setText(_translate("MainWindow", "Zoom in"))
        self.actionZoomIn.setStatusTip(_translate("MainWindow", "zooms in"))
        self.actionZoomIn.setShortcut(_translate("MainWindow", "Ctrl++"))

        self.actionZoomOut.setText(_translate("MainWindow", "Zoom out"))
        self.actionZoomOut.setStatusTip(_translate("MainWindow", "zooms out"))
        self.actionZoomOut.setShortcut(_translate("MainWindow", "Ctrl+-"))