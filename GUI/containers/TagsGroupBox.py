from PyQt6 import QtCore, QtWidgets


class TagsGroupBox(QtWidgets.QGroupBox):

    def __init__(self, centralWidget):

        super().__init__(centralWidget)

        self.setAutoFillBackground(True)
        self.setObjectName("TagGroupBox")

        self.gridLayout = QtWidgets.QGridLayout(self)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")

        self.filterLine = QtWidgets.QLineEdit(self)
        self.filterLine.setObjectName("filterLine")

        self.tagView = QtWidgets.QTreeView(self)

        self.__initGridLayout()
        self.__initHorizontalLayout()

        self.__retranslateUI()

    def __initHorizontalLayout(self):
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.filterLine)

    def __initTagView(self):
        self.tagView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tagView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tagView.setProperty("showDropIndicator", False)
        self.tagView.setDragDropOverwriteMode(False)
        self.tagView.setAlternatingRowColors(True)
        self.tagView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tagView.setTextElideMode(QtCore.Qt.TextElideMode.ElideNone)
        self.tagView.setIndentation(10)
        self.tagView.setSortingEnabled(True)
        self.tagView.setObjectName("tagView")

    def __initGridLayout(self):
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.tagView, 1, 0, 1, 1)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "DICOM Tags"))
        self.label.setText(_translate("MainWindow", "Filter:"))
        self.filterLine.setToolTip(_translate("MainWindow", "Filter DICOM tags by name, ID, or content, using regular expressions, "))
        self.tagView.setToolTip(_translate("MainWindow", "List of DICOM tags"))