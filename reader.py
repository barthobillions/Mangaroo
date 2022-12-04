from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import os
import sys

# Class that represents the reader GUI, created in Pyqt5
# - MainWindow: main window object to run the events on
# - SCROLLHEIGHT: the total height of the scrollbox based on the number of panels in each chapter
# - WIDTH: The greatest width panel from the chapter to determine how big the box will be. No horizontal scrolling
# - manga_path: The full directory of the manga being read
# - crnt_ch_path: The full directory of the chapter being read
# - chapter_num: Chapter number being read
# - mangaName: Name of the manga
class MangaReaderGUI(QtWidgets.QWidget):
    def setupUi(self, MainWindow, SCROLLHEIGHT, WIDTH, manga_path, crnt_ch_path, chapter_num, mangaName):
        self.mangaName = mangaName
        self.chapter_num = chapter_num
        self.manga_path = manga_path
        self.MainWindow = MainWindow
        panel_dist_buffer = 150 # a distance of 150 pixels between the window border and the panel
        height = 1000 # height of the viewing window box
        width = panel_dist_buffer*2 + WIDTH # total width of the entire window box
        btn_length = (WIDTH / 4) - 50 # button length to be scalable with different sized panels
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(width, height)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, width, height))
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setStyleSheet("background-color: rgb(229, 123, 137)")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 781, 5018))
        self.scrollAreaWidgetContents.setStyleSheet("background-color: rgb(229, 123, 137)")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setMinimumSize(QtCore.QSize(0, SCROLLHEIGHT))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Displays the entire chapter onto the screen and returns entire height to display buttons at
        cumu_height = self.show_chapter(crnt_ch_path)


        # ======================================== BUTTONS ========================================
        #PREVIOUS CHAPTER BUTTON
        self.prevChBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.prevChBttn.setGeometry(QtCore.QRect(panel_dist_buffer, cumu_height + 15, btn_length, 30))
        self.prevChBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.prevChBttn.setText("PREVIOUS")
        self.prevChBttn.setObjectName("prevChBttn")
        self.prevChBttn.clicked.connect(lambda: self.btn_press(-1))

        #NEXT CHAPTER BUTTON
        self.nextChBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.nextChBttn.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length + 10, cumu_height + 15, btn_length, 30))
        self.nextChBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.nextChBttn.setText("NEXT")
        self.nextChBttn.setObjectName("nextChBttn")
        self.nextChBttn.clicked.connect(lambda: self.btn_press(1))

        #JUMP TO CHAPTER BUTTON
        self.chooseBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.chooseBtn.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length*2 + 20, cumu_height + 15, btn_length, 30))
        self.chooseBtn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.chooseBtn.setText("...")
        self.chooseBtn.setObjectName("chooseBtn")
        self.chooseBtn.clicked.connect(lambda: self.gotoChapter())

        #QUIT PROGRAM BUTTON 
        self.quitBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.quitBttn.setGeometry(QtCore.QRect(WIDTH - btn_length + panel_dist_buffer, cumu_height + 15, btn_length, 30))
        self.quitBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.quitBttn.setText("QUIT")
        self.quitBttn.setObjectName("quitBttn")
        self.quitBttn.clicked.connect(lambda: sys.exit())
        # ============================================================================================

        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", self.mangaName))

    # This method displays the individual panel onto the screen under the previous panel that was displayed
    def display_images(self, path, height, width, cumu_height):
        # print("placing image with dim: " + height + width + " at 0 x " + )
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        label.setScaledContents(True)
        label.setGeometry(QtCore.QRect(150, cumu_height, width, height))
        label.setObjectName("l")
        label.setPixmap(QtGui.QPixmap(path))

    # This method runs the display_images method the total panel number of times in a chapter
    # Returns the cumulative height to display the buttons
    def show_chapter(self, chPath):
        cumu_height = 10
        for img in os.listdir(chPath):
            height, width, _ = cv2.imread(chPath + "/" + img).shape
            self.display_images(chPath + "/" + img, height, width, cumu_height)
            cumu_height += height
        return cumu_height

    # This method handles button presses to change chapters, "PREVIOUS" "NEXT"
    def btn_press(self, change_chapter):
        file = open(self.manga_path + "/data.txt", "w")
        if change_chapter == 1:
            if self.chapter_num < len(os.listdir(self.manga_path)) - 2:
                file.write(str(self.chapter_num + 1))
                file.close()
                self.MainWindow.close()
        else:
            if self.chapter_num > 0:
                file.write(str(self.chapter_num - 1))
                file.close()
                self.MainWindow.close()

    # This method handles the "GO TO" button, allows user to enter a chapter to jump right to
    # Only allows input if it falls in the range of number of chapters
    # If input fails, nothing will happen and user will be returned back to the GUI window
    def gotoChapter(self):
        avail_ch = len(os.listdir(self.manga_path)) - 1
        chapter, valid = QtWidgets.QInputDialog.getText(self, self.mangaName, "Go to(" + str(avail_ch) + " total chapters):")
        if valid:
            try:
                if int(chapter) <= avail_ch and int(chapter) > 0:
                    chapter = int(chapter) - 1
                    file = open(self.manga_path + "/data.txt", "w")
                    file.write(str(chapter))
                    file.close()
                    self.MainWindow.close()
            except:
                pass

# This method will create the current view window for the chapter of the manga being read
# After a chapter is changed, the window will reopen with the new updated panels of a different chapter
def open_view_window(manga_path, manga_title, chapter):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    home = MangaReaderGUI()
    cleaned_path = os.listdir(manga_path)
    cleaned_path.remove("data.txt")
    crnt_ch_path = manga_path + "/" + cleaned_path[chapter]

    TOTAL_HEIGHT = 0
    GREATEST_WIDTH = 0

    for image in os.listdir(crnt_ch_path):
        y, x, _ = cv2.imread(crnt_ch_path + "/" + image).shape
        if x > GREATEST_WIDTH:
            GREATEST_WIDTH = x
        TOTAL_HEIGHT += y

    home.setupUi(MainWindow, TOTAL_HEIGHT + 70, GREATEST_WIDTH, manga_path, crnt_ch_path, chapter, manga_title +  ": Chapter " + str(chapter + 1))
    MainWindow.show()
    app.exec_()


# The main method that handles user choosing which manga that exists in the 'Material' directory
# If valid, the method will keep running until the quit button is pressed
# The exit button at the top of the window will not work, QUIT needs to be pressed to safely exit
# Manga progression is saved in a data file called 'data.txt'
# This file is edited and saved everytime a chapter change happens so the user can resume
# where they left off after quitting.
def main():
    PARENTFOLDER = "Material"
    mangas = os.listdir(PARENTFOLDER)

    for manga in range(len(mangas)):
        print(str(manga) + ": " + mangas[manga])

    choice = int(input("Choose manga: "))

    manga_title = mangas[choice]
    manga_path = PARENTFOLDER + "/" + manga_title
    # Checks if user left off on a chapter that is not the first chapter
    try:
        file = open(PARENTFOLDER + "/" + manga_title + "/data.txt", "r")
        num = int(file.read())
        if num > 0:
            print("You last left off on Chapter " + str(num + 1))
        file.close()
    # If try did not work, that means the data.txt file does not exist
    # This will create the file and start the user at chapter 1
    except:
        file = open(PARENTFOLDER + "/" + manga_title + "/data.txt", "w")
        file.write("0")
        file.close()

    # MAIN WHILE LOOP THAT RUNS THE PROGRAM UNTIL QUIT IS PRESSED
    # Runs open_view_window at the chapter found in the 'data.txt' file
    while True:
        file = open(PARENTFOLDER + "/" + manga_title + "/data.txt", "r")
        chapter = int(file.read())
        file.close()
        open_view_window(manga_path, manga_title, chapter)

main()