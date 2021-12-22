from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QFileDialog

from .AbstractMenu import AbstractMenu
from ...DICOM.DicomSeries import DicomSeries


class MenuFiles(AbstractMenu, QDialog):

    def __init__(self, menuBar):

        super().__init__(menuBar, "menuFiles")
        self.setToolTip("")
        self.window = menuBar.window
        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    def toggleActions(self, value: bool, dicomContainer = None) -> None:

        self.actionRemoveFromView.setEnabled(value)

        if isinstance(dicomContainer, DicomSeries) or not value:
            self.toggleActionRemoveSeries(value)

    def toggleActionRemoveSeries(self, value: bool) -> None:
        self.actionRemoveSeries.setEnabled(value)

    def toggleFilesActions(self, value: bool) -> None:
        self.actionOpenDICOMFile.setEnabled(value)
        self.actionOpenDICOMFolder.setEnabled(value)

    def __defineActions(self) -> None:

        self.actionOpenDICOMFile = QtWidgets.QWidgetAction(self.menuBar)
        self.actionOpenDICOMFile.setObjectName("actionOpenDICOMFile")
        self.actionOpenDICOMFile.triggered.connect(self.__openDICOMFile)

        self.actionOpenDICOMFolder = QtWidgets.QWidgetAction(self.menuBar)
        self.actionOpenDICOMFolder.setObjectName("actionOpenDICOMFolder")
        self.actionOpenDICOMFolder.triggered.connect(self.__openDICOMFolder)

        self.actionRemoveFromView = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRemoveFromView.setObjectName("actionRemoveFromView")
        self.actionRemoveFromView.triggered.connect(self.menuBar.window.dicomHandler.removeImageFromView)

        self.actionRemoveSeries = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRemoveSeries.setObjectName("actionRemoveSeries")
        self.actionRemoveSeries.triggered.connect(self.menuBar.window.dicomHandler.removeSeries)

        self.toggleActions(False)

    def __addActions(self) -> None:
        self.addSeparator()

        self.addAction(self.actionOpenDICOMFile)
        self.addAction(self.actionOpenDICOMFolder)

        self.addSeparator()

        self.addAction(self.actionRemoveFromView)
        self.addAction(self.actionRemoveSeries)

    def __openDICOMFolder(self) -> None:

        """
        dialog = QFileDialog(self.window)
        dialog.setWindowTitle("Select Directory")
        dialog.setDirectory(self.window.dicomHandler.lastLoadFolderDirectory)
        dialog.setOption(QtWidgets.QFileDialog.Option.DontUseNativeDialog, True)
        dialog.setOption(QtWidgets.QFileDialog.Option.ShowDirsOnly)
        folderPath = dialog.show()"""

        folderPath = QFileDialog.getExistingDirectory(self.window, "Select Directory",
                                                      self.window.dicomHandler.lastLoadFolderDirectory
                                                      )
        if folderPath:
            self.window.dicomHandler.handleFilesFromFolder(folderPath)

    def __openDICOMFile(self) -> None:

        filePath = QFileDialog.getOpenFileName(self.window, 'Open file', "", "DICOM (*.dcm)",
                                               options = QtWidgets.QFileDialog.Option.DontUseNativeDialog)

        if filePath[0] != '':
            self.window.dicomHandler.handleSingleFiles(filePath[0])

    def __retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Files"))

        self.actionOpenDICOMFile.setText(_translate("MainWindow", "Open DICOM file"))
        self.actionOpenDICOMFile.setStatusTip(_translate("MainWindow", "Open a DICOM file"))
        # self.actionOpenDICOMFile.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.actionOpenDICOMFolder.setText(_translate("MainWindow", "Open DICOM folder"))
        self.actionOpenDICOMFolder.setStatusTip(_translate("MainWindow", "Open DICOM folder"))
        # self.actionOpenDICOMFolder.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))

        self.actionRemoveFromView.setText(_translate("MainWindow", "Remove image from view"))
        self.actionRemoveFromView.setStatusTip(_translate("MainWindow", "Remove image from view"))
        # self.actionRemoveFromView.setShortcut(_translate("MainWindow", "§"))

        self.actionRemoveSeries.setText(_translate("MainWindow", "Remove series"))
        self.actionRemoveSeries.setStatusTip(_translate("MainWindow", "Remove series"))
        # self.actionRemoveSeries.setShortcut(_translate("MainWindow", "ì"))
