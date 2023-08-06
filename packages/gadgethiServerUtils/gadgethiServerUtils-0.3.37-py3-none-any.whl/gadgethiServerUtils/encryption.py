# -*- coding: UTF-8 -*-
import hashlib
import codecs
import base64
import os
import requests
import ast
from datetime import datetime
import json
from base64 import b64decode, b64encode
from hashlib import sha256
# We will need to select between Cryptodome and Crypto
import Cryptodome
from Cryptodome.Signature import pkcs1_15, PKCS1_PSS, pss, PKCS1_v1_5
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Hash import SHA256, HMAC
import time

# AES message block size
BS = AES.block_size
# open source WORKING padding and unpadding functions
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class GadgetEncryption:
	def __init__(self, key, iv, pub_key=None, AES_decode_mode='base64'):
		"""
		Input:
			- key (string): Secret Key
			- iv (string): IV provided by Intella
		"""
		self.key = key
		self.iv = iv
		self.publicKey_filepath = pub_key
		self.AES_decode_mode = AES_decode_mode

	# POST to intella
	def client_post(self, address, dictionary): 
		"""
		POST to specific address. 
		"""
		to_send = address
		r = requests.post(to_send, json = dictionary)
		data = r.text
		return data

	# Helper functions
	# ----------------------------
	def encodebase64bytes(self, input_byte):
		"""
		This is the helper function to encode bytes array
		to base64 format.
		Input:
			- input byte (bytes)
		Output:
			- base64 encoding byte array (bytes)
		"""
		base64bytes = base64.b64encode(input_byte)
		return base64bytes

	# SHA256
	# ----------------------------
	def sha256encrypt_string(self, hash_string):
		"""
		Use SHA256 to encrypt a string
		Input: 
			- hash_string (string): the string that
			you want to encrypt
		"""
		sha_signature = \
			hashlib.sha256(hash_string.encode()).hexdigest()
		return sha_signature

	# AES
	# -----------------------------
	def encrypt_AES(self, data):
		"""
		This is the AES encryption function
		Input:
			data (string): the input data that
			you want to encrypt
		Output:
			encrypted (string): output data in base64 format
		"""
		data = pad(data)
		cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
		encrypted = cryptor.encrypt(data.encode())
		encrypted = codecs.encode(encrypted, self.AES_decode_mode).decode()
		return encrypted
	def decrypt_AES(self, data):
		"""
		This is the AES decryption function
		Input:
			data (string): the input data that
			you want to decrypt. It is assumed that the input
			data is in base64 format
		Output:
			encrypted (string): output data in base64 format
		"""
		if self.AES_decode_mode == 'hex':
			data = codecs.encode(codecs.decode(data, 'hex'), 'base64').decode()

		data = base64.b64decode(data)
		cryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
		decrypted = cryptor.decrypt(data)
		decrypted = unpad(decrypted)
		# print ("decrypted before decode = ",decrypted)
		decrypted = decrypted.decode('utf-8')
		return decrypted

	# RSA
	# -----------------------------
	def rsaencyption_string(self, message):
		"""
		This is the RSA encryption function
		Input:
			message (bytes): the input data that
			you want to encrypt
		Output:
			encrypted (bytes): output data in base64 format
		"""
		with open(self.publicKey_filepath) as f:
			key = f.read()
			rsakey = RSA.importKey(key)
			cipher = Cipher_pkcs1_v1_5.new(rsakey)
			cipher_text = base64.b64encode(cipher.encrypt(message))
		return cipher_text

	def hashFunction(self, message):
		hashed = sha256(message.encode("UTF-8")).hexdigest()
		return hashed

	def verify(self,dictionary):
		"""
		Use for verifying the message send from Intella
		- Input: (dictionary)
			message(after encode)
			signature(provided from the Intella dictionary)
		- Output:
			True:successfully authenticate
			False:successfully authenticate
		"""
		message,signature = self.prepareforauthenticatedata(dictionary)
		print ("message in verify = ",message)
		signature = base64.b64decode(signature)
		print ("signature = ",signature)
		key = RSA.importKey(open(self.publicKey_filepath).read())
		h = SHA256.new(message)
		print ("h = ",h)
		verifier = PKCS1_v1_5.new(key)
		if verifier.verify(h,signature):
			return True
		else:
			return False

	# HMAC
	# ------------------------------
	def HMAC256_digest(self,secret,string,mode='base64'):
		if type(secret) != bytes:
			secret = secret.encode()
		h = HMAC.new(secret, digestmod=SHA256)
		if string != bytes:
			string = string.encode()
		h.update(string)
		if mode != 'base64':
			return h.hexdigest()
		else:
			b64 = b64encode(bytes.fromhex(h.hexdigest())).decode()
			return b64

	# Intella API usage
	# ------------------------------
	def getSHA256Password(self, password):
		"""
		This is the function to get the tradekey
		based on Intella API
		"""
		return self.sha256encrypt_string(password)

	def getAPIKey(self):
		"""
		This is the helper function to get 
		API key for Intella API
		"""
		base64key = self.encodebase64bytes(self.key)
		return self.rsaencyption_string(base64key)

	def generateRequestDict(self, request_data):
		"""
		This is the helper function to encode the request dictionary
		to Intella API format
		Input:
			- request_data (dict): Please read the intella api for furhter
			information about this format
		Output:
			- request_dict (dict): A dictionary that is ready to be sent out
		"""
		# self.key = os.urandom(16)
		return {"Request": self.encrypt_AES(str(request_data)).strip('\n'), "ApiKey": self.getAPIKey().decode()}
	
	def decodeIntellaResponse(self, response_dict):
		"""
		This is the helper function to decode the response_string
		based on the Intella API format
		Input:
			- response_dict (dict): {
				"Response": "asdfasfdwer....wertawetg"
			} 
		"""
		response_string = response_dict["Response"]
		response_string = response_string.replace("\n", "")
		response_string = response_string.replace("\u003d", "=")
		return self.decrypt_AES(response_string)
	
	def prepareforauthenticatedata(self,dictionary):
		"""
		This function is use for changing to specific type of string 
		for intella authenticate
		Input:
			- HTTP POST from Intella (dictionary):
			{'MchId': 'gadgethi ', 'MethodName': 'LINE Pay', 'Result': '0000', 'StoreOrderNo': 'PO-20200514-039', 'TotalFee': '1'}
		Output:
			{"MchId":"gadgethi ","MethodName":"LINE Pay","Result":"0000","StoreOrderNo":"PO-20200514-039","TotalFee":"1"}
		"""
		signature = dictionary['Sign']
		dictionary.pop('Sign')
		dictionary = str(dictionary)
		dictionary = dictionary.replace("'","\"")
		dictionary = dictionary.replace(": ",":")
		dictionary = dictionary.replace(", ",",")
		return (dictionary.encode(),signature)
