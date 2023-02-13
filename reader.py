from PyQt5 import QtCore, QtGui, QtWidgets
import bs4 as bs
import requests
import ctypes
import time
import cv2
import sys
import os

# gets resolution of monitor to scale window for higher reso screens
WINDOW_RESO = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

# Class that represents the reader GUI, created in Pyqt5
# - MainWindow: main window object to run the events on
# - SCROLLHEIGHT: the total height of the scrollbox based on the number of panels in each chapter
# - WIDTH: The greatest width panel from the chapter to determine how big the box will be. No horizontal scrolling
# - manga_path: The full directory of the manga being read
# - crnt_ch_path: The full directory of the chapter being read
# - chapter_num: Chapter number being read
# - mangaName: Name of the manga
class MangaReaderGUI(QtWidgets.QWidget):
    def setupUi(self, MainWindow, manga_path, crnt_ch_path, chapter_num, mangaName):
        self.MainWindow = MainWindow
        self.mangaName = mangaName
        self.chapter_num = chapter_num
        self.manga_path = manga_path
        self.quitting_return = True
        self.total_height = 0
        panel_dist_buffer = 150 # a distance of 150 pixels between the window border and the panel
        height = WINDOW_RESO[1] * .9 # height of the viewing window box
        self.screen_width = WINDOW_RESO[0] * .625
        self.width = panel_dist_buffer*2 + 1200 # total width of the entire window box
        btn_length = 200 # button length to be scalable with different sized panels
        btn_width = 30
        btn_stylesheet = "QPushButton {\n""background-color: #E7DECD;\n""border-radius:10px;\n""}\n""\n""QPushButton:hover {\n""background-color:#bda06e;\n""\n""}\n""\n""QPushButton:pressed {\n""background-color: rgb(98, 84, 67);\n""}"
        
        self.jump = QtGui.QIcon()
        self.jump.addPixmap(QtGui.QPixmap("icons/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next = QtGui.QIcon()
        self.next.addPixmap(QtGui.QPixmap("icons/next.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prev = QtGui.QIcon()
        self.prev.addPixmap(QtGui.QPixmap("icons/prev.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quit_ico = QtGui.QIcon()
        self.quit_ico.addPixmap(QtGui.QPixmap("icons/quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.setMaximumSize(self.screen_width, height)
        self.MainWindow.resize(self.screen_width, height)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.screen_width, height - 20))
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setStyleSheet("background-color: #E7DECD;")
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.scrollAreaWidgetContents.setStyleSheet("background-color: #0D1317")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setStyleSheet("background-color: #0D1317")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Displays the entire chapter onto the screen
        self.show_chapter(crnt_ch_path)

        # ======================================== BUTTONS ========================================
        #PREVIOUS CHAPTER BUTTON BOTTOM
        self.prevChBttnBOT = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.prevChBttnBOT.setGeometry(QtCore.QRect(panel_dist_buffer, self.total_height, btn_length, btn_width))
        self.prevChBttnBOT.setStyleSheet(btn_stylesheet)
        self.prevChBttnBOT.setIcon(self.prev)
        self.prevChBttnBOT.clicked.connect(lambda: self.btn_press(-1))
        #PREVIOUS CHAPTER BUTTON TOP
        self.prevChBttnTOP = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.prevChBttnTOP.setGeometry(QtCore.QRect(panel_dist_buffer, 10, btn_length, btn_width))
        self.prevChBttnTOP.setStyleSheet(btn_stylesheet)
        self.prevChBttnTOP.setIcon(self.prev)
        self.prevChBttnTOP.clicked.connect(lambda: self.btn_press(-1))
        #NEXT CHAPTER BUTTON BOTTOM
        self.nextChBttnBOT = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.nextChBttnBOT.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length + 10, self.total_height, btn_length, btn_width))
        self.nextChBttnBOT.setStyleSheet(btn_stylesheet)
        self.nextChBttnBOT.setIcon(self.next)
        self.nextChBttnBOT.clicked.connect(lambda: self.btn_press(1))
        #NEXT CHAPTER BUTTON TOP
        self.nextChBttnTOP = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.nextChBttnTOP.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length + 10, 10, btn_length, btn_width))
        self.nextChBttnTOP.setStyleSheet(btn_stylesheet)
        self.nextChBttnTOP.setIcon(self.next)
        self.nextChBttnTOP.clicked.connect(lambda: self.btn_press(1))
        #JUMP TO CHAPTER BUTTON BOTTOM
        self.chooseBtnBOT = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.chooseBtnBOT.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length*2 + 20, self.total_height, btn_length, btn_width))
        self.chooseBtnBOT.setStyleSheet(btn_stylesheet)
        self.chooseBtnBOT.setIcon(self.jump)
        self.chooseBtnBOT.clicked.connect(lambda: self.gotoChapter())
        #JUMP TO CHAPTER BUTTON TOP
        self.chooseBtnTOP = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.chooseBtnTOP.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length*2 + 20, 10, btn_length, btn_width))
        self.chooseBtnTOP.setStyleSheet(btn_stylesheet)
        self.chooseBtnTOP.setIcon(self.jump)
        self.chooseBtnTOP.clicked.connect(lambda: self.gotoChapter())
        #QUIT PROGRAM BUTTON BOTTOM
        self.quitBttnBOT = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.quitBttnBOT.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length*3 + 30, self.total_height, btn_length, btn_width))
        self.quitBttnBOT.setStyleSheet(btn_stylesheet)
        self.quitBttnBOT.setIcon(self.quit_ico)
        self.quitBttnBOT.clicked.connect(lambda: self.quit_program())
        #QUIT PROGRAM BUTTON TOP
        self.quitBttnTOP = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.quitBttnTOP.setGeometry(QtCore.QRect(panel_dist_buffer + btn_length*3 + 30, 10, btn_length, btn_width))
        self.quitBttnTOP.setStyleSheet(btn_stylesheet)
        self.quitBttnTOP.setIcon(self.quit_ico)
        self.quitBttnTOP.clicked.connect(lambda: self.quit_program())
        # ============================================================================================
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", self.mangaName))
        self.MainWindow.setWindowIcon(QtGui.QIcon(self.manga_path + "/thumbnail.jpg"))

    # This method displays the individual panel onto the screen under the previous panel that was displayed
    def display_images(self, path, height, width):
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        label.setScaledContents(True)
        label.setGeometry(QtCore.QRect(150, self.total_height, width, height))
        label.setObjectName("pic_label")
        label.setPixmap(QtGui.QPixmap(path))

    # This method runs the display_images method the total panel number of times in a chapter
    # Returns the cumulative height to display the buttons
    def show_chapter(self, chPath):
        # Gets files in chapter directory and removes the extension from each string,
        # then converts each string into an integer, and finally sorts the list
        panels = convert_to_int(remove_extension(os.listdir(chPath), '.'))
        # This is the fully cleaned and sorted panels list
        panels.sort()
        panel_target_width = (WINDOW_RESO[0] * (WINDOW_RESO[0] * .47))
        # Panels start populating 70 pixels down from the window border
        self.total_height = 50
        for img in panels:
            height, width, _ = cv2.imread(chPath + "/" + str(img) + ".jpg").shape
            scalar = 900/width
            width = width * scalar
            height = height * scalar
            self.display_images(chPath + "/" + str(img) + '.jpg', height, width)
            self.total_height += height + 15

        self.frame.setMinimumSize(QtCore.QSize(self.width, self.total_height + 50))


    # This method handles button presses to change chapters, "PREVIOUS" and "NEXT"
    def btn_press(self, change_chapter):
        ch, link = read_data_file(self.manga_path + "/data.txt")
        if change_chapter == 1:
            if self.chapter_num < len(os.listdir(self.manga_path)) - 2:
                file = open(self.manga_path + "/data.txt", "w")
                file.write(str(self.chapter_num + 1) + "\n")
                file.write(link)
                file.close()
                self.MainWindow.close()
        else:
            if self.chapter_num > 0:
                file = open(self.manga_path + "/data.txt", "w")
                file.write(str(self.chapter_num - 1) + "\n")
                file.write(link)
                file.close()
                self.MainWindow.close()

    # Function to deal with quit button press
    def quit_program(self):
        self.quitting_return = False
        self.MainWindow.close()

    # This method handles the "GO TO" button, allows user to enter a chapter to jump to
    # Only allows input if it falls in the range of number of chapters
    # If input fails (out of range or invalid input such as a char/string), nothing will happen and the pop-up window will simply close
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

# Takes in a list, removes a passed in extension, and returns new
# cleaned list
def remove_extension(array, char):
    cleaned_int = []
    for item in array:
        cleaned_int.append(item.split(".")[0])
    return cleaned_int

# Takes in a list of ints in the form of strings and converts every element to its int form
def convert_to_int(list_path):
    converted = []
    for item in list_path:
        converted.append(int(item))
    return converted

# This method will create the current view window for the chapter of the manga being read
# After a chapter is changed, the window will reopen with the new updated panels of a different chapter
def open_view_window(manga_path, manga_title, chapter):
    app1 = QtWidgets.QApplication(sys.argv)
    reader_win = QtWidgets.QMainWindow()
    home = MangaReaderGUI()
    # removes the data.txt file, converts every element into an int, then sorts
    # this is to deal with os.listdir() collecting the files in a differently sorted pattern
    ch_list = os.listdir(manga_path)
    ch_list.remove("data.txt")
    ch_list.remove("thumbnail.jpg")
    ch_list = convert_to_int(ch_list)
    ch_list.sort()
    crnt_ch_path = manga_path + "/" + str(ch_list[chapter])
    home.setupUi(reader_win, manga_path, crnt_ch_path, chapter, manga_title +  ": Chapter " + str(chapter + 1))
    reader_win.show()
    app1.exec_()

    return home.quitting_return


# Reads in data file and returns the current chapter number, and link of the manga
def read_data_file(path):
    num = 0
    link = ""
    with open(path, "r") as writer:
        num = int(writer.readline().split("\n")[0])
        link = writer.readline()
    return num, link

# Checks manga site for update, will download missing chapters if prompted to
def update_manga(manga_path, name):
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
    missing_ch = 0

    # if total amount of chapters found on site is greater than total amount of chapters
    # in directory, this portion will run to download them
    if len(chapters) > total_chs:
        missing_ch = len(chapters) - total_chs
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9",
           "Referer": link}
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
            dir_name = "Material/" + name + "/" + str(total_chs)

            # Tries to create the directory with this name, in event a download retry
            try:
                os.mkdir(dir_name)
            except:
                pass

            # The request and saving of image file in each chapter
            size = len(img_links_container)
            counter = 1
            for item in img_links_container:
                while True:
                    try:
                        img_link = item.get('src')
                        img_data = requests.get(img_link, headers=headers).content
                        with open(dir_name + "/" + str(counter) + '.jpg', 'wb') as writer:
                            writer.write(img_data)
                        break
                    except:
                        pass
                counter += 1
            ch_counter += 1
    return missing_ch

# The main control method that is called in the menu.py script
# Now uses GUI to control which manga to be displayed
# Manga progression is saved in a data file called 'data.txt'
# This file is edited and saved everytime a chapter change happens so the user can resume
# where they left off after quitting.
def control_loop(manga_path, manga_title):
    # MAIN WHILE LOOP THAT RUNS THE PROGRAM UNTIL QUIT
    # Runs open window function at the chapter found in the 'data.txt' file
    cont = True
    while cont:
        file = open(manga_path + "/data.txt", "r")
        chapter = int(file.readline().split("\n")[0])
        file.close()
        cont = open_view_window(manga_path, manga_title, chapter)