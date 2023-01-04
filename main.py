import reader, downloader
import os
import time

if __name__ == "__main__":
	# Tries to create parent directory. Will be made if not existing
	# If does not exist, 'Material' directory will be made
	print("Creating parent directory...")
	time.sleep(.8)
	try:
		os.mkdir("Material")
		print("No existing material found, created parent directory located at 'Material'")
	except:
		print("'Material' directory already exists.")
	time.sleep(.8)
	run = True
	while run:
		os.system('cls')
		print("================= SELECT PROGRAM ===================")
		print("                 *ENTER A NUMBER*")
		print("(1) - DOWNLOADER")
		print("(2) - READER")
		print("(x) - QUIT")
		choice = input("> ")
		if choice == '1':
			# download_controller() returns the name and link of the manga
			downloader.download_controller()
		elif choice == "2":
			reader.control_loop()
		elif choice == "x":
			print("--- QUITTING ---")
			time.sleep(1)
			run = False
		else:
			print("Invalid choice...")
			time.sleep(.7)