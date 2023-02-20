from PyQt5 import QtCore, QtGui, QtWidgets
from downloader import download_controller
import threading
import time
import sys
import os

# Class that defines a downloading window
# This allows the user to search, retrieve, and download a manga of their choosing
# Data pertaining to the download is displayed via the Console Output box defined in
# main.py
class Download_Window(QtWidgets.QWidget):
    def setupUi(self, DownloadWindow):
        DownloadWindow.setObjectName("DownloadWindow")
        DownloadWindow.resize(650, 300)
        DownloadWindow.setStyleSheet("background-color: #3E363F;")
        self.centralwidget = QtWidgets.QWidget(DownloadWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 20, 621, 261))
        self.frame.setStyleSheet("QFrame{\n""background-color: #E7DECD;\n""border-radius:15px;\n""}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        # Button to enable searching and downloading of new material
        self.SEARCH = QtWidgets.QPushButton(self.frame)
        self.SEARCH.setGeometry(QtCore.QRect(250, 0, 121, 31))
        self.SEARCH.setStyleSheet("QPushButton {\n""background-color: #d4ccbd;\n""border-radius:10px;\n""font: 63 11pt \"Segoe UI Semibold\";\n"
"}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SEARCH.setIcon(icon)
        self.SEARCH.setIconSize(QtCore.QSize(20, 20))
        self.SEARCH.setObjectName("SEARCH")
        self.SEARCH.clicked.connect(self.get_input)
        # Button to shutdown the main window
        self.CANCEL = QtWidgets.QPushButton(self.frame)
        self.CANCEL.setGeometry(QtCore.QRect(570, 0, 31, 31))
        self.CANCEL.setStyleSheet("QPushButton {\n""background-color: #d4ccbd;\n""border-radius:10px;\n"
"}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CANCEL.setIcon(icon)
        self.CANCEL.setIconSize(QtCore.QSize(28, 28))
        self.CANCEL.setObjectName("QUIT")
        self.CANCEL.clicked.connect(lambda: DownloadWindow.close())
        # This button force terminates the program to stop downloading process
        self.TERMINATE = QtWidgets.QPushButton(self.frame)
        self.TERMINATE.setGeometry(QtCore.QRect(20, 0, 31, 31))
        self.TERMINATE.setStyleSheet("QPushButton {\n""background-color: #d4ccbd;\n""border-radius:10px;\n"
"}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/frown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TERMINATE.setIcon(icon)
        self.TERMINATE.setIconSize(QtCore.QSize(28, 28))
        self.TERMINATE.setObjectName("TERMINATE")
        self.TERMINATE.clicked.connect(self.terminate)

        # This window displays text to the user that is relevant to the downloading process
        self.console_output = QtWidgets.QLabel(self.frame)
        self.console_output.setGeometry(QtCore.QRect(20, 40, 581, 211))
        self.console_output.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n""background-color: #d4ccbd;\n""border-radius:15px;")
        self.console_output.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.console_output.setObjectName("console_output")
        DownloadWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(DownloadWindow)
        QtCore.QMetaObject.connectSlotsByName(DownloadWindow)

    def retranslateUi(self, DownloadWindow):
        _translate = QtCore.QCoreApplication.translate
        DownloadWindow.setWindowTitle(_translate("DownloadWindow", "Mangaroo-Downloader"))
        DownloadWindow.setWindowIcon(QtGui.QIcon("icons/win_icon.png"))
        self.SEARCH.setText(_translate("DownloadWindow", "SEARCH"))
        self.console_output.setText(_translate("DownloadWindow", ""))

    # Search box that takes input and retrieves data for the specified manga
    def get_input(self):
        name, valid = QtWidgets.QInputDialog.getText(self, "DOWNLOAD", "Enter name of Manga:")
        if valid:
            # Runs downloading in multi-thread to allow data to be passed between windows (console log)
            t1 = threading.Thread(target=download_controller, args=(self.console_output, name))
            t1.start()

    # Confirms with user whether or not they want to force quit
    def terminate(self):
        confirm = QtWidgets.QMessageBox()
        confirm.setWindowTitle("Force quit?")
        confirm.setText("Are you sure you want to force quit?")
        confirm.setIcon(QtWidgets.QMessageBox.Warning)
        confirm.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        confirm.buttonClicked.connect(self.confirm_term)
        confirm.exec_()

    # Helper method for confirmation on termination
    def confirm_term(self, btnClicked):
        if btnClicked.text() == "&Yes":
            os._exit(1)