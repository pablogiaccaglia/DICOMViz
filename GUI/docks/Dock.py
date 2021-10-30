import os
from typing import List

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QDockWidget


class Dock(QDockWidget):

    def __init__(self, name, window):
        super().__init__(window)
        self.filesListWidget = QtWidgets.QWidget()
        self.dockContents = QtWidgets.QWidget()
        self.dockContents.setObjectName(name)
        self.listView = QtWidgets.QListWidget(self.dockContents)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockContents)
        self.window = window

        self.setMaximumSize(QtCore.QSize(524287, 524287))
        self.setObjectName("dockWidgetOf" + name)
        self.filesListWidget.setObjectName(name)

        self.verticalLayout.setObjectName("verticalLayoutOf" + name)
        self.listView.setObjectName("listViewOf" + name)
        self.verticalLayout.addWidget(self.listView)
        self.setWidget(self.dockContents)

        self.filesList = []
        self._file_name = None

    def loadFiles(self, files: List[str]):

        self.listView.clear()

        self.filesList.clear()
        self.filesList = files

        for fileName in self.filesList:
            item = QtWidgets.QListWidgetItem(os.path.basename(fileName))
            item.setToolTip(fileName)
            self.listView.addItem(item)

        self.listView.setMinimumWidth(self.listView.sizeHintForColumn(0) + 20)

        if self.filesList:
            self.file_name = self.filesList[0]

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        try:
            self._file_name = value
            #   data = DicomData.from_files([self._file_name])
            #    self.pix_label.data = data
            self.window.setWindowTitle("DICOM Visualizer : " + self._file_name)
        except BaseException as exc:
            print(exc)
            #   self.pix_label.data = None
            self.window.setWindowTitle("pydiq: No image")
