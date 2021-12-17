from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QAbstractItemView

from DICOM import dicom
from GUI.containers.TagsContainer import TagsContainer


class TagsGroupBox(QtWidgets.QGroupBox):

    def __init__(self, centralWidget, tagsContainer: TagsContainer):
        super().__init__(centralWidget)

        self.setAutoFillBackground(True)
        self.setObjectName("TagGroupBox")
        self.tagsContainer = tagsContainer

        self.gridLayout = QtWidgets.QGridLayout(self)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")

        self.filterEditLine = QtWidgets.QLineEdit(self)
        self.filterEditLine.setObjectName("filterLine")
        self.filterEditLine.textChanged.connect(self.__setRegexFilter)
        self.filterRegex = ""
        self.dicomFile = None

        self.tagsTreeView = QtWidgets.QTreeView(self)

        self.__initTagView()
        self.__initGridLayout()
        self.__initHorizontalLayout()

        self.__retranslateUI()

    def __setRegexFilter(self, regex):
        """Set the filtering regex to be `regex'."""
        self.filterRegex = regex
        self.fillTagsTree(self.dicomFile)

    def fillTagsTree(self, dicomFile):
        """Refill the Dicom tag view, this will rejig the columns and (unfortunately) reset column sorting."""
        self.dicomFile = dicomFile
        vpos = self.tagsTreeView.verticalScrollBar().value()
        self.tagsContainer.fillTags(self.dicomFile.getDicomFile(), dicom.tagTreeColumns, self.filterRegex)
        self.tagsTreeView.expandAll()
        self.tagsTreeView.resizeColumnToContents(0)
        self.tagsTreeView.verticalScrollBar().setValue(vpos)

    def __initHorizontalLayout(self):
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.filterEditLine)

    def __initTagView(self):
        self.tagsTreeView.setModel(self.tagsContainer)
        self.tagsTreeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tagsTreeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tagsTreeView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tagsTreeView.setProperty("showDropIndicator", False)
        self.tagsTreeView.setDragDropOverwriteMode(False)
        self.tagsTreeView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.tagsTreeView.setTextElideMode(QtCore.Qt.TextElideMode.ElideNone)
        self.tagsTreeView.setIndentation(10)
        self.tagsTreeView.setSortingEnabled(True)
        self.tagsTreeView.setObjectName("tagsTreeView")

    def __initGridLayout(self):
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.tagsTreeView, 1, 0, 1, 1)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "DICOM Tags"))
        self.label.setText(_translate("MainWindow", "Filter:"))
        self.filterEditLine.setToolTip(
            _translate("MainWindow", "Filter DICOM tags by name, ID, or content, using regular expressions, "))
        self.tagsTreeView.setToolTip(_translate("MainWindow", "List of DICOM tags"))
