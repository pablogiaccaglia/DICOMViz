from PyQt6 import QtWidgets, QtCore

from GUI.menus.AbstractMenu import AbstractMenu


class MenuExport(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuExport")
        self.graphicsView = menuBar.window.graphicsView

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    def __defineActions(self):
        self.actionExportImages = QtWidgets.QWidgetAction(self.menuBar)
        self.actionExportImages.setObjectName("actionExportImages")
        self.actionExportImages.triggered.connect(self.__exportImages)
        self.actionExportImages.setDisabled(True)

        self.actionCopy_to_clipboard = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCopy_to_clipboard.setObjectName("actionCopy_to_clipboard")
        self.actionCopy_to_clipboard.triggered.connect(self.__copyToClipboard)
        self.actionCopy_to_clipboard.setDisabled(True)

        self.actionCopy_all_to_clipboard = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCopy_all_to_clipboard.setObjectName("actionCopy_all_to_clipboard")
        self.actionCopy_all_to_clipboard.setDisabled(True)

    def __exportImages(self):
        if self.menuBar.window.dicomHandler.isSeriesImageSelected():
            self.menuBar.window.dicomHandler.prepareGifExporter()
        self.graphicsView.showExportDialog()


    def __addActions(self):
        self.addAction(self.actionExportImages)

        self.addSeparator()

        self.addAction(self.actionCopy_to_clipboard)
        self.addAction(self.actionCopy_all_to_clipboard)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Export"))

        self.actionExportImages.setText(_translate("MainWindow", "Export images"))
        self.actionExportImages.setStatusTip(_translate("MainWindow", "Export images in different formats"))
        self.actionExportImages.setShortcut(_translate("MainWindow", "Ctrl+E"))

        self.actionCopy_to_clipboard.setText(_translate("MainWindow", "Copy to clipboard"))
        self.actionCopy_to_clipboard.setStatusTip(_translate("MainWindow", "Copy image to clipboard"))
        self.actionCopy_to_clipboard.setShortcut(_translate("MainWindow", "Ctrl+C"))

        self.actionCopy_all_to_clipboard.setText(_translate("MainWindow", "Copy all to clipboard"))
        self.actionCopy_all_to_clipboard.setStatusTip(_translate("MainWindow", "Copy all images to clipboard"))
        self.actionCopy_all_to_clipboard.setShortcut(_translate("MainWindow", "Shift+C"))

    def toggleActions(self, value: bool, dicomContainer = None):
        self.actionExportImages.setEnabled(value)
        self.actionCopy_to_clipboard.setEnabled(value)
        self.actionCopy_all_to_clipboard.setEnabled(value)

    def __copyToClipboard(self):
        self.menuBar.window.dicomHandler.copyImageToClipboard()

