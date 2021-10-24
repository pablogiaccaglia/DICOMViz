from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMenu


class MenuExport(QMenu):
    def __init__(self, menuBar):
        super().__init__(menuBar)
        self.menuBar = menuBar
        self.setObjectName("menuExport")

        self.__defineActions()
        self.__addActions()
        self.__retransalteUI()

    def __defineActions(self):
        self.actionExportImages = QtWidgets.QWidgetAction(self.menuBar)
        self.actionExportImages.setObjectName("actionExportImages")

        self.actionCopy_to_clipboard = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCopy_to_clipboard.setObjectName("actionCopy_to_clipboard")

        self.actionCopy_all_to_clipboard = QtWidgets.QWidgetAction(self.menuBar)
        self.actionCopy_all_to_clipboard.setObjectName("actionCopy_all_to_clipboard")

    def __addActions(self):
        self.addAction(self.actionExportImages)

        self.addSeparator()

        self.addAction(self.actionCopy_to_clipboard)
        self.addAction(self.actionCopy_all_to_clipboard)

    def __retransalteUI(self):
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
