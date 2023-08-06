#!/usr/bin/env python3
from gadgethiServerUtils.db_operations import *
import collections

def merge_Data(selection_dict, table, multiple_vals=False,other_db="None"):
	"""
	This function reverses the split Data result given selection criterion (ex.order_id).
	After reading from database, get all rows that meet the criterion and merge them back.
	- Input:
		* selection_dict: dict of selection criterion to merge (ex. {'order_id':101...})
		* table: table to operate on (ex.'order')
	- Return:
		* merged_data: dictionary of data (ex. {'order_id':101, 'name1':"['1','2','5']"})
	"""
	where_columns_list, where_value_list = [], []

	for key in selection_dict:
		where_columns_list.append(key)
		where_value_list.append(selection_dict[key])

	# db_components =	generate_db_components(table)

	if not multiple_vals:
		matched_data = get_data(table, where_columns_list, where_value_list)

		merged_data = collections.defaultdict(list)
		for indivisual in matched_data:
			for k, v in indivisual.items():  # d.items() in Python 3+
				try:
					v = ast.literal_eval(v)
				except:
					pass
					
				if k in where_columns_list:
					merged_data[k] = v
					
				else:
					merged_data[k].append(v)
	else:
		# This is the special case, only one where column and value is allowed
		# Need where_columns_list = ["status"]
		# where_value_list = [("1", "2"...)]
		db_components = generate_db_components(table)
		
		query = "SELECT {} FROM {} WHERE {} IN %s".format("%s" % ', '.join(map(str,db_components['columns'])), db_components['table_name'], where_columns_list[0])
		print("query: ", query)
		fetched_data = executeSql(getDb(), query, (where_value_list[0],), db_operations.MODE_DB_W_RETURN_AND_ARGS,other_db=other_db)
		data_list = FormatReturnData(fetched_data) 
		# print ("queue_list = ",queue_list)
		matched_data = FormatReturnDict(db_components['columns'],data_list)

		merged_parent_dict = {}
		for indivisual in matched_data:
			current_order_id = indivisual["order_id"]
			try:
				_ = merged_parent_dict[current_order_id]
			except:
				merged_parent_dict[current_order_id] = collections.defaultdict(list)

			for k, v in indivisual.items():  # d.items() in Python 3+
				try:
					v = ast.literal_eval(v)
				except:
					pass
					
				if k in where_columns_list:
					merged_parent_dict[current_order_id][k] = v
				else:
					merged_parent_dict[current_order_id][k].append(v)

		merged_data = []
		for key in merged_parent_dict.keys():
			merged_data.append(dict(merged_parent_dict[key]))

	# print ("matched_data = ",matched_data)
	# matched_data = [{'order_id':'101', 'name1' : 'beef', 'name2' : "{'sauce':'ketchup'}"}, {'order_id':'101', 'name1' : 'pork', 'name2' : "{'sauce':'mayonaize'}"}]

	# merged_data = {}

	# print ("merged_data = ",merged_data)

	return merged_data

def split_Data(input_data, number_of_data):
	"""
	Break multiple inputs into indivisuals
	- Input
		* input_data: dictionary of data {input_id:101, main:"['1','2','5']" ....}
	- Return
		* splitted_list: list of dictionaries [{input_id:101, main:1...}, {input_id:101....}]
	"""
	# print ("Safe post input in parse = ",input_data)
	# number_of_data = int(input_data["number_of_data"])

	splitted_list = []
	new_input_data = copy.deepcopy(input_data)

	number_of_data = int(number_of_data)

	print ("number_of_data = ",number_of_data)


	try:
		imported_ast = ast.literal_eval("['success']")
	except:
		raise Exception("ast not imported")
	
	for key in new_input_data:
		# print ("Type of value = " , (new_input_data[key]))

		try:
			"""
			Try to view it as a list first, if it's not a list, then
			just copy the thing three times?
			"""
			evaled_value = ast.literal_eval(new_input_data[key])

			# print ("Is list")
			NOT_LIST = False
		except:
			# print ("Not list ")
			NOT_LIST = True

		if NOT_LIST or type(evaled_value) != list:
			new_input_data[key] = [new_input_data[key] for i in range(number_of_data)]
		else:
			try:
				assert len(evaled_value) == number_of_data
				new_input_data[key] = evaled_value
				# new_input_data[key] = str(evaled_value)
				
			except AssertionError:
				raise GadosServerError( "Input key: {} got {}, expecting length to be {}".format(key,new_input_data[key],number_of_data))


	# print ("After expanding new_input_data")
	# print ("New input data = ",new_input_data)

	for i in range(number_of_data):
		"""
		For all bowls, create a copy of dictionary and save it to the
		result list.
		"""
		individual_input_dict = {}
		for key in new_input_data:
			individual_input_dict[key] = new_input_data[key][i]
		splitted_list.append(individual_input_dict)

	return splitted_list


def get_data(table, where_columns_list = 'None', where_value_list = 'None', multiple=False,
		order_by_list = 'None', special_where = False, limit_number ='None',other_db="None"):
	"""

	This function fetches the rows given the arguments at WHERE = %s

	- Input:
		* table: the table to fetch (ex. inventory)
		* where_columns: the name of the conditional columns (ex.['material'])
		* where_value: the value of where_columns should be (ex.['redbean'])
		* special_where: If true, use special generate query for things like 
									SELECT * WHERE order_id LIKE 'DDA-20200701-%'

	- Return:
		* data_dict: list of dictionaries that meet the criterion 
		(ex.[{'redbean':10,....},{....}])

	"""
	db_components = generate_db_components(table)
	# print ("db_components = ",db_components)
	if where_value_list == 'None' or where_value_list == []:
		return []

	if where_columns_list == 'None':
		if not special_where:
			query = generate_query(db_components['table_name'],'SELECT',db_components['columns'],order_by_list=order_by_list,limit_number=limit_number)
		else:
			query = special_generate_query(db_components['table_name'],'SELECT',db_components['columns'],order_by_list=order_by_list,limit_number=limit_number)
		# print ("query = ",query)
		fetched_data = executeSql(getDb(), query, None, db_operations.MODE_DB_W_RETURN_WO_ARGS,other_db=other_db)
		# print ("getDb table = ",getDb())
		# print ("fetched_data = ",fetched_data)
	else:
		if not multiple:
			if not special_where:
				query = generate_query(db_components['table_name'],'SELECT',db_components['columns'],where_columns_list,order_by_list=order_by_list,limit_number=limit_number)
			else:
				query = special_generate_query(db_components['table_name'],'SELECT',db_components['columns'], where_columns_list, order_by_list=order_by_list,limit_number=limit_number)
			
			# print ("query = " + query)
			fetched_data = executeSql(getDb(), query, tuple(where_value_list), db_operations.MODE_DB_W_RETURN_AND_ARGS,other_db=other_db)
		else:
			# multiple execution
			# If this is the case, I would assume that where value list is a list of tuples
			# [(10,), (1,), (2,)] -> and we get multiple matches from db

			# Support Multiple columns in multiple conditions
			# TODO: Need to fix this whole thing in the future.
			column_number_list = []
			deflated_where_value_list = []
			for val in where_value_list:
				if isinstance(val, list):
					column_number_list.append(len(val))
					deflated_where_value_list.extend(val)
				else:
					column_number_list.append(len(where_value_list))
					deflated_where_value_list.extend(where_value_list)
					break

			multi_query = conditional_generate_query(db_components['table_name'],'SELECT',db_components['columns'],where_columns_list,
				column_number_list,order_by_list=order_by_list,limit_number=limit_number)
			fetched_data = executeSql(getDb(), multi_query, tuple(deflated_where_value_list), db_operations.MODE_DB_W_RETURN_AND_ARGS,other_db=other_db)

	# print ("fetched_data in get_data = ",fetched_data)
	data_list = FormatReturnData(fetched_data) 
	# print ("queue_list = ",queue_list)
	data_dict = FormatReturnDict(db_components['columns'],data_list)

	return data_dict


def separate_edit_add(splitted_list, table, where_columns_list):
	"""

	If we perform executemany on ADD operations, some existing 
	rows may be duplicated. We want to edit those instead.

	This function separates splitted_list into two parts:
		1. Editing: Found by fetching in database
		2. Adding: New data not found in database

	- Input:
		* splitted_list: list of dictionaries indicating the data pending execution
		* table: the table to execute (ex. inventory)
		* where_columns: the name of the conditional columns (ex.['material'])
		* where_value: the value of where_columns should be (ex.['redbean'])

	- Return:
		* separted_dict: Dictionary of two lists
			* editing_list: list of dictionaries for edit operation
			* adding_list: list of dictionaries for add operation

	Ex. splitted_list = [{input_id:101, main:1...}, {input_id:102....}, {'input_id':103...}]
	Where input:101 already exists in the database, then the result would become 
	editing_list = [{input_id:101, main:1...}], adding_list = [{input_id:102....}, {'input_id':103...}]

	"""
	separted_dict = {}
	editing_list, adding_list = [], []

	for dictionary in splitted_list:
		where_value_list = [dictionary[key] for key in where_columns_list]
		fetched_data = get_data(table,where_columns_list,where_value_list)

		if (fetched_data == []):
			adding_list.append(dictionary)
		else:
			editing_list.append(dictionary)

	separted_dict['adding_list'], separted_dict['editing_list'] = adding_list, editing_list

	return separted_dict


def add_to_table(table, adding_list,other_db="None"):
	"""
	This is the common function for inserting data,
	there will be no logic tests for checking duplicacy
	
	- Input:
		* table: the table to perform operation on
		* adding_list: list of dictionaries to be add (may be single)

	- Return:
		* message: indicating if the add operation has been successful
	"""
	try:
		db_components = generate_db_components(table)

		add_query = generate_query(db_components['table_name'],'INSERT',db_components['columns'])

		# print ("db_components columns = ",db_components['columns'])

		add_arguments = [extract_data(index, db_components['columns']) for index in adding_list]

	except:
		return False

	# print ("Add arguments = ",add_arguments)

	if (len(add_arguments) == 1):
		result = executeSql(getDb(),add_query,add_arguments[0],db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True
	else:
		result = execute_multiple_Sql(getDb(),add_query,add_arguments,db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True

def add_to_table_general(table, adding_list,other_db="None"):
	"""
	Assume that the key that is to be inserted might be
	less than the total columns of the table. So, add the 
	given keys and keep others to none.

	Also assume that all entries need to have the same columns
	that is to be added. Although it can be less than the db
	columns.
	"""
	try:
		db_components = generate_db_components(table)

		addlist_key = set(adding_list[0].keys())
		db_header_columns = set(db_components['columns'])

		intersect_key = list(addlist_key.intersection(db_header_columns))

		add_query = generate_query(db_components['table_name'],'INSERT',intersect_key)

		add_arguments = [extract_data(entry, intersect_key) for entry in adding_list]
	
	except:
		return False

	if (len(add_arguments) == 1):
		result = executeSql(getDb(),add_query,add_arguments[0],db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True	
	else:
		result = execute_multiple_Sql(getDb(),add_query,add_arguments,db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True

def edit_on_table(table, editing_list, where_columns_list,other_db="None"):
	"""
	This function edits existing row(s)

	- Input:
		* table: table executed 
		* editing_list: list of dictionaries to be edited (may be single)
		* where_columns_list: the name of the conditional columns (ex.['material'])

	- Return:
		* message: indicating if the edit operation has been successful
	"""

	if editing_list == []:
		return True

	# print ("editing_list = ",editing_list)
	try:

		db_components = generate_db_components(table)

		edit_columns = [key for key in editing_list[0] if key in db_components['columns']]

		# print ("edit_columns = ",edit_columns)

		edit_query = generate_query(db_components['table_name'],'UPDATE',edit_columns,where_columns_list)

		# print(edit_query)
		# print ("edit_query = ",edit_query)
		# edit_arguments = [tuple(index.values()) + tuple(index[key] for key in where_columns_list) for index in editing_list]

		edit_arguments = [extract_data(index, edit_columns) + tuple(index[key] for key in where_columns_list) for index in editing_list]

		print ("edit_arguments = ",edit_arguments)

	except:
		return False

	if (len(edit_arguments) == 1):
		# print ("single")
		result = executeSql(getDb(),edit_query,edit_arguments[0],db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True

		# print ("executed")
	else:
		result = execute_multiple_Sql(getDb(),edit_query,edit_arguments,db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True


def delete_from_table(table, deleting_list, where_columns_list,other_db="None"):
	"""
	This function edits existing row(s)

	- Input:
		* table: table executed 
		* deleting_list: list of dictionaries to be deleted (may be single)
		* where_columns_list: the name of the conditional columns (ex.['material'])

	- Return:
		* message: indicating if the edit operation has been successful
	
		order_id   payment   takeout	
		100			 cash      true
		100          line      false
		101          cash      false
	
	Invalid format (each dictionary should have same length of where_column):
		deleting_list: [{"order_id":100}, {"order_id":100, "payment":"line"}]

	"""

	if deleting_list == []:
		return True

	try:

		db_components = generate_db_components(table)

		delete_query = generate_query(db_components['table_name'],'DELETE',[],where_columns_list)

		# Make sure all of deleting list keys are in where_columns_list
		check = set(where_columns_list) == set().union(*deleting_list)
		if not check:
			print ("Mismatch between where_columns_list and deleting_list")
			return False

		delete_arguments = [extract_data(index, where_columns_list) for index in deleting_list]

		print ("delete_arguments = ",delete_arguments)

	except:
		return False

	if (len(delete_arguments) == 1):
		# print ("single")
		result = executeSql(getDb(),delete_query,delete_arguments[0],db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True

		# print ("executed")
	else:
		result = execute_multiple_Sql(getDb(),delete_query,delete_arguments,db_operations.MODE_DB_W_ARGS,other_db=other_db)
		return False if result == False else True






def delete_inventory(delete_data,other_db="None"):
	"""
	delete an specific inventory from the inventory table
	"""
	material = delete_data['material']
	queue_info = get_inventory(material)
	if queue_info == []:
		raise GadosServerError( "This inventory doesn't exist in the inventory table")

	delete_entry = generate_query('inventory_table','DELETE',['material'])
	executeSql(getDb(), delete_entry, (material), db_operations.MODE_DB_W_ARGS,other_db=other_db)
	message = "Material {} deleted on inventory table".format(material)	
	return {"indicator":True, "message": message}


def mass_dictionary(key_list):
	"""
	This function converts every element in the keylist to dictionary. Time saving.
	- Input:
		* key_list: ['order_id','order_no'....]
	- Return:
		* return_dict; {'order_id':order_id, 'order_no':order_no...}
	"""

	return_dict = {}

	for element in key_list:
		return_dict['element'] =  eval(element)

	return return_dict







