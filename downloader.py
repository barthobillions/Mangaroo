from selenium.webdriver.common.keys import Keys
from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
import bs4 as bs
import requests
import time
import sys
import os

PARENTFOLDER = "Material"

# Opens a headless selenium browser and defaults to the manganato site.
# The inputed manga title will be searched in the search bar, and the first option will be chosen
def get_link(console_object, manga):
	manga_site = "https://manganato.com/"
	drivers = "drivers/chromedriver.exe"
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors-spki-list') # blocks errors that may appear from chrome related things
	options.add_argument('--ignore-ssl-errors')
	options.add_argument('--log-level=3')
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_argument('headless')

	# Opens the browser and goes to the manga site
	send_to_console(console_object, "Connecting to site...", .7)
	browser = webdriver.Chrome(drivers, options=options)
	browser.get(manga_site)

	# full xpath for the searchbar that will be inputed into
	searchbar = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/form/input[1]').send_keys(manga)
	send_to_console(console_object, "--- CONNECTION SUCCESSFUL ---", .7)

	# Tries to keep collecting the search results as some connections may be
	# slower than others. This will deal with connection times
	send_to_console(console_object, "*Search will timeout if no results within 60 seconds*", .7)
	crntTime = time.time()
	while True:
		try:
			search_result = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/form/div/ul/a')
			break
		except:
			if time.time() - crntTime > 60:
				send_to_console(console_object, "60 seconds elapsed with no results, timed out...", .7)
				return False, None, None

	# Gets the link of the manga found in search bar and goes to it
	send_to_console(console_object, "--- FOUND MANGA ---", .7)
	link = search_result.get_attribute("href")
	browser.get(link)

	# Once again, tries to collect the name of the manga. Will deal with different speeds of connections
	send_to_console(console_object, "--- LOADING DATA ---", .7)
	while True:
		try:
			name = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/h1').text
			break
		except:
			pass
	
	return True, name, link


# This will use the link and name retrieved from the get_link method, along with the pathname of the manga
# to download the chapters.
def download_manga(console_object, name, link):
	console_object.clear()
	send_to_console(console_object, "=======================================================================", 0)
	send_to_console(console_object, "		        DOWNLOADING " + name, 0)
	send_to_console(console_object, "	-Press frown(top left) to force shutdown", 0)
	send_to_console(console_object, "		*use if download stuck or want to cancel download*", 0)
	send_to_console(console_object, "	-Press X(top right) to close this window", 0)
	send_to_console(console_object, "=======================================================================", 0)
	# Headers that allow searches and requests to be made without being redirected
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9",
           "Referer": link}

    # Gets the page contents at the manga link and gets it into a beautiful soup object
	source = requests.get(link).text
	soup = bs.BeautifulSoup(source, 'lxml')

	# Collects the chapters list box that holds the links to every chapter
	content = soup.find('ul', class_='row-content-chapter')
	# The actual individual chapters collected into an array
	chapters = content.find_all('li')
	# Tries to create parente directory, "Material/'manga_name'"
	# In the event a download retry of a manga happens, a directory can be
	# accounted for, either created or already existing
	try:
		os.mkdir(PARENTFOLDER + "/" + name)
	except:
		pass

	# Gets link for thumbnail and writes it to the file 'thumbnail.jpg'
	thumbnail_link = soup.find('span', class_='info-image').find('img').get('src')
	thumbnail = requests.get(thumbnail_link, headers=headers).content
	with open(PARENTFOLDER + "/" + name + "/thumbnail.jpg", 'wb') as writer:
		writer.write(thumbnail)
	# Reverses the chapters array as collected in descending order
	# Gets link to each chapter in the list and requests the html
	header = console_object.text()
	header = header.split("\n",1)[1]
	ch_counter = 1
	for chapter in reversed(chapters):
		console_object.clear()
		current_text = header + "\nCompleted " + str(ch_counter) + " of " + str(len(chapters))
		send_to_console(console_object, current_text, 0)
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
		dir_name = PARENTFOLDER + "/" + name + "/" + str(ch_counter)

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

	send_to_console(console_object, "-- DOWNLOAD COMPLETED --", 2)


# Function that takes in the pyqt window object so it can send relevant print data to the user
# This information is displayed on the pyqt window.
def send_to_console(console_object, msg, duration):
	console_object.setText(console_object.text() + "\n" + msg)
	if duration > 0:
		time.sleep(duration)


# This is the main control function for getting needed data and downloading to the directory.
def download_controller(console_object, name):
	success, name, link = get_link(console_object, name)

	send_to_console(console_object, "--- RESULTS ---", .7)

	if not success:
		send_to_console(console_object, find_manga + " was not found in current databases.", .3)
		send_to_console(console_object, find_manga + "Returning to main menu.", 2)
		return

	send_to_console(console_object, "Found: " + name + ": " + link, .7)
	send_to_console(console_object, "DOWNLOAD ATTEMPT IN 5 SECONDS, QUIT IF YOU WANT TO CANCEL PROCESS", 5)

	send_to_console(console_object, "--- PREPARING TO DOWNLOAD ---", 2)

	os.mkdir(PARENTFOLDER + "/" + name)
	# data.txt file is created to store this information to be used
	with open(PARENTFOLDER + "/" + name +"/data.txt", "w") as writer:
		writer.write("0\n")
		writer.write(link)

	# RUNS THE DOWNLOAD METHOD
	download_manga(console_object, name, link)