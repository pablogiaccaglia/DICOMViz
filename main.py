import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from GUI.GUIMainWindow import GUIMainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)  # in OSX, forces menubar to be in window

    app.setApplicationName("DICOM Visualizer")
    app.setOrganizationName("Pablo Giaccaglia")
    app.setDesktopFileName("DICOM Visualizer")

    # setup stylesheet
    # apply_stylesheet(app, theme = 'dark_teal.xml')

    # MainWindow = QtWidgets.QMainWindow()
    ui = GUIMainWindow()
    ui.start()
    sys.exit(app.exec())

