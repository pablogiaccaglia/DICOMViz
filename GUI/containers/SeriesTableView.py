

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableView


class SeriesTableView(QTableView):

    def __init__(self, fatherWidget = None):
        super().__init__(fatherWidget)

        self.__setupUI()

    def __setupUI(self):
        self.__setSizePolicy()

        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setDragDropOverwriteMode(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setShowGrid(False)
        self.setSortingEnabled(True)
        self.setObjectName("SeriesSelection")

        self.__setupHHeader()

        self.__setupVHeader()

        self.__retranslateUI()

    def __setSizePolicy(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)

    def __setupHHeader(self):
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.horizontalHeader().setDefaultSectionSize(30)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setMinimumSectionSize(30)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setStretchLastSection(False)

    def __setupVHeader(self):
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setCascadingSectionResizes(False)
        self.verticalHeader().setHighlightSections(False)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setToolTip(_translate("MainWindow", "List of imported DICOM series"))

    def resizeColumns(self, *args):
        """Resizes columns to contents, setting the last section to stretch."""
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)

