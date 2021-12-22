from functools import partial

from PyQt6 import QtCore, QtWidgets
from ...DICOM.DicomAbstractContainer import ViewMode
from ..menus.AbstractMenu import AbstractMenu


class MenuAlterations(AbstractMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar, "menuAlterations")

        self.window = menuBar.window

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

        self.viewModeMenuOptions = self.ViewModeMenuOptions(self)
        self.selectedViewModeMenuOption = self.viewModeMenuOptions.ORIGINAL
        self.disableOptions()
        self.__connectActions()

    class ViewModeMenuOptions:

        def __init__(self, menuAlterations):
            self.ORIGINAL = menuAlterations.actionDefaultView
            self.LUNGS_MASK = menuAlterations.actionLungsMask
            self.SEGMENTED_LUNGS = menuAlterations.actionSegmentedLungsMask

    def disableOptions(self) -> None:
        self.actionDefaultView.setEnabled(False)
        self.actionLungsMask.setEnabled(False)
        self.actionSegmentedLungsMask.setEnabled(False)
        self.actionNegative.setEnabled(False)

    def toggleActions(self, value: bool, dicomContainer = None) -> None:
        self.actionLungsMask.setEnabled(value)
        self.actionSegmentedLungsMask.setEnabled(value)

    def enableNegativeImageAction(self) -> None:
        self.actionNegative.setEnabled(True)

    def __selectViewModeMenuOption(self, viewModeOption, viewMode: ViewMode) -> None:
        self.enableNegativeImageAction()
        self.selectedViewModeMenuOption.setEnabled(True)
        self.selectedViewModeMenuOption = viewModeOption
        self.selectedViewModeMenuOption.setDisabled(True)
        self.window.changeViewMode(viewMode)

    def __defineActions(self) -> None:
        self.actionDefaultView = QtWidgets.QWidgetAction(self.menuBar)
        self.actionDefaultView.setObjectName("actionDefaultView")

        self.actionLungsMask = QtWidgets.QWidgetAction(self.menuBar)
        self.actionLungsMask.setObjectName("actionLungsMask")

        self.actionSegmentedLungsMask = QtWidgets.QWidgetAction(self.menuBar)
        self.actionSegmentedLungsMask.setObjectName("actionSegmentedLungs")

        self.actionNegative = QtWidgets.QWidgetAction(self.menuBar)
        self.actionNegative.setObjectName("actionNegative")

    def __connectActions(self) -> None:
        self.actionDefaultView.triggered.connect(
                partial(self.__selectViewModeMenuOption, self.viewModeMenuOptions.ORIGINAL,
                        ViewMode.ORIGINAL))

        self.actionLungsMask.triggered.connect(
                partial(self.__selectViewModeMenuOption, self.viewModeMenuOptions.LUNGS_MASK,
                        ViewMode.LUNGS_MASK))

        self.actionSegmentedLungsMask.triggered.connect(
                partial(self.__selectViewModeMenuOption, self.viewModeMenuOptions.SEGMENTED_LUNGS,
                        ViewMode.SEGMENTED_LUNGS))

        self.actionNegative.triggered.connect(
                partial(self.window.changeViewMode, ViewMode.NEGATIVE))

    def __addActions(self) -> None:
        self.addAction(self.actionDefaultView)
        self.addAction(self.actionNegative)
        self.addAction(self.actionLungsMask)
        self.addAction(self.actionSegmentedLungsMask)

    def __retranslateUI(self) -> None:
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "Alterations"))

        self.actionLungsMask.setText(_translate("MainWindow", "Lungs Mask"))
        self.actionLungsMask.setStatusTip(_translate("MainWindow", "Lungs Mask"))
        # self.actionLungsMask.setShortcut(_translate("MainWindow", "-"))

        self.actionDefaultView.setText(_translate("MainWindow", "Default View"))
        self.actionDefaultView.setStatusTip(_translate("MainWindow", "DefaultView"))
        # self.actionDefaultView.setShortcut(_translate("MainWindow", "+"))

        self.actionNegative.setText(_translate("MainWindow", "Negative"))
        self.actionNegative.setStatusTip(_translate("MainWindow", "Negative Image"))
        # self.actionNegative.setShortcut(_translate("MainWindow", "N"))

        self.actionSegmentedLungsMask.setText(_translate("MainWindow", "Segmented Lungs Mask"))
        self.actionSegmentedLungsMask.setStatusTip(_translate("MainWindow", "Segmented Lungs Mask"))
        # self.actionSegmentedLungsMask.setShortcut(_translate("MainWindow", "/"))
