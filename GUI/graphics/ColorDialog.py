from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, pyqtSignal


class ColorAction(QtGui.QAction):

    colorChangedSignal = pyqtSignal(object)

    def __init__(self, name: str, fatherWidget, color = None):
        super(ColorAction, self).__init__(text = name, parent = fatherWidget)

        self._color = None
        self._default = color
        self.triggered.connect(self.onColorPicker)
        self.fatherWidget = fatherWidget
        self.dialog = QtWidgets.QColorDialog(self.fatherWidget)

        self.dialog.currentColorChanged.connect(self.currentColorC)

        # Set the initial/default state.
        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChangedSignal.emit(color)

    @property
    def color(self):
        return self._color

    def onColorPicker(self):

        if self._color:
            self.dialog.setCurrentColor(QtGui.QColor(self._color))

        if self.dialog.show():
            self.setColor(self.dialog.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.setColor(self._default)

        return super(ColorAction, self).mousePressEvent(e)

    def currentColorC(self):
        self.colorChangedSignal.emit(self._color)
        self.setColor(self.dialog.currentColor().name())


