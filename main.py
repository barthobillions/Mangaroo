import reader, downloader
import time

if __name__ == "__main__":
	print("================= SELECT PROGRAM ===================")
	print("                 *ENTER A NUMBER*")
	print("(1) - DOWNLOADER")
	print("(2) - READER")
	print("(q) - QUIT")
	choice = input("> ")
	if choice == '1':
		# Tries to create parent directory. Will be made if not existing
		# If does not exist, 'Material' directory will be made
		print("Creating parent directory...")
		time.sleep(.5)
		try:
			os.mkdir("Material")
		except:
			print("'Material' directory already exists.")
		# download_controller() returns the name and link of the manga
		name, link = downloader.download_controller()
		# data.txt file is created to store this information to be used
		with open("Material/" + name +"/data.txt", "w") as writer:
			writer.write("0\n")
			writer.write(link)
	elif choice == "2":
		reader.control_loop()
	else:
		print("--- QUITTING ---")
