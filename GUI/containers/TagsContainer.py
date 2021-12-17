import re

from PyQt6 import QtGui


class TagsContainer(QtGui.QStandardItemModel):

    def __init__(self, parent):
        QtGui.QStandardItemModel.__init__(self, parent= parent)

    """Container to manage Dicom file's tags in a list"""

    def fillTags(self, dicomFile, columns, regex = None, maxValueSize = 256):

        """Fill the TagContainer with the tags of the dicomFile"""

        self.clear()
        self.setHorizontalHeaderLabels(columns)

        try:
            regex = re.compile(str(regex), re.DOTALL)
        except:
            regex = ""  # no regex or bad pattern

        def _elementToValue(element):

            """ Return the value in the element object. This can be a list of QStandardItem objects
               if element.VR == 'SQ', otherwise it is a string """

            value = None

            if element.VR == "SQ":
                value = []

                for i, item in enumerate(element):
                    anotherParent = QtGui.QStandardItem("%s %i" % (element.name, i))
                    _buildContent(anotherParent, item)

                    if not regex or anotherParent.hasChildren():  # discard sequences whose children have been filtered out
                        value.append(anotherParent)

            elif element.name != "Pixel Data":
                value = str(element.value)

            return value

        def _buildContent(parent, dicomF):

            """ Add every element in the dicom file (dicomF) to the QStandardItem
                parentNode object in a recursive way for all list elements. """

            for element in dicomF:
                value = _elementToValue(element)
                tag = "(%04x, %04x)" % (element.tag.group, element.tag.elem)
                parent1 = QtGui.QStandardItem(str(element.name))
                tagitem = QtGui.QStandardItem(tag)

                if isinstance(value, str):
                    origvalue = value

                    if len(value) > maxValueSize:
                        origvalue = repr(value)
                        value = value[:maxValueSize] + "..."

                    try:
                        value = value.decode("ascii")
                        if "\n" in value or "\r" in value:  # multiline text data should be shown as repr
                            value = repr(value)
                    except:
                        value = repr(value)

                    if not regex or re.search(regex, str(element.name) + tag + value) is not None:
                        item = QtGui.QStandardItem(value)
                        # original value is stored directly or as repr() form for tag value item, used later when copying
                        item.setData(origvalue)

                        parent.appendRow([parent1, tagitem, item])

                elif value is not None and len(value) > 0:
                    parent.appendRow([parent1, tagitem])
                    for v in value:
                        parent1.appendRow(v)

        tagParentNode = QtGui.QStandardItem(
                "Tags")  # create a parent node every tag is a child of, used for copying all tag data
        self.appendRow([tagParentNode])
        _buildContent(tagParentNode, dicomFile)
