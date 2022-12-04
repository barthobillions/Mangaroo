import reader, downloader

if __name__ == "__main__":
	print("================= SELECT PROGRAM ===================")
	print("(0) - DOWNLOADER")
	print("(1) - READER")
	choice = input("> ")
	if choice == '0':
		downloader.download_controller()
	else:
		reader.control_loop()