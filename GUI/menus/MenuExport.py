from PyQt6 import QtWidgets, QtCore

from GUI.menus.AbstractMenu import AbstractMenu


class MenuExport(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuExport")
        self._graphicsView = menuBar.window.graphicsView
        self._window = menuBar.window

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    def toggleActions(self, value: bool, dicomContainer = None):
        self._actionExportImages.setEnabled(value)
        self._actionCopy_to_clipboard.setEnabled(value)

    def _copyToClipboard(self) -> None:
        self.menuBar.window.dicomHandler.copyImageToClipboard()

    def __defineActions(self) -> None:
        self._actionExportImages = QtWidgets.QWidgetAction(self.menuBar)
        self._actionExportImages.setObjectName("_actionExportImages")
        self._actionExportImages.triggered.connect(self.__exportImages)
        self._actionExportImages.setDisabled(True)

        self._actionCopy_to_clipboard = QtWidgets.QWidgetAction(self.menuBar)
        self._actionCopy_to_clipboard.setObjectName("_actionCopy_to_clipboard")
        self._actionCopy_to_clipboard.triggered.connect(self._copyToClipboard)
        self._actionCopy_to_clipboard.setDisabled(True)

    def __exportImages(self) -> None:
        if self.menuBar.window.dicomHandler.isSeriesImageSelected():
            self.menuBar.window.dicomHandler.prepareGifExporter()
        self._graphicsView.showExportDialog()

    def __addActions(self) -> None:
        self.addAction(self._actionExportImages)

        self.addSeparator()

        self.addAction(self._actionCopy_to_clipboard)

    def __retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Export"))

        self._actionExportImages.setText(_translate("MainWindow", "Export image"))
        self._actionExportImages.setStatusTip(_translate("MainWindow", "Export images in different formats"))
        # self._actionExportImages.setShortcut(_translate("MainWindow", "Ctrl+E"))

        self._actionCopy_to_clipboard.setText(_translate("MainWindow", "Copy to clipboard"))
        self._actionCopy_to_clipboard.setStatusTip(_translate("MainWindow", "Copy image to clipboard"))
        # self._actionCopy_to_clipboard.setShortcut(_translate("MainWindow", "Ctrl+C"))
