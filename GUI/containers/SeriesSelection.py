from collections import OrderedDict
from operator import itemgetter

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt

from DICOM import dicom


class SeriesSelection(QtCore.QAbstractTableModel):

    def __init__(self, columnNames, fatherWidget = None):
        super().__init__(fatherWidget)

        self.seriesEntries = OrderedDict()
        self.table = []
        self.columnNames = columnNames
        self.currentSelectedRow = -1
        self.columnToSort = 0
        self.sortingOrder = Qt.SortOrder.AscendingOrder

    def rowCount(self, parent = None):
        return len(self.table)

    def columnCount(self, parent = None):
        if self.table:
            return len(self.table[0])
        return 0

    def sort(self, columnToSort, sortingOrder = None):

        if not sortingOrder:
            sortingOrder = Qt.SortOrder.AscendingOrder

        self.layoutAboutToBeChanged.emit()
        self.columnToSort = columnToSort
        self.sortingOrder = sortingOrder

        self.table.sort(key = itemgetter(columnToSort), reverse = (sortingOrder == Qt.SortOrder.DescendingOrder))
        self.layoutChanged.emit()

    def updateTable(self, seriesEntries):
        self.table = self.table + list(seriesEntries)
        self.sort(self.columnToSort, self.sortingOrder)

    def getRowContent(self, index):
        try:
            return self.series[index]
        except IndexError:
            return None

    def headerData(self, section, orientation, role = None):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return dicom.keywordNameMap[self.columnNames[section]]

    def data(self, index, role = None):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self.table[index.row()][index.column()])
