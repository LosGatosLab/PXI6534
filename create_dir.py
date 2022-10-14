import os

def create_dir(file_dir_data):
	# Check whether the specified path exists or not
	isExist = os.path.exists(file_dir_data)
	if not isExist:
	  os.makedirs(file_dir_data)
	# print("*** Save Path: "+file_dir_data+" ***")