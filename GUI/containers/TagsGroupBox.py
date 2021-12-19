from PyQt6 import QtCore, QtWidgets

from DICOM import dicom
from GUI.containers.TagsContainer import TagsContainer


class TagsGroupBox(QtWidgets.QGroupBox):

    def __init__(self, centralWidget, tagsContainer: TagsContainer):
        super().__init__(centralWidget)

        self.setAutoFillBackground(True)
        self.setObjectName("TagGroupBox")
        self._tagsContainer = tagsContainer

        self._gridLayout = QtWidgets.QGridLayout(self)

        self._horizontalLayout = QtWidgets.QHBoxLayout()

        self._label = QtWidgets.QLabel(self)
        self._label.setObjectName("label")

        self._filterEditLine = QtWidgets.QLineEdit(self)
        self._filterEditLine.setObjectName("filterLine")
        self._filterEditLine.textChanged.connect(self.__setRegexFilter)
        self._filterRegex = ""
        self._dicomFile = None

        self._tagsTreeView = QtWidgets.QTreeView(self)

        self.__initTagView()
        self.__initGridLayout()
        self.__initHorizontalLayout()

        self.__retranslateUI()

    def __setRegexFilter(self, regex) -> None:
        """Set the filtering regex to be `regex'."""
        self._filterRegex = regex
        self.fillTagsTree(self._dicomFile)

    @property
    def filterRegex(self) -> str:
        return self._filterRegex

    def fillTagsTree(self, dicomFile) -> None:
        """Refill the Dicom tag view, this will rejig the columns and (unfortunately) reset column sorting."""
        self._dicomFile = dicomFile
        vpos = self._tagsTreeView.verticalScrollBar().value()
        self._tagsContainer.fillTags(self._dicomFile.getDicomFile(), dicom.tagTreeColumns, self._filterRegex)
        self._tagsTreeView.expandAll()
        self._tagsTreeView.resizeColumnToContents(0)
        self._tagsTreeView.verticalScrollBar().setValue(vpos)

    def __initHorizontalLayout(self) -> None:
        self._horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self._horizontalLayout.setObjectName("_horizontalLayout")
        self._horizontalLayout.addWidget(self._label)
        self._horizontalLayout.addWidget(self._filterEditLine)

    def __initTagView(self) -> None:
        self._tagsTreeView.setModel(self._tagsContainer)
        self._tagsTreeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self._tagsTreeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._tagsTreeView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self._tagsTreeView.setProperty("showDropIndicator", False)
        self._tagsTreeView.setDragDropOverwriteMode(False)
        self._tagsTreeView.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self._tagsTreeView.setTextElideMode(QtCore.Qt.TextElideMode.ElideNone)
        self._tagsTreeView.setIndentation(10)
        self._tagsTreeView.setSortingEnabled(True)
        self._tagsTreeView.setObjectName("tagsTreeView")

    def __initGridLayout(self) -> None:
        self._gridLayout.setObjectName("gridLayout")
        self._gridLayout.addLayout(self._horizontalLayout, 0, 0, 1, 1)
        self._gridLayout.addWidget(self._tagsTreeView, 1, 0, 1, 1)

    def __retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "DICOM Tags"))
        self._label.setText(_translate("MainWindow", "Filter:"))
        self._filterEditLine.setToolTip(
            _translate("MainWindow", "Filter DICOM tags by name, ID, or content, using regular expressions, "))
        self._tagsTreeView.setToolTip(_translate("MainWindow", "List of DICOM tags"))
