from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableView


class SeriesTableView(QTableView):

    def __init__(self, fatherWidget = None):
        super().__init__(fatherWidget)

        self._setupUI()

    def _setupUI(self):
        self._setSizePolicy()

        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setDragDropOverwriteMode(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setShowGrid(False)
        self.setSortingEnabled(True)
        self.setObjectName("SeriesSelection")

        self._setupHHeader()

        self._setupVHeader()

        self._retranslateUI()

    def _setSizePolicy(self) -> None:
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)

    def _setupHHeader(self) -> None:
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.horizontalHeader().setDefaultSectionSize(30)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setMinimumSectionSize(30)
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setStretchLastSection(False)

    def _setupVHeader(self) -> None:
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setCascadingSectionResizes(False)
        self.verticalHeader().setHighlightSections(False)

    def _retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        self.setToolTip(_translate("MainWindow", "List of imported DICOM series"))

    def resizeColumns(self) -> None:
        """Resizes columns to contents, setting the last section to stretch."""
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)

    def clickRow(self, index: int) -> None:
        self.selectRow(index)
        self.clicked.emit(self.currentIndex())
