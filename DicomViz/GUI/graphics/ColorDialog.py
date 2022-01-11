from functools import partial

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal


class ColorDialogAction(QtGui.QAction):

    colorChangedSignal = pyqtSignal(object)
    dialogCancelClickedSignal = pyqtSignal(object)
    dialogOkClickedSignal = pyqtSignal(object)

    def __init__(self, name: str, fatherWidget, color = None):
        super(ColorDialogAction, self).__init__(text = name, parent = fatherWidget)

        self._color = None
        self._default = color
        self.triggered.connect(self._onColorPicker)
        self._fatherWidget = fatherWidget
        self._colorDialog = QtWidgets.QColorDialog(self._fatherWidget)
        self._colorDialog.currentColorChanged.connect(self._currentColorChanged)
        self._colorDialog.rejected.connect(partial(lambda: self.dialogCancelClickedSignal.emit))
        self._colorDialog.accepted.connect(partial(lambda: self.dialogOkClickedSignal.emit))
        # Set the initial/default state.
        self._color = self._default

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color) -> None:
        if color != self._color:
            self._color = color
            self.colorChangedSignal.emit(color)

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.MouseButton.RightButton:
            self._color = self._default

        return self._colorDialog.mousePressEvent(e)

    def _currentColorChanged(self) -> None:
        self._color = self._colorDialog.currentColor().name()
        self.colorChangedSignal.emit(self._color)

    def _onColorPicker(self) -> None:

        if self._color:
            self._colorDialog.setCurrentColor(QtGui.QColor(self._color))

        if self._colorDialog.show():
            self._color = self._colorDialog.currentColor().name()


