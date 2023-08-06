import os
import sys
import logging
import traceback

# Advanced Info on Error
def error_description():
	"""
	This function gets the file path and error line number 
	when a system exception occurs
	"""
	_, _, exc_tb = sys.exc_info()
	fobj = traceback.extract_tb(exc_tb)[-1]
	fname = fobj.filename
	line_no = fobj.lineno
	return fname, line_no, ''.join(traceback.format_tb(exc_tb))

def construct_error_message(header, bounds, description, filename, line_number, tb):
	"""
	This function constructs the error debug message by breaking line
	"""
	file_message = 'Occured in file: {} \n'.format(filename)
	line_number_message = 'At line: {} \n'.format(line_number)
	error_message = tb+header + '\n' + description + '\n' + file_message + line_number_message + bounds + '\n'
	return error_message

# define Python user-defined exceptions
class GadosServerError(Exception):
	"""
	Base class for other exceptions
	filename: The file where the exception happens
	line_number: Line number where the exception occurs
	"""
	def __init__(self, description, fn=None, lineno=None, tb=None):
		super().__init__()
		self.description = description
		self.json_response = {"indicator":False, "message":description}
		self.bounds = "************************************************\n"
		self.fname, self.line_number, self.tb = fn, lineno, tb
		
	def __str__(self):
		self.header = super().__str__()
		if self.fname == None or self.line_number == None or self.tb == None:
			self.fname, self.line_number, self.tb = error_description()
		error_message = construct_error_message(self.header,self.bounds,self.description,self.fname,self.line_number, self.tb)
		logging.error(error_message)
		return error_message

	@classmethod
	def buildfromexc(cls, desc, fname, lineno, tb):
		"""
		This is the class method to return
		an instance based on existing exception
		"""
		return cls(desc, fname, lineno, tb)

class LackOfArgumentsError(Exception):
	'''
	Raised when it's missing some arguments in the input

	Input Arguments
	--------------------
	exec_info: all the system execution information. can be obtained by sys.exc_info()
	missing_arguments: all the missing arguments (list of strings)
	'''

	def __init__(self, missing_arguments):
		super().__init__("")
		self.missing_arguments = missing_arguments
		self.bounds = "************************************************\n"
		self.description  = "Missing: {}".format(missing_arguments)
		self.json_response = {"indicator":False, "message":self.description}

	def __str__(self):
		self.header = super().__str__()
		self.fname, self.line_number, self.tb = error_description()
		error_message = construct_error_message(self.header,self.bounds,self.description,self.fname,self.line_number, self.tb)
		logging.error(error_message)
		return error_message
    

def gexception(function):
	"""
	This is the wrapper function to wrap
	the utility functions and handle error
	"""
	def handle_error(*args, **kwargs):
		"""
		This wraps try except clause around the function
		and return the error message. 
		"""
		response = None
		try:
			response = function(*args, **kwargs)
			ret = {"indicator": True, "message": response}
		except Exception as e:
			_, _, exc_tb = sys.exc_info()
			fobj = traceback.extract_tb(exc_tb)[-1]
			fname = fobj.filename
			line_no = fobj.lineno

			ddyerror = GadosServerError.buildfromexc(str(e), fname, line_no, ''.join(traceback.format_tb(exc_tb)))
			logging.error("GadosServerError = "+str(ddyerror))
			print("GadosServerError = "+str(ddyerror))
			ret = ddyerror.json_response

		if response != None:
			return ret["message"]

	return handle_error