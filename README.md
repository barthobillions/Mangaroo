# MangaReader
This program downloads a specified manga, and allows the user to read the manga through a PYQT5 GUI.
The only site the program parses is manganato; I will be adding more site compatibilities
As of currently, the GUI only consists of command line for the initial download and choosing of manga to open.

Working on main menu GUI where users can browse their stored media, and a portion for downloading without command line interfacing.

https://drive.google.com/file/d/18F5w_B4mMKhJ6Oao8tud9_PrS-m41tXv/view?usp=share_link
=============================================================================================
WORKING COMPILED VERSION OF THE APP CAN BE FOUND AT THE LINK ABOVE

You will need to extract everything and keep all of the files inside in one directory
It will only work if the download_controller() (downloads entire manga) function finishes as data.txt will be created
after that.
This data file stores necessary information for the current version to work.
If the entire manga is not wanted, users can stop the download and manually create the file.
It needs to be named 'data.txt' (a text file), the user will type in a zero on the first line, hit enter, and paste in the link of the manga.
