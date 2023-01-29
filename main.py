from PyQt5 import QtCore, QtGui, QtWidgets
import reader, downloader
import sys
import os

PARENTFOLDER = "Material"


class Ui_menu(QtWidgets.QMainWindow):
    def setupUi(self, menu):
        self.menu = menu
        self.menu.setObjectName("menu")
        self.menu.resize(800, 600)
        self.menu.setStyleSheet("background-color: #3E363F;")
        self.btn_group = QtWidgets.QButtonGroup()
        self.btn_group.setExclusive(False)

        self.selected_manga = ""
        self.selected_manga_name = ""
        self.cont = False

        self.centralwidget = QtWidgets.QWidget(self.menu)
        self.centralwidget.setObjectName("centralwidget")
        self.list_container = QtWidgets.QWidget(self.centralwidget)
        self.list_container.setGeometry(QtCore.QRect(400, 20, 381, 561))
        self.list_container.setStyleSheet("background-color: #E7DECD;")
        self.list_container.setObjectName("list_container")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.list_container)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.list_scrollzone = QtWidgets.QScrollArea(self.list_container)
        self.list_scrollzone.setMinimumSize(QtCore.QSize(0, 0))
        self.list_scrollzone.setWidgetResizable(True)
        self.list_scrollzone.setObjectName("list_scrollzone")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 346, 800))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.list_scrollzone.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.list_scrollzone)

        self.QUIT = QtWidgets.QPushButton(self.centralwidget)
        self.QUIT.setGeometry(QtCore.QRect(20, 550, 41, 31))
        self.QUIT.setStyleSheet("QPushButton {\n""background-color: #E7DECD;\n""border-radius:10px;\n""}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
        quit_ico = QtGui.QIcon()
        quit_ico.addPixmap(QtGui.QPixmap("icons/quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QUIT.setIcon(quit_ico)
        self.QUIT.setIconSize(QtCore.QSize(28, 28))
        self.QUIT.setObjectName("QUIT")
        self.QUIT.clicked.connect(self.quit)

        self.tbn_container = QtWidgets.QWidget(self.centralwidget)
        self.tbn_container.setGeometry(QtCore.QRect(20, 20, 331, 481))
        self.tbn_container.setStyleSheet("background-color: #E7DECD;\n""border-radius:15px;")
        self.tbn_container.setObjectName("tbn_container")
        self.thumbnail = QtWidgets.QLabel(self.tbn_container)
        self.thumbnail.setGeometry(QtCore.QRect(50, 10, 231, 271))
        self.thumbnail.setStyleSheet("")
        self.thumbnail.setObjectName("thumbnail")
        self.thumbnail.setScaledContents(True)
        self.description = QtWidgets.QLabel(self.tbn_container)
        self.description.setGeometry(QtCore.QRect(40, 290, 251, 81))
        self.description.setStyleSheet("font: 63 12pt \"Segoe UI Semibold\";")
        self.description.setObjectName("description")
        self.description.setAlignment(QtCore.Qt.AlignCenter)

        self.open = QtWidgets.QPushButton(self.tbn_container)
        self.open.setGeometry(QtCore.QRect(10, 430, 141, 41))
        self.open.setStyleSheet("QPushButton {\n""background-color: rgb(109, 109, 163);\n""border-radius:10px;\n""font: 63 11pt \"Myriad Pro Light\";\n""}\n""\n""QPushButton:hover {\n""background-color: rgb(99, 99, 148);\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(68, 68, 103);\n""}")
        self.open.setIconSize(QtCore.QSize(28, 28))
        self.open.setObjectName("open")
        self.open.clicked.connect(self.start_reader)

        self.download = QtWidgets.QPushButton(self.tbn_container)
        self.download.setGeometry(QtCore.QRect(270, 430, 51, 41))
        self.download.setStyleSheet("QPushButton {\n""background-color: rgb(109, 109, 163);\n""border-radius:10px;\n""}\n""\n""QPushButton:hover {\n""background-color: rgb(99, 99, 148);\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(68, 68, 103);\n""}")
        download_ico = QtGui.QIcon()
        download_ico.addPixmap(QtGui.QPixmap("icons/download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.download.setIcon(download_ico)
        self.download.setIconSize(QtCore.QSize(28, 28))
        self.download.setObjectName("download")

        self.delete_btn = QtWidgets.QPushButton(self.tbn_container)
        self.delete_btn.setGeometry(QtCore.QRect(200, 430, 51, 41))
        self.delete_btn.setStyleSheet("QPushButton {\n""background-color: rgb(109, 109, 163);\n""border-radius:10px;\n""}\n""\n""QPushButton:hover {\n""background-color: rgb(99, 99, 148);\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(68, 68, 103);\n""}")
        del_ico = QtGui.QIcon()
        del_ico.addPixmap(QtGui.QPixmap("icons/del.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(del_ico)
        self.delete_btn.setIconSize(QtCore.QSize(28, 28))
        self.delete_btn.setObjectName("delete_btn")

        self.menu.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        self.btn_group.buttonClicked.connect(self.select_manga)
        QtCore.QMetaObject.connectSlotsByName(self.menu)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.menu.setWindowTitle(_translate("menu", "MainWindow"))
        self.description.setText(_translate("menu", ""))
        self.open.setText(_translate("menu", "OPEN"))
        self.list_available()

    def list_available(self):
        manga_in_folder = os.listdir(PARENTFOLDER)
        total_scroll_height = len(manga_in_folder) * 40
        if total_scroll_height > 561:
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 346, total_scroll_height))
            self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, total_scroll_height))
        curr_height = 10
        btn_counter = 0
        for manga in manga_in_folder:
            button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            button.setGeometry(QtCore.QRect(10, 10, 311, 16))
            button.setStyleSheet("QPushButton {\n""background-color: #d4ccbd;\n""border-radius:10px;\nfont: 63 12pt \"Segoe UI Semibold\";\n""}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
            button.setText(manga)
            button.setGeometry(QtCore.QRect(10, curr_height, 356, 30))
            id = btn_counter
            self.btn_group.addButton(button, id)
            btn_counter += 1
            curr_height += 40

    def select_manga(self, btn):
        chosen = os.listdir(PARENTFOLDER)[self.btn_group.id(btn)]
        self.selected_manga = PARENTFOLDER + "/" + chosen
        self.selected_manga_name = chosen
        self.thumbnail.setPixmap(QtGui.QPixmap(self.selected_manga + "/thumbnail.jpg"))
        num = 0
        link = ""
        with open(self.selected_manga+"/data.txt", "r") as writer:
            num = int(writer.readline().split("\n")[0])
        self.description.setText(chosen + "\n\nTotal Chapters: " + str(len(os.listdir(self.selected_manga)) - 2) + "\nBookmarked Chapter: " + str(num+1))

    def quit(self):
        self.menu.close()
    def start_reader(self):
        self.cont = True
        self.menu.close()
        

def run_instances():
    app = QtWidgets.QApplication(sys.argv)
    menu = QtWidgets.QMainWindow()
    ui = Ui_menu()
    ui.setupUi(menu)
    menu.show()
    app.exec_()
    return ui.selected_manga, ui.selected_manga_name, ui.cont

def main():
    while True:
        sel_path, sel_name, cont = run_instances()
        if cont:
            reader.control_loop(sel_path, sel_name)
        else:
            sys.exit()

main()