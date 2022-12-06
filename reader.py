from PyQt5 import QtCore, QtGui, QtWidgets
import bs4 as bs
import requests
import win32gui
import win32con
import time
import cv2
import os
import sys

# grabs the id of the console
console = win32gui.GetForegroundWindow()

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
        screen_width = 1000
        width = panel_dist_buffer*2 + WIDTH # total width of the entire window box
        btn_length = (WIDTH / 4) - 50 # button length to be scalable with different sized panels
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setFixedSize(screen_width, height)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, screen_width, height - 20))
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
        self.frame.setMinimumSize(QtCore.QSize(width, SCROLLHEIGHT))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Displays the entire chapter onto the screen and returns entire height to display buttons at
        cumu_height = self.show_chapter(crnt_ch_path)


        # ======================================== BUTTONS ========================================
        #PREVIOUS CHAPTER BUTTON BOTTOM
        self.prevChBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.prevChBttn.setGeometry(QtCore.QRect(panel_dist_buffer, cumu_height + 15, btn_length, 30))
        self.prevChBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.prevChBttn.setText("PREVIOUS")
        self.prevChBttn.setObjectName("prevChBttn")
        self.prevChBttn.clicked.connect(lambda: self.btn_press(-1))
        #PREVIOUS CHAPTER BUTTON TOP
        self.prevChBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.prevChBttn.setGeometry(QtCore.QRect(panel_dist_buffer, 15, btn_length, 30))
        self.prevChBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.prevChBttn.setText("PREVIOUS")
        self.prevChBttn.setObjectName("prevChBttn")
        self.prevChBttn.clicked.connect(lambda: self.btn_press(-1))
        #NEXT CHAPTER BUTTON BOTTOM
        self.nextChBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.nextChBttn.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length + 10, cumu_height + 15, btn_length, 30))
        self.nextChBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.nextChBttn.setText("NEXT")
        self.nextChBttn.setObjectName("nextChBttn")
        self.nextChBttn.clicked.connect(lambda: self.btn_press(1))

        #NEXT CHAPTER BUTTON TOP
        self.nextChBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.nextChBttn.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length + 10, 15, btn_length, 30))
        self.nextChBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.nextChBttn.setText("NEXT")
        self.nextChBttn.setObjectName("nextChBttn")
        self.nextChBttn.clicked.connect(lambda: self.btn_press(1))
        #JUMP TO CHAPTER BUTTON BOTTOM
        self.chooseBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.chooseBtn.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length*2 + 20, cumu_height + 15, btn_length, 30))
        self.chooseBtn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.chooseBtn.setText("...")
        self.chooseBtn.setObjectName("chooseBtn")
        self.chooseBtn.clicked.connect(lambda: self.gotoChapter())
        #JUMP TO CHAPTER BUTTON TOP
        self.chooseBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.chooseBtn.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length*2 + 20, 15, btn_length, 30))
        self.chooseBtn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.chooseBtn.setText("...")
        self.chooseBtn.setObjectName("chooseBtn")
        self.chooseBtn.clicked.connect(lambda: self.gotoChapter())
        #QUIT PROGRAM BUTTON BOTTOM
        self.quitBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.quitBttn.setGeometry(QtCore.QRect(WIDTH - btn_length + panel_dist_buffer, cumu_height + 15, btn_length, 30))
        self.quitBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.quitBttn.setText("QUIT")
        self.quitBttn.setObjectName("quitBttn")
        self.quitBttn.clicked.connect(lambda: sys.exit())
        #QUIT PROGRAM BUTTON TOP
        self.quitBttn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.quitBttn.setGeometry(QtCore.QRect(WIDTH - btn_length + panel_dist_buffer, 15, btn_length, 30))
        self.quitBttn.setStyleSheet("background-color: rgb(255, 188, 192)")
        self.quitBttn.setText("QUIT")
        self.quitBttn.setObjectName("quitBttn")
        self.quitBttn.clicked.connect(lambda: self.quit_program())
        # ============================================================================================
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", self.mangaName))

    # This method displays the individual panel onto the screen under the previous panel that was displayed
    def display_images(self, path, height, width, cumu_height):
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        label.setScaledContents(True)
        label.setGeometry(QtCore.QRect(150, cumu_height, width, height))
        label.setObjectName("pic_label")
        label.setPixmap(QtGui.QPixmap(path))

    # This method runs the display_images method the total panel number of times in a chapter
    # Returns the cumulative height to display the buttons
    def show_chapter(self, chPath):
        panels = os.listdir(chPath)
        panels = remove_extension(panels, '.')
        panels = convert_to_int(panels)
        panels.sort()

        cumu_height = 70
        for img in panels:
            height, width, _ = cv2.imread(chPath + "/" + str(img) + ".jpg").shape
            self.display_images(chPath + "/" + str(img) + '.jpg', height, width, cumu_height)
            cumu_height += height
        return cumu_height

    # This method handles button presses to change chapters, "PREVIOUS" and "NEXT"
    def btn_press(self, change_chapter):
        ch, link = read_data_file(self.manga_path + "/data.txt")
        file = open(self.manga_path + "/data.txt", "w")
        if change_chapter == 1:
            if self.chapter_num < len(os.listdir(self.manga_path)) - 2:
                file.write(str(self.chapter_num + 1) + "\n")
                file.write(link)
                file.close()
                self.MainWindow.close()
        else:
            if self.chapter_num > 0:
                file.write(str(self.chapter_num - 1) + "\n")
                file.write(link)
                file.close()
                self.MainWindow.close()

    # Function to deal with quit button press
    def quit_program(self):
        sys.exit()

    # This method handles the "GO TO" button, allows user to enter a chapter to jump right to
    # Only allows input if it falls in the range of number of chapters
    # If input fails, nothing will happen and user will be returned back to the GUI window
    def gotoChapter(self):
        avail_ch = len(os.listdir(self.manga_path)) - 1
        chapter, valid = QtWidgets.QInputDialog.getText(self, self.mangaName, "Go to(" + str(avail_ch) + " total chapters):")
        if valid:
            try:
                if int(chapter) <= avail_ch and int(chapter) > 0:
                    crnt_ch, link = read_data_file(self.manga_path + "/data.txt")
                    chapter = int(chapter) - 1
                    if crnt_ch != chapter:
                        file = open(self.manga_path + "/data.txt", "w")
                        file.write(str(chapter) + "\n")
                        file.write(link)
                        file.close()
                        self.MainWindow.close()
            except:
                pass

# Takes in a list and removes a passed in extension
def remove_extension(array, char):
    cleaned_int = []
    for item in array:
        cleaned_int.append(item.split(".")[0])
    return cleaned_int

# Takes in a list of ints in the form of strings and converts every element to its int form
def convert_to_int(array):
    converted = []
    for item in array:
        converted.append(int(item))
    return converted

# This method will create the current view window for the chapter of the manga being read
# After a chapter is changed, the window will reopen with the new updated panels of a different chapter
def open_view_window(manga_path, manga_title, chapter):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    home = MangaReaderGUI()
    ch_list = os.listdir(manga_path)
    # removes the data.txt file, converts every element into an int, then sorts
    # this is to deal with os.listdir() collecting the files in a differently sorted pattern
    ch_list.remove("data.txt")
    ch_list = convert_to_int(ch_list)
    ch_list.sort()
    crnt_ch_path = manga_path + "/" + str(ch_list[chapter])

    TOTAL_HEIGHT = 0
    GREATEST_WIDTH = 0

    for image in os.listdir(crnt_ch_path):
        y, x, _ = cv2.imread(crnt_ch_path + "/" + image).shape
        if x > GREATEST_WIDTH:
            GREATEST_WIDTH = x
        TOTAL_HEIGHT += y

    home.setupUi(MainWindow, TOTAL_HEIGHT + 140, GREATEST_WIDTH, manga_path, crnt_ch_path, chapter, manga_title +  ": Chapter " + str(chapter + 1))
    MainWindow.show()
    app.exec_()

# Reads in data file and returns the current chapter number, and link of the manga
def read_data_file(path):
    num = 0
    link = ""
    with open(path, "r") as writer:
        num = int(writer.readline().split("\n")[0])
        link = writer.readline()
    return num, link

# Checks manga site for update, will download missing chapters if prompted to
def update(manga_path, name):
    print("Checking site for updates on " + name)
    time.sleep(.3)
    _, link = read_data_file(manga_path + "/data.txt")
    ch_in_dir = os.listdir(manga_path)
    total_chs = len(ch_in_dir) - 1
    # Gets the page contents at the manga link and gets it into a beautiful soup object
    source = requests.get(link).text
    soup = bs.BeautifulSoup(source, 'lxml')
    # Collects the chapters list box that holds the links to every chapter
    content = chapters = soup.find('ul', class_='row-content-chapter')
    # The actual individual chapters collected into an array
    chapters = content.find_all('li')

    # if total amount of chapters found on site is greater than total amount of chapters
    # in directory, this portion will run to download them
    if len(chapters) > total_chs:
        missing_ch = len(chapters) - total_chs
        print("You are missing " + str(missing_ch) + " of the latest chapters.")
        time.sleep(.3)
        print("Would you like to update now(y/n)?")
        choice = input("> ")
        if choice == "y":
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.9",
               "Referer": link}
            print("===================== UPDATING =====================")
            add_ch = []
            for ch in range(missing_ch):
                add_ch.append(chapters[ch])
            ch_counter = 1
            for chapter in reversed(add_ch):
                while True:
                    try:
                        current_chapter_source = requests.get(chapter.find('a').get('href')).text
                        current_chapter = bs.BeautifulSoup(current_chapter_source, 'lxml')

                        # Container that houses the information for the current chapter link
                        container = current_chapter.find('div', class_='container-chapter-reader')
                        # This contains all of the panels in the chapter being parsed
                        img_links_container = container.find_all('img')
                        break
                    except:
                        pass

                # The directory name of the current chapter
                # EXAMPLE: "Material/'manga_name'/Chapter 1"
                total_chs += 1
                dir_name = "Material" + "/" + name + "/" + str(total_chs)

                # Tries to create the directory with this name, in event a download retry
                try:
                    os.mkdir(dir_name)
                except:
                    pass

                # The request and saving of image file in each chapter
                size = len(img_links_container)
                counter = 1
                print(str(ch_counter) + "/" + str(missing_ch))
                for item in img_links_container:
                    while True:
                        try:
                            img_link = item.get('src')
                            img_data = requests.get(img_link, headers=headers).content
                            with open(dir_name + "/" + str(counter) + '.jpg', 'wb') as writer:
                                writer.write(img_data)
                            # Printing percentages to show progress
                            sys.stdout.write("\r" + str(int(counter/size * 100)) + "%")
                            sys.stdout.flush()
                            break
                        except:
                            pass
                    counter += 1
                ch_counter += 1
                print()
    print("You are up to date on " + name)
    time.sleep(.4)

# The main method that handles user choosing which manga that exists in the 'Material' directory
# If valid, the method will keep running until the quit button is pressed
# The exit button at the top of the window will not work, QUIT needs to be pressed to safely exit
# Manga progression is saved in a data file called 'data.txt'
# This file is edited and saved everytime a chapter change happens so the user can resume
# where they left off after quitting.
def control_loop():
    PARENTFOLDER = "Material"
    mangas = os.listdir(PARENTFOLDER)

    print("================= SELECT MANGA ===================")
    print("                *ENTER A NUMBER*")
    for manga in range(len(mangas)):
        print("(" + str(manga + 1) + ")" + " - " + mangas[manga])

    print()
    while True:
        choice = int(input("> "))
        # try:
        #     manga_title = mangas[choice-1]
        #     update(PARENTFOLDER + "/" + manga_title)
        #     break
        # except:
        #     print("Option does not exist.")

        manga_title = mangas[choice-1]
        update(PARENTFOLDER + "/" + manga_title, manga_title)
        break

    manga_path = PARENTFOLDER + "/" + manga_title
    # Checks if user left off on a chapter that is not the first chapter
    num, link = read_data_file(PARENTFOLDER + "/" + manga_title + "/data.txt")
    if num > 0:
        print("You last left off on Chapter " + str(num + 1))
        time.sleep(.5)

    # hides the console from user, won't be brought up again
    win32gui.ShowWindow(console , win32con.SW_HIDE)

    # MAIN WHILE LOOP THAT RUNS THE PROGRAM UNTIL QUIT IS PRESSED
    # Runs open_view_window at the chapter found in the 'data.txt' file
    while True:
        file = open(PARENTFOLDER + "/" + manga_title + "/data.txt", "r")
        chapter = int(file.readline().split("\n")[0])
        file.close()
        open_view_window(manga_path, manga_title, chapter)