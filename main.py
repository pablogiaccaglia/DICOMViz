import signal
import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication

from GUI.GUIMainWindow import GUIMainWindow


def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QApplication.quit()


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

    signal.signal(signal.SIGINT, sigint_handler)

    timer = QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

    sys.exit(app.exec())
