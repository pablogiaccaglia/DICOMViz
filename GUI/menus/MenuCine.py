from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMenu

from GUI.menus.AbstractMenu import AbstractMenu


class MenuCine(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuCine")

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()
        self.actionAnimateSeries.setEnabled(False)

    def toggleActions(self, value: bool, dicomContainer = None):
        if value and self.menuBar.window.dicomHandler.isSeriesImageSelected():
            self.actionAnimateSeries.setEnabled(value)
        if not value:
            self.actionAnimateSeries.setEnabled(value)
        pass

    def __defineActions(self):
        self.actionAnimateSeries = QtWidgets.QWidgetAction(self.menuBar)
        self.actionAnimateSeries.setObjectName("actionAnimateSeries")
        self.actionAnimateSeries.triggered.connect(self.__addGifHandlerToGraphicsView)

    def __addActions(self):
        self.addAction(self.actionAnimateSeries)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "Cine"))

        self.actionAnimateSeries.setText(_translate("MainWindow", "Animate"))
        self.actionAnimateSeries.setStatusTip(_translate("MainWindow", "Animate series"))
        self.actionAnimateSeries.setShortcut(_translate("MainWindow", "Ctrl+'"))

    def __addGifHandlerToGraphicsView(self):
        self.menuBar.window.graphicsView.addGifHandler()