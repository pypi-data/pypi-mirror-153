#-*-coding:utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from urllib.parse import unquote
from io import BytesIO, BufferedReader
import threading

from gadgethiServerUtils._exceptions import *
from gadgethiServerUtils.db_operations import *
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import *

import datetime
import os
import json
import sys
import logging

from os.path import expanduser

class GadgetHiHTTPHandler(SimpleHTTPRequestHandler):
	"""
	This is the base handler of gadgethi http server. 
	"""
	server_configs = {}
	service_redirect = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@classmethod
	def initialize_configs(cls, configs):
		"""
		This is the function to initialize configs
		"""
		cls.server_configs.update(configs)

	@classmethod
	def initialize_service_redirect(cls, service_redirect):
		"""
		This is the function to initialize configs 
		"""
		cls.service_redirect = service_redirect

	def do_GET(self):
		print ("Inside server do_GET")
		d = {}
		d["method"] = "GET"
		d["values"] = {}

		self.send_response(200)
		self.end_headers()

		if self.server_configs["serverAuthentication"]:
			# Get authentication information
			auth_flag, auth_msg = self.authentication_helper(self.headers, self.client_address[0], 
							**self.server_configs)
		else:
			auth_flag = True

		# Return if authentication failed early
		if not auth_flag:
			self.wfile.write(bytes(json.dumps({"indicator": auth_flag, "message": auth_msg}), 'utf-8'))
		else:
			try:
				self.split_query_string(self.path, d)
				response = self.service_redirect(d, **self.server_configs)

			except GadosServerError as e:
				print("GadosServerError = ",e)
				response = e.json_response

			except LackOfArgumentsError as e:
				print ("LackOfArgumentsError = ",e)
				response = e.json_response

			except Exception as e:
				_, _, exc_tb = sys.exc_info()
				fobj = traceback.extract_tb(exc_tb)[-1]
				fname = fobj.filename
				line_no = fobj.lineno

				gse = GadosServerError.buildfromexc(str(e), fname, line_no, ''.join(traceback.format_tb(exc_tb)))
				print("GadosServerError = ",gse)
				response = gse.json_response

			if type(response) is BufferedReader:
				# If it's the bufferedreader, meaning that it's an image,
				# read the response out and write it the thre registerfile
				self.wfile.write(response.read())
				response.close()
			elif type(response) is dict:
				# If it's a string, turn it into utf-8 encodings
				try:
					response_string_json = str(json.dumps(response))
				except:
					raise GadosServerError("Response not of type Json")

				self.wfile.write(bytes(response_string_json, 'utf-8'))
			else:
				self.wfile.write(bytes(str(response), 'utf-8'))

	def do_POST(self):
		print ("Inside server do_POST")
		d = {}
		d["method"] = "POST"
		d["values"] = {}
		d["form"] = {}

		content_length = int(self.headers['Content-Length'])
		content_type = self.headers['Content-Type']
		body = self.rfile.read(content_length)

		self.send_response(200)
		self.end_headers()

		if self.server_configs["serverAuthentication"]:
			# Get authentication information
			auth_flag, auth_msg = self.authentication_helper(self.headers, self.client_address[0], 
							**self.server_configs)
		else:
			auth_flag = True

		# Return if authentication failed early
		if not auth_flag:
			self.wfile.write(bytes(json.dumps({"indicator": auth_flag, "message": auth_msg}), 'utf-8'))
		else:
			# Need a better way to figure out if an request is 
			# an image or not.
			handle_flag = True
			if content_type:
				logging.info("POST content_type: "+content_type)
				logging.info("[json body before decode]: "+str(body))
				if "application/json" in content_type:
					body = body.decode("utf-8")
					d["form"] = json.loads(body)
				else:
					try:
						body = body.decode("utf-8")
						body = unquote(body)

						# Try to decode it to utf-8 (if it's a string)
						self.split_body(body, d["form"])
					except:
						handle_flag = False

			logging.info("POST body: "+str(d["form"]))

			if handle_flag:
				try:
					response = self.service_redirect(d, **self.server_configs)
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
					
				try:
					response_string_json = json.dumps(response)
				except:
					response_string_json = str(response)
			else:
				response_string_json = json.dumps({"indicator": False, "message": "Not supported content-type"})

			self.wfile.write(bytes(response_string_json, 'utf-8'))

	def end_headers(self):
		# Can add CORS restrictions here
		SimpleHTTPRequestHandler.end_headers(self)

	# Helper Functions
	# -------------------------
	def authentication_helper(self, headers, ip, **configs):
		"""
		This is the helper function to check whether the
		authentication passed or failed. KEYS and IP
		- Inputs:
			* headers: the headers from HTTP. CANNOT ALTER HEADERS CONTENT
			* client address: IP address
		- Return:
			* (Indicator, Message)
		"""
		logging.info("IP address: "+ip)

		# Handles allowed IP
		wildcard_ip = False
		for allowed_ip in configs["allowed_ip"]:
			if '*' in allowed_ip:
				truncated_ip = allowed_ip[:allowed_ip.index('*')]
				logging.info("truncated_ip: "+truncated_ip)
				if truncated_ip in ip:
					wildcard_ip = True

		if ip not in configs["allowed_ip"] and not wildcard_ip:
			return False, "IP not allowed"

		#This part handles the authentication for gadgethi
		auth = GadgethiHMAC256Verification(headers['Hmac256-Result'])
		c = auth.gserver_authentication(str(headers['Gadgethi-Key'])+str(headers['time']), float(headers['time']), configs["gadgethi_secret"])
		if c['indicator']:
			logging.info("authentication pass"+headers['Gadgethi-Key']+headers['Hmac256-Result']+headers['time'])
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

	def split_query_string(self, path, dictionary):
		"""
		transform the http query string to python dictionary

		>>> d = {}
		>>> d["values"] = {}
		>>> query = "/?way=1&lon=19.32940&len=2349"
		>>> split_query_string(query, d)
		>>> print(d)
		{'values': {'way': '1', 'lon': '19.32940', 'len': '2349'}}
		"""
		try:
			beginning = path.index('?')
			new_str = path[beginning+1:]
			new_str = unquote(new_str)
		except:
			raise GadosServerError("decode get/post request error. Can't split the query string.")

		self.split_body(new_str, dictionary["values"])

"""
Represents the main class of 
gadgethi server.
"""
class GadgetHiServer(HTTPServer):
	"""
	Schemes:
		gadgethi server scheme and custom server scheme.

	@params table_list: a list of table that is going to be used by this server. 
	@params initialized_func_list: a list of functions to init the db tables.
	@params desc: description of the server
	@params configs: All the other configurations setting
	@params service_handler: If using gadgethi server scheme, this is the service handler function
	@params config_path: file path to server config yaml
	@params credential_path: file path to credential yaml
	@params custom_event_handler: If using custom server scheme, this is the handler function
	@params authentication: Set to true if need to turn on header authentication

	# Fetch Yaml Deprecated
	# New scheme requires user put fetch files definition in config file
	- s3_bucket_name: e.g. gadgethi-001
	- fetch_s3_files: e.g. ["database_ini/database.ini", "doday_yamls/*"]
	- local_s3_locations: e.g. ["util/database.ini", "yamls/*"]
	"""
	def __init__(self, table_list=[], initialize_func_list=[], desc="GadgetHi Main", 
		configs={}, service_handler=lambda: None, 
		config_path="", credential_path="",custom_event_handler=None, 
		authentication=True, aws_fake_server=False, **kwargs):

		if aws_fake_server:
			"""
			This part is for aws handler fake test server
			"""
			self.http_handler = GadgetHiHTTPHandler
			self.service_handler = service_handler
			
			GadgetHiHTTPHandler.initialize_service_redirect(self.service_handler)

			self.desc = desc
			self.host = configs["server_address"]
			self.port = int(configs["server_port"])

			local_server_address = (self.host, self.port)
			super().__init__(local_server_address, self.http_handler)

			# Set authentication
			configs["serverAuthentication"] = authentication
			GadgetHiHTTPHandler.initialize_configs(configs)

			print("*** Server Initialized ***")
			return

		self.server_config = load_config(config_path)
		self.credentials_config = load_config(credential_path)

		init_log(self.server_config["log_file_path"]+self.server_config["program_header"])

		self.service_handler = service_handler
		self.http_handler = GadgetHiHTTPHandler
		self.desc = desc

		self.host = self.server_config["server_address"]
		self.port = int(self.server_config["server_port"])

		local_server_address = (self.host, self.port)
		super().__init__(local_server_address, self.http_handler)

		# Set authentication
		configs["serverAuthentication"] = authentication

		yaml_config = {}
		yaml_config.update(configs)
		yaml_config.update(self.server_config)
		yaml_config.update(self.credentials_config)

		GadgetHiHTTPHandler.initialize_configs(yaml_config)

		bucket_name = yaml_config.get("s3_bucket_name", None)
		fetch_s3_files = yaml_config.get("fetch_s3_files", [])
		local_s3_locations = yaml_config.get("local_s3_locations", [])
		if bucket_name:
			fetch_from_s3(bucket_name, fetch_s3_files, local_s3_locations, **yaml_config)
		
		if custom_event_handler:
			GadgetHiHTTPHandler.initialize_service_redirect(custom_event_handler)
		else:
			# Gadgethi Server Scheme
			self.server_api_path = self.server_config["server_api_path"]
			self.server_api_dict = read_config_yaml(self.server_api_path)
			GadgetHiHTTPHandler.initialize_service_redirect(self.redirectToServices)

		# db operations init
		generate_db_header(table_list)
		init_db_location(self.server_config)

		# db_operation, connect to correct database specified
		connect_to_database()

		for init_func in initialize_func_list:
			# This initialized all the tables
			init_func()

		print("*** Server Initialized ***")
		logging.info("*** "+self.desc+" Log Initialized *** ")

	def run(self):
		"""
		execution function
		"""
		print('Starting %s Server at ' % self.desc, self.host, ' port: ', self.port)
		self.serve_forever()

	def redirectToServices(self, request_dict, **server_config):
		"""
		This helps redirect to various services
		in the management server.
		"""
		if ("form" in request_dict):
			srv = request_dict["form"]["service"]
		else:
			srv = request_dict["values"]["service"]

		try:
			if ("form" in request_dict):
				srv = request_dict["form"]["service"]
			else:
				srv = request_dict["values"]["service"]
		except:
			raise LackOfArgumentsError(["service"])
		try:
			method = request_dict['method']
		except:
			raise LackOfArgumentsError(['method'])

		try:
			api_context = self.server_api_dict["services"][srv]
		except:
			raise GadosServerError("Service Type not supported.")

		return self.service_handler(request_dict, api_context, method, **server_config)



