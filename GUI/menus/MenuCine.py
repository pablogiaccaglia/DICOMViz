from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMenu


class MenuCine(QMenu):

    def __init__(self, menuBar):
        super().__init__(menuBar)
        self.menuBar = menuBar
        self.setObjectName("menuCine")

        self.__defineActions()
        self.__addActions()
        self.__retranslateUI()

    def __defineActions(self):
        self.actionAnimateSeries = QtWidgets.QWidgetAction(self.menuBar)
        self.actionAnimateSeries.setObjectName("actionAnimateSeries")
        self.actionAnimateSeries.triggered.connect(self.__addGifHandlerToGraphicsView)

    def __addActions(self):
        self.addAction(self.actionAnimateSeries)

    def __retranslateUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", "Cine"))

        self.actionAnimateSeries.setText(_translate("MainWindow", "Animate"))
        self.actionAnimateSeries.setStatusTip(_translate("MainWindow", "Animate series"))
        self.actionAnimateSeries.setShortcut(_translate("MainWindow", "Ctrl+'"))

    def __addGifHandlerToGraphicsView(self):
        self.menuBar.window.graphicsView.addGifHandler()