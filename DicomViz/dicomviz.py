import signal
import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QFileInfo
from PyQt6.QtCore import Qt, QTimer, qInstallMessageHandler
from PyQt6.QtWidgets import QApplication
from multiprocessing import freeze_support
from DicomViz.GUI import windowSingleton


def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QApplication.quit()


# suppress warnings
def handler(msg_type, msg_log_context, msg_string):
    pass


qInstallMessageHandler(handler)


def excepthook(exc_type, exc_value, exc_tb):
    # really bad trick to ignore exception raised by modules which have been monkey patched. Do not emulate :(
    pass

def main(args=[], app=None):

    if app is None:
        app = QtWidgets.QApplication(args)
        app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)  # in OSX, forces menubar to be in window

        app.setApplicationName("DICOM Visualizer")
        app.setOrganizationName("Pablo Giaccaglia")
        app.setDesktopFileName("DICOM Visualizer")
        app.setStyle("Plastique")

        # setup stylesheet
        app.setAttribute(Qt.ApplicationAttribute.AA_Use96Dpi)

        # set icon
        root = QFileInfo(__file__).absolutePath()
        icon = QtGui.QIcon(root + "/dicomviz-logo.png")
        app.setWindowIcon(icon)

        windowSingleton.buildMainWindowSingleton()
        windowSingleton.mainWindow.start()

        signal.signal(signal.SIGINT, sigint_handler)

        timer = QTimer()
        timer.start(500)  # You may change this if you wish.
        timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

        sys.excepthook = excepthook

    if app is None:
        return 1
    else:
        sys.exit(app.exec())

def mainargv():
    """setuptools compatible entry point."""
    freeze_support()
    sys.exit(main(sys.argv))


if __name__ == "__main__":
    main(sys.argv)
