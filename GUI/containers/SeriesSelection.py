from operator import itemgetter
from typing import Optional

from PyQt6 import QtCore
from PyQt6.QtCore import Qt

from DICOM import dicom


class SeriesSelection(QtCore.QAbstractTableModel):

    def __init__(self, columnNames, fatherWidget = None):
        super().__init__(fatherWidget)

        self._table = []
        self._columnNames = columnNames
        self._currentSelectedRowIndex = -1
        self._columnToSort = 0
        self._sortingOrder = Qt.SortOrder.AscendingOrder

    @property
    def currentSelectedRowIndex(self) -> int:
        return self._currentSelectedRowIndex

    @currentSelectedRowIndex.setter
    def currentSelectedRowIndex(self, index) -> None:
        if index >= 0:
            self._currentSelectedRowIndex = index

    def rowCount(self, parent = None) -> int:
        return len(self._table)

    def columnCount(self, parent = None) -> int:
        if self._table:
            return len(self._table[0])
        return 0

    def sort(self, columnToSort, sortingOrder = None) -> None:

        if not sortingOrder:
            sortingOrder = Qt.SortOrder.AscendingOrder

        self.layoutAboutToBeChanged.emit()
        self._columnToSort = columnToSort
        self._sortingOrder = sortingOrder

        self._table.sort(key = itemgetter(columnToSort), reverse = (sortingOrder == Qt.SortOrder.DescendingOrder))
        self.layoutChanged.emit()

    def updateTable(self, seriesEntries) -> None:
        self._table = self._table + list(seriesEntries)
        self.sort(self._columnToSort, self._sortingOrder)

    def getRowContent(self, index) -> Optional[str]:
        try:
            return self._table[index]
        except IndexError:
            return None

    def headerData(self, section, orientation, role = None) -> Optional[str]:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return dicom.keywordNameMap[self._columnNames[section]]

    def data(self, index, role = None) -> Optional[str]:
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._table[index.row()][index.column()])

    def removeRow(self, index, parent = None) -> tuple:
        self.beginRemoveRows(QtCore.QModelIndex(), self.rowCount() - 1, self.rowCount() - 1)
        rowContent = self._table.pop(index)
        self.endRemoveRows()
        return rowContent
