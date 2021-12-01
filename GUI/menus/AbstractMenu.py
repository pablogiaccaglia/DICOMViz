from PyQt6.QtWidgets import QMenu


class AbstractMenu(QMenu):

    def __init__(self, menuBar, name):
        super().__init__()
        self.menuBar = menuBar
        self.setObjectName(name)

    def toggleActions(self, value: bool):
        pass