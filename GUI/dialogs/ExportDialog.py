from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog


class ExportDialog(QDialog):

    def __init__(self, window):
        super().__init__()

        self.window = window
        self.exportPushButton = QtWidgets.QPushButton(self)
        self.closePushButton = QtWidgets.QPushButton(self)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.currentImageRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.exportButtonGroup = QtWidgets.QButtonGroup(self)
        self.currentSeriesRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.jpegRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.fileFormatButtonGroup = QtWidgets.QButtonGroup(self)
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        self.dicomRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.bmpRadioButton = QtWidgets.QRadioButton(self.groupBox)

    def setupUi(self):

        self.setObjectName("ExportDialog")
        self.setEnabled(True)
        self.resize(640, 220)
        self.setMinimumSize(QtCore.QSize(640, 220))
        self.setMaximumSize(QtCore.QSize(640, 220))
        self.setModal(False)

        self.exportPushButton.setGeometry(QtCore.QRect(430, 180, 101, 31))
        self.exportPushButton.setObjectName("pushButton")

        self.closePushButton.setGeometry(QtCore.QRect(540, 180, 91, 31))
        self.closePushButton.setObjectName("pushButton_2")

        self.groupBox.setGeometry(QtCore.QRect(10, 10, 621, 161))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.label.setGeometry(QtCore.QRect(20, 30, 71, 31))
        self.label.setObjectName("label")

        self.label_2.setGeometry(QtCore.QRect(20, 80, 91, 31))
        self.label_2.setObjectName("label_2")

        self.currentImageRadioButton.setGeometry(QtCore.QRect(130, 30, 121, 31))
        self.currentImageRadioButton.setObjectName("radioButton")

        self.exportButtonGroup.setObjectName("exportButtonGroup")
        self.exportButtonGroup.addButton(self.currentImageRadioButton)

        self.currentSeriesRadioButton.setGeometry(QtCore.QRect(280, 30, 121, 31))
        self.currentSeriesRadioButton.setObjectName("radioButton_2")

        self.exportButtonGroup.addButton(self.currentSeriesRadioButton)

        self.jpegRadioButton.setGeometry(QtCore.QRect(130, 80, 61, 31))
        self.jpegRadioButton.setObjectName("radioButton_3")

        self.fileFormatButtonGroup.setObjectName("fileFormatButtonGroup")
        self.fileFormatButtonGroup.addButton(self.jpegRadioButton)

        self.radioButton_4.setGeometry(QtCore.QRect(280, 80, 61, 31))
        self.radioButton_4.setObjectName("radioButton_4")

        self.fileFormatButtonGroup.addButton(self.radioButton_4)

        self.dicomRadioButton.setGeometry(QtCore.QRect(130, 110, 61, 31))
        self.dicomRadioButton.setObjectName("radioButton_5")
        self.fileFormatButtonGroup.addButton(self.dicomRadioButton)

        self.bmpRadioButton.setGeometry(QtCore.QRect(280, 110, 61, 31))
        self.bmpRadioButton.setObjectName("radioButton_6")
        self.fileFormatButtonGroup.addButton(self.bmpRadioButton)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ExportDialog", "Export images"))
        self.exportPushButton.setText(_translate("ExportDialog", "Export"))
        self.closePushButton.setText(_translate("ExportDialog", "Close"))
        self.label.setText(_translate("ExportDialog",
                                      "<html><head/><body><p><span style=\" font-size:14pt;\">Export</span></p></body></html>"))
        self.label_2.setText(_translate("ExportDialog",
                                        "<html><head/><body><p><span style=\" font-size:14pt;\">File format</span></p></body></html>"))
        self.currentImageRadioButton.setText(_translate("ExportDialog", "Current image"))
        self.currentSeriesRadioButton.setText(_translate("ExportDialog", "Current series"))
        self.jpegRadioButton.setText(_translate("ExportDialog", "JPEG"))
        self.radioButton_4.setText(_translate("ExportDialog", "PNG"))
        self.dicomRadioButton.setText(_translate("ExportDialog", "DICOM"))
        self.bmpRadioButton.setText(_translate("ExportDialog", "BMP"))