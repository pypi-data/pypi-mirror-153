#!/usr/bin/env python3
import os 
import ast 
import yaml
import boto3
import logging
from gadgethiServerUtils.time_basics import *

default_gserver_location = os.path.expanduser(os.path.join("~", ".gserver"))

# Main API function
# -------------------------
# @@@ 1 @@@
def load_config(cfg_location):
	"""
	load the config file
	"""
	return read_config_yaml(cfg_location)

# @@@ 2 @@@
def read_config_yaml(fn):
	"""
	This is the helper function that reads the config yaml
	file and returns a config dictionary
	- Input:
		fn: filename
	- Returns:
		dict: a config dictionary
	"""
	try:
		with open(fn, 'r', encoding="utf-8") as file:
			# The FullLoader parameter handles the conversion from YAML
			# scalar values to Python the dictionary format
			config_yaml = yaml.load(file, Loader=yaml.FullLoader)
			return config_yaml
	except Exception as e:
		return e

# @@@ 3 @@@
def write_yaml(fn, content, sort_keys=True):
	"""
	This is the helper function that writes to the config yaml and 
	returns the status indicating whether the operation is successful or not.
	- Input:
		* fn: filename
		* content: resulting yaml to be added 
	- Returns:
		A dictionary containing the following keys
		* indicator: True, False whether the operation is completed
		* message: message of operation
	"""
	indicator = True
	message = "Write to yaml successful"
	try:
		with open(fn, "w") as file:
			yaml.dump(content, file, allow_unicode = True, sort_keys=sort_keys)
	except Exception as e:
		indicator = False
		message = str(e) 
	
	return {"indicator":indicator, "message":message}

# @@@ 4 @@@
def read_file_content(parent_directory, file_name):
	"""

	This function reads the content line by line and stores the result in a list

	- Input:
		* parent_directory: Since state_files and promotions files are not kept in the same
		  directory, we need to specify the location (ex. 'state_txt/')
		* file_name: name of file, may be promotion_key (ex. machine_state)

	- Return:
		* content_list: list of read-in data from text file

	"""
	abs_path = get_file_path(parent_directory, file_name)

	with open (abs_path, encoding = "utf8") as read_file:
		content_list =[ast.literal_eval(line.rstrip('\n')) for line in read_file]

	return content_list

# @@@ 5 @@@
def write_file_content(parent_directory, file_name, write_content, newline=True):
	"""
	This function writes list of information into text file

	- Input:
		* parent_directory: Since state_files and promotions files are not kept in the same
		  directory, we need to specify the location (ex. 'state_txt/')
		* file_name: name of file, may be promotion_key (ex. machine_state)
		* write_content: ordered list of lists, with each sublist written to newline
		* newline: whether we want each item to be written in a new line. 

	- Return:
		* message
	"""
	abspath = get_file_path(parent_directory,file_name)

	with open(abspath, 'w') as write_file:
		for index in write_content:
			write_file.write(str(index) + '\n' if newline else "")

	return {"indicator":True,"message":"Machine state text file updated"}

def append_file_content(parent_directory, file_name, write_content):
	"""
	Append given text as a new line at the end of file

	- Input:
		* parent_directory: Since state_files and promotions files are not kept in the same
			directory, we need to specify the location (ex. 'state_txt/')
		* file_name: name of the file
		* write_content: The new line of content
	"""
	abspath = get_file_path(parent_directory,file_name)

	# Open the file in append & read mode ('a+')
	with open(abspath, "a+") as file_object:
		# Move read cursor to the start of file.
		file_object.seek(0)
		# If file is not empty then append '\n'
		data = file_object.read(100)
		if len(data) > 0:
			file_object.write("\n")
		# Append text at the end of file
		file_object.write(write_content)

	return {"indicator":True,"message":"File content appended"}


# @@@ 7 @@@
def init_log(log_parent_directory):
	"""
	This is the helper function to init logger
	* Usage:
		After init, use logging.info(msg) to log messages
		or logging.error(msg) to put different levels of faults
	"""
	try:
		LOG_FILE_PATH = log_parent_directory + serverTime(TimeMode.STRING) + ".txt"
	except:
		raise Exception("Cannot create log file path")

	# level implies that the logger will write all messages greater than level = INFO
	logging.basicConfig(filename=LOG_FILE_PATH, 
						level=logging.INFO, 
						format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    	datefmt='%m-%d %H:%M',
                    	filemode='w'
						)

	# define a Handler which writes INFO messages or higher to the sys.stderr
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	# set a format which is simpler for console use
	formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
	# tell the handler to use this format
	console.setFormatter(formatter)
	# add the handler to the root logger
	logging.getLogger().addHandler(console)

	# CAN USE THE FOLLOWING TO DEFINE LOGGERS IN DIFFERENT REGIONS, defined in
	# different files. 
	# logger1 = logging.getLogger('myapp.area1')
	# logger2 = logging.getLogger('myapp.area2')

# Helper functions
# -------------------------
def get_file_path(parent_directory, file_name):
	"""
	This function gets the absolute path given parent directory and file_name  

	- Input:
		* parent_directory: Since state_files and promotions files are not kept in the same
		  directory, we need to specify the location (ex. 'state_txt/')
		* file_name: name of file, may be promotion_key (ex. machine_state)

	- Return:
		* abs_path: path of the file
	"""
	file = str(file_name) + '.txt'

	abs_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', parent_directory) + '/' + file)

	return abs_path


def check_file_exists(parent_directory, file_name):
	"""

	This function checks whether the text file exists

	- Input:
		* parent_directory: Since state_files and promotions files are not kept in the same
		  directory, we need to specify the location (ex. 'state_txt/')
		* file_name: name of file, may be promotion_key (ex. machine_state)

	- Return:
		* existence: Bool of whether it exists

	"""

	abs_path = get_file_path(parent_directory, file_name)

	return os.path.exists(abs_path)	


# File Handling from S3
# ----------------------------
def fetch_from_s3(bucket, files, tolocation, **configs):
	"""
	This is the helper function to fetch files from s3.
	If you want to fetch all files from a directory 

	- Input:
		* bucket: name of the s3 bucket
		* files: a list of filenames on s3 bucket. It supports
			single file or multiple files.
			e.g. ["database_ini/database.ini", "doday_yamls/*"]
		* tolocation: the local folder that we 
			want to put the fetched files in.
			e.g. ["util/database.ini", "yamls/*"]
	"""
	assert isinstance(files, list) and isinstance(tolocation, list)
	assert len(files) == len(tolocation)

	# connect to s3
	ACCESS_ID = configs.get("aws_access_key_id", None)
	SECRET_KEY = configs.get("aws_secret_access_key", None)
	s3 = boto3.client('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)

	logging.info("Pulling Files From S3....")

	for fileid in range(len(files)):
		# wild card for all files in single folder
		if "*" == files[fileid][-1]:
			s3_folder_header = files[fileid][:-1]
			local_folder_header = tolocation[fileid][:-1]
			objects = s3.list_objects(Bucket=bucket, Prefix=s3_folder_header)["Contents"]
			for obj in objects:
				obj_name = obj["Key"].replace(s3_folder_header, "")
				logging.info(obj_name)
				s3.download_file(bucket, s3_folder_header+obj_name, local_folder_header+obj_name)
		else:
			s3.download_file(bucket, files[fileid], tolocation[fileid])

def read_yaml_on_s3(bucket_name, file_path):
	"""
	This is the helper function to read yaml
	from s3 and return the dictionary of it. 
	"""
	s3 = boto3.client('s3')
	data = s3.get_object(Bucket=bucket_name, Key=file_path)
	contents = data['Body'].read()
	s = contents.decode("utf-8")
	ret_yaml = yaml.safe_load(s)
	return ret_yaml
