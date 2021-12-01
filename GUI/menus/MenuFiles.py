import time

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDialog, QFileDialog

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

        self.actionAddDICOMFile = QtWidgets.QWidgetAction(self.menuBar)
        self.actionAddDICOMFile.setObjectName("actionAddDICOMFile")

        self.actionAddDICOMFolder = QtWidgets.QWidgetAction(self.menuBar)
        self.actionAddDICOMFolder.setObjectName("actionAddDICOMFolder")

        self.actionRemoveFromView = QtWidgets.QWidgetAction(self.menuBar)
        self.actionRemoveFromView.setObjectName("actionRemoveFromView")
        self.actionRemoveFromView.triggered.connect(self.menuBar.window.dicomHandler.removeImageFromView)
        self.toggleActions(False)

    def __addActions(self):
        self.menuADD_DICOM_images.addAction(self.actionAddDICOMFile)
        self.menuADD_DICOM_images.addAction(self.actionAddDICOMFolder)

        self.addAction(self.actionNewWindow)
        self.addAction(self.actionDuplicateWindow)

        self.addSeparator()

        self.addAction(self.actionOpenDICOMFile)
        self.addAction(self.actionOpenDICOMFolder)

        self.addSeparator()

        self.addAction(self.menuADD_DICOM_images.menuAction())
        self.addAction(self.actionRemoveFromView)

    def __openDICOMFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Select Directory",
                                                      self.window.dicomHandler.lastLoadFolderDir)
        if folderPath:
            self.window.handleFilesFromFolder(folderPath)

    def __openDICOMFile(self):
        filePath = QFileDialog.getOpenFileName(self, 'Open file', "", "DICOM (*.dcm)")

        if filePath[0] != '':
            self.window.handleSingleFiles(filePath[0])

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

            self.actionAddDICOMFile.setText(_translate("MainWindow", "Add DICOM file"))
            self.actionAddDICOMFile.setStatusTip(_translate("MainWindow", "Add a new DICOM file"))

            self.actionAddDICOMFolder.setText(_translate("MainWindow", "Add DICOM folder"))
            self.actionAddDICOMFolder.setStatusTip(_translate("MainWindow", "ADD a new DICOM folder"))

            self.actionRemoveFromView.setText(_translate("MainWindow", "Remove image from view"))
            self.actionRemoveFromView.setStatusTip(_translate("ManWindow", "Remove image from view"))
            self.actionRemoveFromView.setShortcut(_translate("MainWindow", "§"))

    def toggleActions(self, value: bool):
            self.actionRemoveFromView.setEnabled(value)