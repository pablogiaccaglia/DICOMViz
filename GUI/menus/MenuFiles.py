import time

import qdarktheme
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QFileDialog

from DICOM.DicomSeries import DicomSeries
from GUI.menus.AbstractMenu import AbstractMenu


class MenuFiles(AbstractMenu, QDialog):

    def __init__(self, menuBar):

        super().__init__(menuBar, "menuFiles")
        self.setToolTip("")
        self.window = menuBar.window

        # nested menu
        self.menuADD_DICOM_images = QtWidgets.QMenu(self)
        self.menuADD_DICOM_images.setObjectName("menuADD_DICOM_images")

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    #  self.setStyleSheet(qdarktheme.load_stylesheet())

    def __defineActions(self):
        self.actionNewWindow = QtWidgets.QWidgetAction(self.menuBar)
        self.actionNewWindow.setShortcutVisibleInContextMenu(True)
        self.actionNewWindow.setObjectName("actionNewWindow")

        self.actionDuplicateWindow = QtWidgets.QWidgetAction(self.menuBar)
        self.actionDuplicateWindow.setObjectName("actionDuplicateWindow")

        self.actionOpenDICOMFile = QtWidgets.QWidgetAction(self.menuBar)
        self.actionOpenDICOMFile.setObjectName("actionOpenDICOMFile")
        self.actionOpenDICOMFile.triggered.connect(self.__openDICOMFile)

        self.actionOpenDICOMFolder = QtWidgets.QWidgetAction(self.menuBar)
        self.actionOpenDICOMFolder.setObjectName("actionOpenDICOMFolder")
        self.actionOpenDICOMFolder.triggered.connect(self.__openDICOMFolder)

        #  self.actionAddDICOMFile = QtWidgets.QWidgetAction(self.menuBar)
        #  self.actionAddDICOMFile.setObjectName("actionAddDICOMFile")

        #  self.actionAddDICOMFolder = QtWidgets.QWidgetAction(self.menuBar)
        #  self.actionAddDICOMFolder.setObjectName("actionAddDICOMFolder")

        self.actionRemoveFromView = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRemoveFromView.setObjectName("actionRemoveFromView")
        self.actionRemoveFromView.triggered.connect(self.menuBar.window.dicomHandler.removeImageFromView)

        self.actionRemoveSeries = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRemoveSeries.setObjectName("actionRemoveSeries")
        self.actionRemoveSeries.triggered.connect(self.menuBar.window.dicomHandler.removeSeries)

        self.toggleActions(False)

    def __addActions(self):
        self.addSeparator()

        self.addAction(self.actionOpenDICOMFile)
        self.addAction(self.actionOpenDICOMFolder)

        self.addSeparator()

        self.addAction(self.actionRemoveFromView)
        self.addAction(self.actionRemoveSeries)

    def __openDICOMFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self.window, "Select Directory",
                                                      self.window.dicomHandler.lastLoadFolderDir,
                                                      options = QtWidgets.QFileDialog.Option.DontUseNativeDialog)
        if folderPath:
            self.window.dicomHandler.handleFilesFromFolder(folderPath)

    def __openDICOMFile(self):

        filePath = QFileDialog.getOpenFileName(self.window, 'Open file', "", "DICOM (*.dcm)",
                                               options = QtWidgets.QFileDialog.Option.DontUseNativeDialog)

        if filePath[0] != '':
            self.window.dicomHandler.handleSingleFiles(filePath[0])

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate

        self.setTitle(_translate("MainWindow", "Files"))
        self.menuADD_DICOM_images.setTitle(_translate("MainWindow", "ADD DICOM images"))

        self.actionNewWindow.setText(_translate("MainWindow", "New window"))
        self.actionNewWindow.setStatusTip(_translate("MainWindow", "Open new window"))
        self.actionNewWindow.setShortcut(_translate("MainWindow", "Ctrl+V"))

        self.actionDuplicateWindow.setText(_translate("MainWindow", "Duplicate window"))
        self.actionDuplicateWindow.setStatusTip(_translate("MainWindow", "Duplicate the current window"))
        self.actionDuplicateWindow.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))

        self.actionOpenDICOMFile.setText(_translate("MainWindow", "Open DICOM file"))
        self.actionOpenDICOMFile.setStatusTip(_translate("MainWindow", "Open a DICOM file"))
        self.actionOpenDICOMFile.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.actionOpenDICOMFolder.setText(_translate("MainWindow", "Open DICOM folder"))
        self.actionOpenDICOMFolder.setStatusTip(_translate("MainWindow", "Open DICOM folder"))
        self.actionOpenDICOMFolder.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))

        self.actionRemoveFromView.setText(_translate("MainWindow", "Remove image from view"))
        self.actionRemoveFromView.setStatusTip(_translate("MainWindow", "Remove image from view"))
        self.actionRemoveFromView.setShortcut(_translate("MainWindow", "§"))

        self.actionRemoveSeries.setText(_translate("MainWindow", "Remove series"))
        self.actionRemoveSeries.setStatusTip(_translate("MainWindow", "Remove series"))
        self.actionRemoveSeries.setShortcut(_translate("MainWindow", "ì"))

    def toggleActions(self, value: bool, dicomContainer = None):

        self.actionRemoveFromView.setEnabled(value)

        if isinstance(dicomContainer, DicomSeries) or not value:
            self.toggleActionRemoveSeries(value)

    def toggleActionRemoveSeries(self, value: bool):
        self.actionRemoveSeries.setEnabled(value)

    def toggleFilesActions(self, value: bool):
        self.actionOpenDICOMFile.setEnabled(value)
        self.actionOpenDICOMFolder.setEnabled(value)
        self.menuADD_DICOM_images.setEnabled(value)
