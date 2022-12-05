import reader, downloader

if __name__ == "__main__":
	print("================= SELECT PROGRAM ===================")
	print("                 *ENTER A NUMBER*")
	print("(1) - DOWNLOADER")
	print("(2) - READER")
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
			time.sleep(.5)
		name, link = downloader.download_controller()
		with open("Material/" + name +"/data.txt", "w") as writer:
			writer.write(link)
	else:
		reader.control_loop()
