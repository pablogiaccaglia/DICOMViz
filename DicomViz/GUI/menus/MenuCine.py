from PyQt6 import QtCore, QtWidgets

from .AbstractMenu import AbstractMenu


class MenuCine(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuCine")

        self.window = menuBar.window

        self._translate = QtCore.QCoreApplication.translate
        self._defineActions()
        self._addActions()
        self._retranslateUI()
        self._actionAnimateSeries.setEnabled(False)

    def toggleActions(self, value: bool, dicomContainer = None) -> None:
        if value and self.menuBar.window.dicomHandler.isSeriesImageSelected():
            self._actionAnimateSeries.setEnabled(value)
        if not value:
            self._actionAnimateSeries.setEnabled(value)

    def changeAnimateActionText(self, isAnimationOn: bool) -> None:

        if isAnimationOn:
            self._actionAnimateSeries.setText(self._translate("MainWindow", "Stop Animation"))
        else:
            self._actionAnimateSeries.setText(self._translate("MainWindow", "Animate"))

    def _defineActions(self) -> None:
        self._actionAnimateSeries = QtWidgets.QWidgetAction(self.menuBar)
        self._actionAnimateSeries.setObjectName("actionAnimateSeries")
        self._actionAnimateSeries.triggered.connect(self.toggleGifHandlerToGraphicsView)

    def _addActions(self) -> None:
        self.addAction(self._actionAnimateSeries)

    def _retranslateUI(self) -> None:

        self.setTitle(self._translate("MainWindow", "Cine"))

        self._actionAnimateSeries.setText(self._translate("MainWindow", "Animate"))
        self._actionAnimateSeries.setStatusTip(self._translate("MainWindow", "Animate series "))

    def toggleGifHandlerToGraphicsView(self) -> None:

        isAnimationOn = self.window.graphicsView.isAnimationOn()

        if isAnimationOn:
            self.window.graphicsView.stopAnimationHandler()
        else:
            self.window.graphicsView.addAnimationHandler()

        self.changeAnimateActionText(isAnimationOn = self.window.graphicsView.isAnimationOn())
