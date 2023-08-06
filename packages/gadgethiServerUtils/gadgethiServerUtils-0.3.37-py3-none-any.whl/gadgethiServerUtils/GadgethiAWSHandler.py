#-*-coding:utf-8 -*-
from urllib.parse import unquote
from io import BytesIO, BufferedReader
import threading

from gadgethiServerUtils._exceptions import *
from gadgethiServerUtils.db_operations import *
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import *

import os
import json
import sys
import logging

from os.path import expanduser

class GadgetHiAWSHandler:
	"""
	Represent the base handler for AWS lambda
	"""
	def __init__(self, service_handler=lambda a,**c: None, authentication=False, 
		**kwargs):
		self.configs = kwargs
		self.service_handler = service_handler
		self.authentication = authentication

	def handle(self, event, context):
		"""
		Main function to handle event and context
		from AWS REST API integration. 
		TODO: Include this version number
		to avoid future upgrade crashes
		"""
		input_dictionary = {}
		input_dictionary["values"] = event["queryStringParameters"] if "queryStringParameters" in event else {}
		input_dictionary["method"] = event["httpMethod"]
		input_dictionary["form"] = {}

		body = event["body"]
		headers = self.header_helper(event["headers"])
		content_type = headers['content-type'] if 'content-type' in headers else None

		if self.authentication:
			# Get authentication information
			auth_flag, auth_msg = self.authentication_helper(headers)
		else:
			auth_flag = True

		if not auth_flag:
			return {"indicator": auth_flag, "message": auth_msg}
		else:
			handle_flag = True

			# Do this for POST only
			if content_type != None and input_dictionary["method"] == "POST":
				# Handle differently based on content types
				logging.info("POST content_type: "+content_type)
				logging.info("[json body before decode]: "+str(body))

				if "application/json" in content_type:
					input_dictionary["form"] = json.loads(body)

				elif "application/x-www-form-urlencoded" in content_type:
					body = unquote(body)

					# Try to decode it to utf-8 (if it's a string)
					self.split_body(body, input_dictionary["form"])
				else:
					# Doesn't handle other content types for now
					handle_flag = False

				logging.info("POST body: "+str(input_dictionary["form"]))

			if handle_flag:
				try:
					response = self.service_handler(input_dictionary, **self.configs)
				except GadosServerError as e:
					print("GadosServerError = ",e)
					response = e.json_response

				except LackOfArgumentsError as e:
					print("LackOfArgumentsError = ",e)
					response = e.json_response

				except Exception as e:
					_, _, exc_tb = sys.exc_info()
					fobj = traceback.extract_tb(exc_tb)[-1]
					fname = fobj.filename
					line_no = fobj.lineno

					gse = GadosServerError.buildfromexc(str(e), fname, line_no, ''.join(traceback.format_tb(exc_tb)))
					print("GadosServerError = ",gse)
					response = gse.json_response
			else:
				response = {"indicator": False, "message": "Not supported content-type"}

			return response

	# Helper Functions
	# -------------------------
	def header_helper(self, headers):
		"""
		This is the helper function to return the
		lowercase headers.
		"""
		header_dict = {}
		for key in headers:
			header_dict[key.lower()] = headers[key]
		return header_dict

	def authentication_helper(self, headers):
		"""
		This is the helper function to check whether the
		authentication passed or failed. KEYS
		- Inputs:
			* headers: the headers from HTTP. CANNOT ALTER HEADERS CONTENT
		- Return:
			* (Indicator, Message)
		"""
		#This part handles the authentication for gadgethi
		auth = GadgethiHMAC256Verification(headers['hmac256-result'])
		c = auth.gserver_authentication(str(headers['gadgethi-key'])+str(headers['time']), float(headers['time']), self.configs["gadgethi_secret"])
		if c['indicator']:
			logging.info("authentication pass"+headers['gadgethi-key']+headers['hmac256-result']+headers['time'])
		else:
			logging.error("authentication fail: "+str(headers))

		return c['indicator'], c['message']

	def split_body(self, body, dictionary):
		"""
		transform the http post to python dictionary

		>>> d = {}
		>>> d["form"] = {}
		>>> body = "way=1&lon=19.32940&len=2349"
		>>> split_body(body, d["form"])
		>>> print(d)
		{'form': {'way': '1', 'lon': '19.32940', 'len': '2349'}}
		"""
		try:
			out = body.split('&')
			for i in range(len(out)):
				out[i] = out[i].replace("+", " ")
		except:
			out = []

		for item in out:
			try:
				temp_list = item.split('=')
				dictionary[temp_list[0]] = temp_list[1]
			except:
				raise GadosServerError("decode get/post request error. item: "+item+" doesn't use the query format")
