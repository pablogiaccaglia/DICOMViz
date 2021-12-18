from functools import partial

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMenu

from GUI.menus.AbstractMenu import AbstractMenu


class MenuCine(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuCine")

        self._translate = QtCore.QCoreApplication.translate
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
        self.actionAnimateSeries.triggered.connect(self.__toggleGifHandlerToGraphicsView)

    def __addActions(self):
        self.addAction(self.actionAnimateSeries)

    def __retranslateUI(self):

        self.setTitle(self._translate("MainWindow", "Cine"))

        self.actionAnimateSeries.setText(self._translate("MainWindow", "Animate"))
        self.actionAnimateSeries.setStatusTip(self._translate("MainWindow", "Animate series "))
        self.actionAnimateSeries.setShortcut(self._translate("MainWindow", "Ctrl+'"))

    def changeAnimateActionText(self, isAnimationOn: bool):

        if isAnimationOn:
            self.actionAnimateSeries.setText(self._translate("MainWindow", "Stop Animation"))
        else:
            self.actionAnimateSeries.setText(self._translate("MainWindow", "Animate"))

    def __toggleGifHandlerToGraphicsView(self):

        isAnimationOn = self.menuBar.window.graphicsView.isAnimationOn()

        if isAnimationOn:
            self.menuBar.window.graphicsView.stopGifHandler()
        else:
            self.menuBar.window.graphicsView.addGifHandler()

        self.changeAnimateActionText(isAnimationOn = self.menuBar.window.graphicsView.isAnimationOn())
