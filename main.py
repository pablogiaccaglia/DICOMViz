import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from GUI.GUIMainWindow import GUIMainWindow
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)  # in OSX, forces menubar to be in window

    # setup stylesheet
    apply_stylesheet(app, theme = 'dark_teal.xml')

    MainWindow = QtWidgets.QMainWindow()
    ui = GUIMainWindow()
    ui.start()
    sys.exit(app.exec())

