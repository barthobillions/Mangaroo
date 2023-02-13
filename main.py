from downloader_ui import Download_Window
from PyQt5 import QtCore, QtGui, QtWidgets
from reader import control_loop, update_manga
import shutil
import sys
import os

PARENTFOLDER = "Material"

# This class defines a Menu Screen GUI that allows the user to download, delete, browse, and read material.
class MenuScreen(QtWidgets.QMainWindow):
    def setupUi(self, menu):
        self.menu = menu
        self.menu.setObjectName("menu")
        self.menu.resize(800, 600)
        self.menu.setStyleSheet("background-color: #3E363F;")
        self.btn_group = QtWidgets.QButtonGroup()
        self.btn_group.setExclusive(False)

        manga_list = os.listdir(PARENTFOLDER)
        # This accounts for a fresh startup with no material or material folder
        # Sets these fields to blank as nothing will be selected
        if len(manga_list) == 0:
            self.selected_manga = ""
            self.selected_manga_name = ""
        else:
            self.selected_manga = PARENTFOLDER + "/" + os.listdir(PARENTFOLDER)[0]
            self.selected_manga_name = manga_list[0]
        self.cont = None

        self.centralwidget = QtWidgets.QWidget(self.menu)
        self.centralwidget.setObjectName("centralwidget")

        self.CONTAINER = QtWidgets.QWidget(self.centralwidget)
        self.CONTAINER.setGeometry(QtCore.QRect(400, 20, 381, 561))
        self.CONTAINER.setStyleSheet("background-color: #E7DECD;\n""border-radius:10px;")
        #======================================================================================================================================
        # This is where the selectable manga will be displayed
        self.list_container = QtWidgets.QWidget(self.CONTAINER)
        self.list_container.setGeometry(QtCore.QRect(10, 10, 370, 540))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.list_container)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.list_scrollzone = QtWidgets.QScrollArea(self.list_container)
        self.list_scrollzone.setMinimumSize(QtCore.QSize(0, 0))
        self.list_scrollzone.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 346, 800))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.list_scrollzone.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.list_scrollzone)
        #======================================================================================================================================
        # This button allows the program to be closed
        self.QUIT = QtWidgets.QPushButton(self.centralwidget)
        self.QUIT.setGeometry(QtCore.QRect(20, 550, 41, 31))
        self.QUIT.setStyleSheet("QPushButton {\n""background-color: #E7DECD;\n""border-radius:10px;\n""}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
        quit_ico = QtGui.QIcon()
        quit_ico.addPixmap(QtGui.QPixmap("icons/quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QUIT.setIcon(quit_ico)
        self.QUIT.setIconSize(QtCore.QSize(28, 28))
        self.QUIT.setObjectName("QUIT")
        self.QUIT.clicked.connect(self.quit)
        #======================================================================================================================================
        # This button will close and reopen the menu window to "refresh" the view
        # Used after downloading/deleting a manga
        self.REFRESH = QtWidgets.QPushButton(self.centralwidget)
        self.REFRESH.setGeometry(QtCore.QRect(70, 550, 31, 31))
        self.REFRESH.setStyleSheet("QPushButton {\n""background-color: #E7DECD;\n""border-radius:10px;\n"
"}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/refresh.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.REFRESH.setIcon(icon)
        self.REFRESH.setIconSize(QtCore.QSize(28, 28))
        self.REFRESH.setObjectName("REFRESH")
        self.REFRESH.clicked.connect(lambda: self.menu.close())
        #======================================================================================================================================
        # This button force terminates the program
        # It is used when the user doesn't force terminate the program to stop downloading in the download window
        self.TERMINATE = QtWidgets.QPushButton(self.centralwidget)
        self.TERMINATE.setGeometry(QtCore.QRect(300, 550, 31, 31))
        self.TERMINATE.setStyleSheet("QPushButton {\n""background-color: #E7DECD;\n""border-radius:10px;\n"
"}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/frown.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.TERMINATE.setIcon(icon)
        self.TERMINATE.setIconSize(QtCore.QSize(28, 28))
        self.TERMINATE.setObjectName("TERMINATE")
        self.TERMINATE.clicked.connect(lambda: os._exit(1))

        self.term_info = QtWidgets.QLabel(self.centralwidget)
        self.term_info.setGeometry(QtCore.QRect(175, 555, 125, 15))
        self.term_info.setStyleSheet("font: 63 11pt \"Myriad Pro Light\";")
        self.term_info.setObjectName("info")
        self.term_info.setText("force terminate ->")
        #======================================================================================================================================
        # Area where selected manga information will be displayed
        # Once something valid is selected, the open/delete button will be usable
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

        # This sets the thumbnail label to the thumbnail of the current selected directory
        if self.selected_manga != "":
            self.thumbnail.setPixmap(QtGui.QPixmap(self.selected_manga + "/thumbnail.jpg"))
            num = 0
            with open(self.selected_manga+"/data.txt", "r") as writer:
                num = int(writer.readline().split("\n")[0])
            self.description.setText(self.selected_manga_name + "\n\nTotal Chapters: " + str(len(os.listdir(self.selected_manga)) - 2) + "\nBookmarked Chapter: " + str(num+1))

        #======================================================================================================================================
        # This button opens the manga at the saved chapter
        # Will only run if a manga is present and selected
        self.open = QtWidgets.QPushButton(self.tbn_container)
        self.open.setGeometry(QtCore.QRect(10, 430, 141, 41))
        self.open.setStyleSheet("QPushButton {\n""background-color: rgb(109, 109, 163);\n""border-radius:10px;\n""font: 63 11pt \"Myriad Pro Light\";\n""}\n""\n""QPushButton:hover {\n""background-color: rgb(99, 99, 148);\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(68, 68, 103);\n""}")
        self.open.setIconSize(QtCore.QSize(28, 28))
        self.open.setObjectName("open")
        self.open.clicked.connect(self.open_viewer)
        #======================================================================================================================================
        # This button opens the downloader window to allow the user to download more material
        self.download = QtWidgets.QPushButton(self.tbn_container)
        self.download.setGeometry(QtCore.QRect(270, 430, 51, 41))
        self.download.setStyleSheet("QPushButton {\n""background-color: rgb(109, 109, 163);\n""border-radius:10px;\n""}\n""\n""QPushButton:hover {\n""background-color: rgb(99, 99, 148);\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(68, 68, 103);\n""}")
        download_ico = QtGui.QIcon()
        download_ico.addPixmap(QtGui.QPixmap("icons/download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.download.setIcon(download_ico)
        self.download.setIconSize(QtCore.QSize(28, 28))
        self.download.setObjectName("download")
        self.download.clicked.connect(self.open_downloader)
        #======================================================================================================================================
        # This button allows the user to delete the selected manga from the save location
        self.delete_btn = QtWidgets.QPushButton(self.tbn_container)
        self.delete_btn.setGeometry(QtCore.QRect(200, 430, 51, 41))
        self.delete_btn.setStyleSheet("QPushButton {\n""background-color: rgb(109, 109, 163);\n""border-radius:10px;\n""}\n""\n""QPushButton:hover {\n""background-color: rgb(99, 99, 148);\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(68, 68, 103);\n""}")
        del_ico = QtGui.QIcon()
        del_ico.addPixmap(QtGui.QPixmap("icons/del.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_btn.setIcon(del_ico)
        self.delete_btn.setIconSize(QtCore.QSize(28, 28))
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.clicked.connect(self.rem_confirm)
        #======================================================================================================================================
        self.menu.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        self.btn_group.buttonClicked.connect(self.select_manga)
        QtCore.QMetaObject.connectSlotsByName(self.menu)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.menu.setWindowTitle(_translate("menu", "MangOasis"))
        self.menu.setWindowIcon(QtGui.QIcon("icons/mango_icon.png"))
        self.open.setText(_translate("menu", "OPEN"))
        self.list_available()

    # Function that runs when window is constructed to display downloaded/readable material
    # If no material found, a message in the appropriate container will be displayed
    def list_available(self):
        manga_in_folder = os.listdir(PARENTFOLDER)
        if len(manga_in_folder) == 0:
            self.description.setText("No material found...")
        else:
            total_scroll_height = len(manga_in_folder) * 40
            if total_scroll_height > 561:
                self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 346, total_scroll_height))
                self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, total_scroll_height))
            curr_height = 10
            btn_counter = 0
            for manga in manga_in_folder:
                button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
                button.setGeometry(QtCore.QRect(15, curr_height, 335, 30))
                button.setStyleSheet("QPushButton {\n""background-color: #d4ccbd;\n""border-radius:10px;\nfont: 63 12pt \"Segoe UI Semibold\";\n""}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}")
                button.setText(manga)
                id = btn_counter
                self.btn_group.addButton(button, id)
                btn_counter += 1
                curr_height += 35

    # Function that handles selecting of a manga
    # When user clicks on displayed manga, the thumbnail and relevant info will be updated
    def select_manga(self, btn):
        chosen = os.listdir(PARENTFOLDER)[self.btn_group.id(btn)]
        self.selected_manga = PARENTFOLDER + "/" + chosen
        self.selected_manga_name = chosen
        self.thumbnail.setPixmap(QtGui.QPixmap(self.selected_manga + "/thumbnail.jpg"))
        num = 0
        with open(self.selected_manga+"/data.txt", "r") as writer:
            num = int(writer.readline().split("\n")[0])
        self.description.setText(chosen + "\n\nTotal Chapters: " + str(len(os.listdir(self.selected_manga)) - 2) + "\nBookmarked Chapter: " + str(num+1))

    # Function that handles the quit button being pressed
    # Sets cont boolean to false to let program know to properly close out
    def quit(self):
        self.cont = False
        self.menu.close()

    # Function that handles the open button being pressed
    # Will run prompt asking user if an update should be ran
    def open_viewer(self):
        if self.selected_manga != "":
            check = QtWidgets.QMessageBox()
            check.setWindowTitle("Update window")
            check.setText("Check for updates and download?")
            check.setIcon(QtWidgets.QMessageBox.Question)
            check.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.No)
            check.buttonClicked.connect(self.update)
            check.exec_()
            self.cont = True
            self.menu.close()

    # Function that opens and displays the downloader window
    def open_downloader(self):
        self.dlWindow = QtWidgets.QMainWindow()
        self.ui = Download_Window()
        self.ui.setupUi(self.dlWindow)
        self.dlWindow.show()

    # Child function of open_viewer that is ran when user presses one of the popup buttons
    # Will attempt to run update function from reader.py is ok button is pressed
    def update(self, btnClicked):
        if btnClicked.text() == "OK":
            chs_updated = update_manga(self.selected_manga, self.selected_manga_name)
            check = QtWidgets.QMessageBox()
            check.setWindowTitle("Update window")
            check.setIcon(QtWidgets.QMessageBox.Information)
            check.setStandardButtons(QtWidgets.QMessageBox.Ok)
            if chs_updated > 0:
                check.setText(str(chs_updated) + " chapters were added.")
            else:
                check.setText("Already updated, no chapters added")
            check.exec_()

    # Child function of rem_confirm that runs when user presses a popup button to confirm deletion
    # If confirm is yes, shutil.rmtree function will attempt to remove the directory specified
    def remove_path(self, btnClicked):
        if btnClicked.text() == "&Yes":
            shutil.rmtree(self.selected_manga)

    # Function that displays popup prompting user to confirm deletion of selected manga
    def rem_confirm(self):
        if self.selected_manga != "":
            confirm = QtWidgets.QMessageBox()
            confirm.setWindowTitle("Confirm deletion")
            confirm.setText("Are you sure you want to remove " + self.selected_manga_name + "?")
            confirm.setIcon(QtWidgets.QMessageBox.Warning)
            confirm.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            confirm.buttonClicked.connect(self.remove_path)
            confirm.exec_()

# Function handling running of new main menu instances
def run_instances():
    app = QtWidgets.QApplication(sys.argv)
    menu = QtWidgets.QMainWindow()
    ui = MenuScreen()
    ui.setupUi(menu)
    menu.show()
    app.exec_()
    return ui.selected_manga, ui.selected_manga_name, ui.cont

# Main function that handles processing and running of main menu and reader:control_loop functions
# Working as a while loop, it allows the user to always be moved back to the main menu screen
# when exiting the reader/downloader, or running refresh function
# Upon running, this function will attempt to create the parent directory "Material"
def main():
    try:
        os.mkdir("Material")
    except:
        pass
    while True:
        sel_path, sel_name, cont = run_instances()
        if cont:
            control_loop(sel_path, sel_name)
        elif cont == False:
            sys.exit()

main()