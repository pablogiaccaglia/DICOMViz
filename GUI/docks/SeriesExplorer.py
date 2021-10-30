import re
from operator import itemgetter

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QModelIndex

from DICOM.dicom import keywordNameMap
from GUI.docks.Dock import Dock


class SeriesExplorer(Dock, QtCore.QAbstractTableModel):
    """This manages the list of series inside a Dock, displaying useful information and providing minimal sorting features."""

    def __init__(self, seriesColumns, name, window):
        Dock.__init__(self, name, window)
        QtCore.QAbstractTableModel.__init__(self, window)
        self.seriesTable = []
        self.seriesColumns = seriesColumns
        self.sortingColumn = 0
        self.sortingOrder = QtCore.Qt.SortOrder.AscendingOrder

    def rowCount(self, parent = None, *args, **kwargs):
        return len(self.seriesTable)

    def columnCount(self, parent = None, *args, **kwargs):
        return len(self.seriesTable[0]) if self.seriesTable else 0

    def sort(self, sortingColumn: int, sortingOrder: Qt.SortOrder = Qt.SortOrder.AscendingOrder, *args, **kwargs):

        self.sortingOrder = sortingOrder
        self.sortingColumn = sortingColumn
        self.layoutAboutToBeChanged.emit()
        self.seriesTable.sort(key = itemgetter(sortingColumn),
                              reverse = sortingOrder == QtCore.Qt.SortOrder.DescendingOrder)
        self.layoutChanged.emit()

    def updateContent(self, seriesTable):
        self.seriesTable = list(seriesTable)
        self.sort(self.sortingColumn, self.sortingOrder)  # sort using existing parameters

    def getRow(self, i):
        return self.seriesTable[i]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return keywordNameMap[self.seriesColumns[section]]

    def data(self, modelIndex: QModelIndex, displayRole: int = Qt.ItemDataRole.DisplayRole):
        if modelIndex.isValid() and displayRole == Qt.ItemDataRole.DisplayRole:
            return str(self.seriesTable[modelIndex.row()][modelIndex.column()])
