#!/usr/bin/env python3
import os
import time
import psycopg2
from enum import Enum
from gadgethiServerUtils._exceptions import *
import copy
import ast
import sys
import yaml 
from configparser import ConfigParser

# global configs
all_db_columns = {}
all_db_columns_header_data = {}
db_name = ""
ini_location = ""

def generate_db_header(table_list):
	"""
	This is the helper function to generate
	db header from table list. 
	- Input
		* table_list = ['order', 'promotion']
	"""
	global all_db_columns_header_data

	for table in table_list:
		all_db_columns_header_data["all_"+table+"_columns"] = {'table': table}

def init_db_location(config):
	"""
	This is the helper function to set the
	db name initially. 
	"""
	global db_name, ini_location

	db_name = config["database_name"]
	ini_location = config["local_database_ini_path"]

# Database config
def config(section='doday-main'):
	# create a parser
	parser = ConfigParser()
	# read config file
	parser.read(ini_location)
	
	# Useful debug check to see which database server it connects to
	# print("Section: ", section)
	
	# get section, default to merchandise
	db = {}
	if parser.has_section(section):
		params = parser.items(section)
		for param in params:
			db[param[0]] = param[1]
	else:
		raise Exception('Section {0} not found in the {1} file'.format(section, ini_location))
 
	return db

# MODE FUNCTIONS
# -----------------------------------------------------------------------------------------------------

def isTest():
	return False

def debug_print(db_path, table_name):
	"""
	Print a specific table in database db_path
	"""
	sql = '''SELECT * FROM %s;''' % table_name
	executeSql(db_path, sql, None, db_operations.MODE_DB_W_RETURN_WO_ARGS, debug_print=True) 


def clear_table(db_path, table_name):
	"""
	Print the content of a specific table in database db_path
	"""
	# raise Exception("Are you sure you want to clear table")
	sql = '''DELETE FROM %s;''' % table_name
	executeSql(db_path, sql, None, db_operations.MODE_DB_NORMAL) 


# This function prints psycopg2 Errors with detailed information
def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    # print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    # print ("pgerror:", err.pgerror)
    # print ("pgcode:", err.pgcode, "\n")



# DATABASE INFORMATION
# -----------------------------------------------------------------------------------------------------

def getDb():
	return db_name

def generate_db_components(table):
	"""
	This function generates the database components related to the 
	given table.
	- Input:
		* table: table_name (ex.'inventory')
	- Return:
		components: dictionary of components 
		(ex.{'columns':all_inventory_columns,'table_name':'inventory_table'})
	"""
	components = {}
	components['columns'] = all_db_columns['all_' + table + '_columns']

	if table[0] == "@":
		query_table = table[1:]
	else:
		query_table = table + "_table"


	components['table_name'] = query_table
	# print ("components = ",components)
	return components


# DATABASE CONNECTION
# -----------------------------------------------------------------------------------------------------
def connect_to_database(test=False):
	""" Connect to the PostgreSQL database server """
	global TEST_MODE
	conn = None
	try:
		# read connection parameters. Read from test if we are in the test mode.
		if test:
			params = config(section='tests')
			TEST_MODE = True
		else:
			params = config(section=getDb())
 
		# connect to the PostgreSQL server
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**params)
	  
		# create a cursor
		cur = conn.cursor()
		
   		# execute a statement
		print('PostgreSQL database version:')
		cur.execute('SELECT version()')
 
		# display the PostgreSQL database server version
		db_version = cur.fetchone()
		print(db_version)
	   
	   # close the communication with the PostgreSQL
		cur.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print_psycopg2_exception(error)
		# print(error)
	finally:
		if conn is not None:
			conn.close()
			print('Database connection closed.')

	init_headers()


# GENERATE QUERY STRING
# -----------------------------------------------------------------------------------------------------

def generate_query(table, action, target_column_list, conditional_column_list = 'None', order_by_list = 'None', limit_number = 'None'):
	"""
	action = SELECT, DELETE, CHANGE
	target_column_list = ['base','soup','food1']
	conditional_column_list = ['order_id','order_no']

	Query types:
		Select_complex = '''SELECT * FROM queue_table WHERE status = 'waiting' ORDER BY priority DESC, time ASC, _id ASC limit 1;'''
		Select = '''SELECT * FROM queue_table WHERE order_id = %s ORDER BY priority,time;'''
		Update = '''UPDATE queue_table SET base = %s, soup = %s, main = %s, food1 = %s, food2 = %s, food3 = %s, special = %s, price = %s, discounted_price = %s ,promotion = %s, promotion_key = %s, priority = %s, status = %s WHERE order_id = %s;'''
		Delete = '''DELETE FROM queue_table WHERE order_id = %s ;'''
		Insert = '''INSERT into queue_table (order_id, order_no, base, soup, main, food1, food2, food3, special, price, discounted_price, promotion, promotion_key, priority, status, time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''

	"""
	if conditional_column_list != 'None':
		# print ("conditional_column_list = ",conditional_column_list)
		arguments = map(str,conditional_column_list)
		# print ("arguments = ",arguments)
		conditional_column_string = "WHERE %s" % ' = %s AND '.join(arguments)
		conditional_column_string += " = %s"
		# print ("conditional_column_string ",conditional_column_string)
	else:
		conditional_column_string = ''

	if order_by_list != 'None':
		order_by_string = "ORDER BY %s" % ', '.join(map(str,order_by_list))
		# print ("Order by string = ",order_by_string)
	else:
		order_by_string = ''

	if limit_number != 'None':
		limit_number_string = "limit {}".format(limit_number)
		# print ("limit_number_string = ",limit_number_string)
	else:
		limit_number_string = ''

	if action == 'SELECT':
		# print ("target_column_list = ",target_column_list)
		target_column_tuple = "%s" % ', '.join(map(str,target_column_list))
		table_action_query = "{} {} FROM {} {} {} {};".format(action,target_column_tuple,table,conditional_column_string,order_by_string,limit_number_string)

	elif action == 'UPDATE':
		target_column_tuple = "%s" % '= %s, '.join(map(str,target_column_list))
		target_column_tuple += " = %s"
		table_action_query = '{} {} SET {} {} {} {};'.format(action,table,target_column_tuple,conditional_column_string,order_by_string,limit_number_string)

	elif action == 'DELETE':
		target_column_tuple = ''
		table_action_query = "{} FROM {} {};".format(action,table,conditional_column_string)

	elif action == 'INSERT':
		target_column_tuple = "(%s)" % ', '.join(map(str,target_column_list))
		values_list = ['%s'] * len(target_column_list)
		values_tuple = "VALUES (%s)" % ','.join(map(str,values_list))
		table_action_query = "{} INTO {} {} {};".format(action,table,target_column_tuple,values_tuple)
	return table_action_query


def special_generate_query(table, action, target_column_list, conditional_column_list = 'None', order_by_list = 'None', limit_number = 'None'):
	"""
	Same as generate_queury, but remove the " = " sign if the selection criterion is comparitive
	ex. SELECT X where time >= startime <= endtime
 	"""
	if conditional_column_list != 'None':
		# print ("conditional_column_list = ",conditional_column_list)
		join_arguments = map(str,conditional_column_list)
		# print ("join_arguments = ",join_arguments)
		conditional_column_string = "WHERE %s" % ' %s AND '.join(join_arguments)
		conditional_column_string += "%s"
		# print ("conditional_column_string ",conditional_column_string)
	else:
		conditional_column_string = ''

	if order_by_list != 'None':
		order_by_string = "ORDER BY %s" % ', '.join(map(str,order_by_list))
		# print ("Order by string = ",order_by_string)
	else:
		order_by_string = ''

	if limit_number != 'None':
		limit_number_string = "limit {}".format(limit_number)
		# print ("limit_number_string = ",limit_number_string)
	else:
		limit_number_string = ''

	if action == 'SELECT':
		target_column_tuple = "%s" % ', '.join(map(str,target_column_list))
		table_action_query = "{} {} FROM {} {} {} {};".format(action,target_column_tuple,table,conditional_column_string,order_by_string,limit_number_string)

	elif action == 'UPDATE':
		target_column_tuple = "%s" % '= %s, '.join(map(str,target_column_list))
		target_column_tuple += " = %s"
		table_action_query = '{} {} SET {} {} {} {};'.format(action,table,target_column_tuple,conditional_column_string,order_by_string,limit_number_string)

	elif action == 'DELETE':
		target_column_tuple = ''
		table_action_query = "{} FROM {} {};".format(action,table,conditional_column_string)

	elif action == 'INSERT':
		target_column_tuple = "(%s)" % ', '.join(map(str,target_column_list))
		values_list = ['%s'] * len(target_column_list)
		values_tuple = "VALUES (%s)" % ','.join(map(str,values_list))
		table_action_query = "{} INTO {} {} {};".format(action,table,target_column_tuple,values_tuple)
	return table_action_query


def conditional_generate_query(table, action, target_column_list, conditional_column_list = 'None', conditional_column_number = 1, order_by_list = 'None', limit_number = 'None'):
	"""
	action = SELECT, DELETE, CHANGE
	target_column_list = ['base','soup','food1']
	conditional_column_list = ['order_id','order_no']

	Query types:
		Select_complex = '''SELECT * FROM queue_table WHERE status = 'waiting' ORDER BY priority DESC, time ASC, _id ASC limit 1;'''
		Select = '''SELECT * FROM queue_table WHERE order_id = %s ORDER BY priority,time;'''
		Update = '''UPDATE queue_table SET base = %s, soup = %s, main = %s, food1 = %s, food2 = %s, food3 = %s, special = %s, price = %s, discounted_price = %s ,promotion = %s, promotion_key = %s, priority = %s, status = %s WHERE order_id = %s;'''
		Delete = '''DELETE FROM queue_table WHERE order_id = %s ;'''
		Insert = '''INSERT into queue_table (order_id, order_no, base, soup, main, food1, food2, food3, special, price, discounted_price, promotion, promotion_key, priority, status, time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''

	"""
	# Build Conditional Column String
	# ---------------------------------
	conditional_column_string = ''

	if isinstance(conditional_column_number, list):
		# Build Tuple List
		tuple_list = []
		for num in conditional_column_number:
			tuple_str = "(%s"
			for i in range(num-1):
				tuple_str += ", %s"
			tuple_str += ")"
			tuple_list.append(tuple_str)

		assert len(tuple_list) == len(conditional_column_list)

		# Concatenate
		conditional_column_string = "WHERE "
		for tid in range(len(tuple_list)-1):
			conditional_column_string += conditional_column_list[tid] + ' in {} AND '.format(tuple_list[tid])
		conditional_column_string += conditional_column_list[-1] + ' in {}'.format(tuple_list[-1])

	else:
		# If not list, it has to be 1
		conditional_column_string = "WHERE %s" % ' in %s AND '.join(map(str,conditional_column_list))
		conditional_column_string += " in %s" # End condition for the last column

	if order_by_list != 'None':
		order_by_string = "ORDER BY %s" % ', '.join(map(str,order_by_list))
		# print ("Order by string = ",order_by_string)
	else:
		order_by_string = ''

	if limit_number != 'None':
		limit_number_string = "limit {}".format(limit_number)
		# print ("limit_number_string = ",limit_number_string)
	else:
		limit_number_string = ''

	if action == 'SELECT':
		target_column_tuple = "%s" % ', '.join(map(str,target_column_list))
		table_action_query = "{} {} FROM {} {} {} {};".format(action,target_column_tuple,table,conditional_column_string,order_by_string,limit_number_string)

	elif action == 'UPDATE':
		target_column_tuple = "%s" % '= %s, '.join(map(str,target_column_list))
		target_column_tuple += " = %s"
		table_action_query = '{} {} SET {} {} {} {};'.format(action,table,target_column_tuple,conditional_column_string,order_by_string,limit_number_string)

	elif action == 'DELETE':
		target_column_tuple = ''
		table_action_query = "{} FROM {} {};".format(action,table,conditional_column_string)

	elif action == 'INSERT':
		target_column_tuple = "(%s)" % ', '.join(map(str,target_column_list))
		values_list = ['%s'] * len(target_column_list)
		values_tuple = "VALUES (%s)" % ','.join(map(str,values_list))
		table_action_query = "{} INTO {} {} {};".format(action,table,target_column_tuple,values_tuple)
	return table_action_query


# ENTRY EXECUTION
# -----------------------------------------------------------------------------------------------------

# DB OPERATIONS
class db_operations(Enum):
	MODE_DB_NORMAL = 0
	MODE_DB_W_ARGS = 1
	MODE_DB_W_RETURN_WO_ARGS = 2
	MODE_DB_W_RETURN_AND_ARGS = 3

#TODO: Need to change the code so that it's more generalized and is able
#to accept db_path as argument. If it's able to accept table name, it
#will be even better.

def executeSql(db_path, sql, entries, mode, debug_print=False, header=False, other_db='None'):
	"""
	This helper function connects to 
	the database and execute the sql 
	command

	mode = 0 -> normal execute
	mode = 1 -> execute with arguments
	mode = 2 -> with return values but without arguments
	mode = 3 -> with return values and with arguments
	"""
	ret = None
	conn = None
	try:
		# read database configuration
		if isTest(): 
			params = config(section='tests')
		elif other_db != 'None':
			params = config(section=other_db)
		else: 
			params = config(section=db_path)
		
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**params)

		c = conn.cursor()

		if mode == db_operations.MODE_DB_NORMAL:
			c.execute(sql)

		elif mode == db_operations.MODE_DB_W_ARGS:
			c.execute(sql, entries)

		elif mode == db_operations.MODE_DB_W_RETURN_WO_ARGS:
			c.execute(sql)
			ret = c.fetchall()
			# ret = c.execute(sql).fetchall()
			if header:
				l = [description[0] for description in c.description]
				ret = l[1:]

			if debug_print:
				"""
				If this flag is true, print the database content
				"""
				headers = [description[0] for description in c.description]
				print(tabulate(ret, headers, tablefmt="fancy_grid"))

		elif mode == db_operations.MODE_DB_W_RETURN_AND_ARGS:
			c.execute(sql, entries)
			ret = c.fetchall()
			# ret = c.execute(sql, entries).fetchall()
			if debug_print:
				"""
				If this flag is true, print the database content
				"""
				headers = [description[0] for description in c.description]
				print(tabulate(ret, headers, tablefmt="fancy_grid"))

		conn.commit()
		c.close()

	except (Exception, psycopg2.DatabaseError) as error:
		# print("Database execution error = ",error)
		print_psycopg2_exception(error)
		return False

	finally:
		if conn is not None:
			conn.close()

	return ret


def execute_multiple_Sql(db_path, sql, entries, mode, debug_print=False, header=False, other_db='None'):
	"""
	This helper function connects to 
	the database and execute the sql 
	command

	mode = 0 -> normal execute
	mode = 1 -> execute with arguments
	mode = 2 -> with return values but without arguments
	mode = 3 -> with return values and with arguments

	# ONLY FOR UPDATE AND INSERT
	"""
	ret = None
	conn = None
	try:
		# read database configuration
		if isTest(): 
			params = config(section='tests')
		elif other_db != 'None':
			params = config(section=other_db)
		else: 
			params = config(section=db_path)
		# connect to the PostgreSQL database
		conn = psycopg2.connect(**params)

		c = conn.cursor()

		if mode == db_operations.MODE_DB_NORMAL:
			c.executemany(sql)

		elif mode == db_operations.MODE_DB_W_ARGS:
			c.executemany(sql, entries)

		elif mode == db_operations.MODE_DB_W_RETURN_WO_ARGS:
			c.executemany(sql)
			ret = c.fetchall()
			# ret = c.executemany(sql).fetchall()
			if header:
				l = [description[0] for description in c.description]
				ret = l[1:]

			if debug_print:
				"""
				If this flag is true, print the database content
				"""
				headers = [description[0] for description in c.description]
				print(tabulate(ret, headers, tablefmt="fancy_grid"))

		elif mode == db_operations.MODE_DB_W_RETURN_AND_ARGS:
			c.executemany(sql, entries)
			ret = c.fetchall()
			# ret = c.executemany(sql, entries).fetchall()
			if debug_print:
				"""
				If this flag is true, print the database content
				"""
				headers = [description[0] for description in c.description]
				print(tabulate(ret, headers, tablefmt="fancy_grid"))

		conn.commit()
		c.close()
	except (Exception, psycopg2.DatabaseError) as error:
		# print(error)
		print_psycopg2_exception(error)
		return False

	finally:
		if conn is not None:
			conn.close()

	return ret



# FORMATTING AND EXTRACTION
# -----------------------------------------------------------------------------------------------------

def extract_data(data, key_list):
	"""
	This helper function helps
	extract all the fields in the
	order data and returns a tuple.

	Inputs: order data from safe_post and key_list
	Outputs: data tuple
	"""
	# print ("Inside extract_data")
	# print ("Data in extract_data = ",data)

	data_tuple = ()
	for key in key_list:
		# print ("Key = ",key)
		# print ("Value = ",data[key])
		data_tuple += (data[key],)
	# print ("Data tuple in extract_data = ",data_tuple)
	return data_tuple

def extract_arguments(request, request_type, argument_list):
	"""
	This function replaces the try/except blocks in services where we have to check 
	whether every argument is provided 
	ex. try:
			username = request['values']['username']
		except:
			raise LackOfArgumentsError(["username"])
		try:
			action = request['values']['action']
		except:
			raise LackOfArgumentsError(["action"])
	
	Could be modulized to username, action = extract_arguments(request,'values',['username','action'])
	"""
	argument_tuple = []
	for argument in argument_list:
		try:
			argument = request[request_type][argument]
			argument_tuple.append(argument)
		except:
			raise LackOfArgumentsError([argument])
	if len(argument_tuple) == 1:
		return argument_tuple[0]
	else:
		return tuple(argument_tuple)

def extract_optionals(request, request_type, argument_list, optional_value):
	"""
	This function does not raise exception if the given value is not sent,
	instead it assigns optional_value to it

	- Input:
		* optional_value: "None"

	"""
	argument_tuple = []
	for argument in argument_list:
		try:
			argument = request[request_type][argument]
			argument_tuple.append(argument)
		except:
			argument_tuple.append(optional_value)

	if len(argument_tuple) == 1:
		return argument_tuple[0]
	else:
		return tuple(argument_tuple)

def extract_changed_arguments(request,request_type, column_list):
	"""
	This function replaces the try/except blocks in services where we have to check 
	whether every argument is provided, if not, sent 

	request = {"form":{"main":"1","food1":"3"...}}
	ex. try:
			username = request['values']['username']
		except:
			raise LackOfArgumentsError(["username"])
		try:
			action = request['values']['action']
		except:
			raise LackOfArgumentsError(["action"])
	
	Could be modulized to username, action = extract_arguments(request,'values',['username','action'])
	"""
	changed_arguments_dict = {}
	for key in request[request_type]:
		# Key = main..
		if key in column_list:
			changed_arguments_dict[key] = request[request_type][key]
	return changed_arguments_dict

def FormatReturnData(data):
	"""
	Make the tuple a list
	"""
	ret = []
	# print ("Data in FormatReturnData = ", data )
	for tup in data:
		ret.append(list(tup))
	return ret


def FormatReturnDict(key_list, values_list):
	"""
	key_list = ['order_id', 'order_no', 'base', 'soup', 'main', 'food1', 'food2', 'food3', 'special', 'price', 'discounted_price', 'promotion', 'promotion_key', 'priority', 'status', 'time']
	values_list =   (2d list) 
	[['100', '2', '4', '2', '10', '30', '31', 'LOW_ICE', '95', '60%', 'RXIR25', 0, 'waiting', 1504683418], 
	['101', '2', '4', '2', '10', '30', '31', 'LOW_ICE', '95', '60%', 'RXIR25', 0, 'waiting', 1558337818], 
	['102', '2', '5', '3', '2', '7', '19', 'None', '75', '60%', 'RXIR25', 0, 'waiting', 1553758618],
	['103', '4', '1', '5', '5', '6', '14', 'LOW_ICE', '85', '60%', 'RXIR25', 0, 'waiting', 1560670618]] 

	Return list of dictionaries with keys indicating columns
	[{'order_id' : 101, 'order_no': 3, 'base' : 1 ...}, {'order_id' : 102, 'order_no' : 3 ...}]
	"""
	if values_list == []:
		return []


	return [dict(zip(key_list,index)) for index in values_list]	

def FormatReturnTuple(list_of_dict, key_list):
	"""
	This function converts list of dicts into list of tuples by key_list order
	"""
	index_map = {v: i for i, v in enumerate(key_list)}
	
	sorted(list_of_dict.items(), key=lambda pair: index_map[pair[0]])


def FormatDictList(list_of_dict, key_list):
	"""
	Convert list of dict by order of key_list
	"""
	ordered_list = []
	for dictionary in list_of_dict:
		ordered_component = list(extract_data(dictionary, key_list))
		ordered_list.append(ordered_component)
	return ordered_list



# INIT FUNCTIONS
# ------------------------------------------------------------------
def init_headers():
	global all_db_columns

	for columns in all_db_columns_header_data:
		# If no table name specified, see it as a skip
		# print ("Columns in init_headers = ",columns)
		try:
			table_name = all_db_columns_header_data[columns]['table']
			# print ("table name = ",table_name)
		except:
			continue

		# If you want full name, add @ in the front of your table name
		if table_name[0] == "@":
			query_table_name = table_name[1:]
		else:
			query_table_name = table_name + "_table"

		query_string = '''SELECT * FROM %s limit 1;''' % query_table_name
		all_db_columns[columns] = executeSql(getDb(),query_string,None,db_operations.MODE_DB_W_RETURN_WO_ARGS,header=True)
