import os
import sys
import subprocess
import argparse
from AuthUser import AuthUser
from ContentArticle import ContentArticle

def parse_command_line():
    """Parse command line arguments

    Returns: 
    decompress -- a boolean specifying whether dumps should be extracted
    parse_db -- a boolean specifying whether dbs should be parsed into files
    dump_directory -- the directory of the dump files
    db_directory -- the directory of the database files
    output_directory -- the directory of the output files
    """
    parser = argparse.ArgumentParser(description="Run simulation")
    parser.add_argument('-decompress', metavar='Decompress dump files? y/n', type=str)
    parser.add_argument('-parse_db', metavar='Parse database file? y/n', type=str)
    parser.add_argument('-dump_directory', metavar='Specify dump file directory.', type=str)
    parser.add_argument('-db_directory', metavar='Specify database file directory.', type=str)
    parser.add_argument('-output_directory', metavar='Specify output directory.', type=str)
    args = parser.parse_args()

    decompress = 'n'
    parse_db = 'n'
    dump_directory = 'dumps'
    db_directory = 'dbs'
    output_directory = 'output'

    if(vars(args)['decompress'] is not None):
        decompress = vars(args)['decompress']
    if(vars(args)['parse_db'] is not None):
        parse_db = vars(args)['parse_db']
    if(vars(args)['dump_directory'] is not None):
        dump_directory = vars(args)['dump_directory']
    if(vars(args)['db_directory'] is not None):
        db_directory = vars(args)['db_directory']		
    if(vars(args)['output_directory'] is not None):
        output_directory = vars(args)['output_directory']

    if decompress == 'y':
        decompress = True
    else:
    	decompress = False
    if parse_db == 'y':
        parse_db = True
    else:
    	parse_db = False


    if decompress and not parse_db:
    	print "========"
    	print "Warning:"
    	print "You want to decompress files without parsing the new database."
    	print "This means the data that will be used may belong to another database."
    	print "========"

    return decompress, parse_db, dump_directory, db_directory, output_directory

def get_files(dump_directory):
    """Retrieve all dump files from the specified directory

    Arguments:
    directory -- the directory to retrieve dump files from

    Returns:
    dump_path_list -- a list of paths to checked dump files
    """
    #List all files in directory
    dump_files = os.listdir(dump_directory)
    dump_path_list = []
    for dump in dump_files:
    	#If file is a dump file
        if dump.lower().endswith('.dump'):
        	#Append to dump_path_list
            dump_path_list.append(dump_directory + '/' + dump)
    return dump_path_list

def decompress_files(dump_path_list, db_directory, decompress):
	"""Decompress all files in dump_path_list to Postgresql

	Arguments:
	dump_path_list -- the list of relative paths to compressed files

	Returns:
	pg_path_list -- a list of paths to decompressed Postgresql files

	TODO: weird printing bug, doesn't seem to mess up the function tho
	"""
	pg_path_list = []
	print dump_path_list
	for dump in dump_path_list:
		#Get path for decompressed file
		pg_file_path = db_directory + '/' + dump.split('/')[1].split('.')[0]
		#Decompression command writes to pg_file_path
        if decompress:
            print "Loading dump file '" + dump + "'..."
            print "---"
            command = 'pg_restore -O ' + dump + ' >> ' + pg_file_path
            #Run bash command 
            p = subprocess.Popen(command, shell=True)
		#Append to pg_path_list
        pg_path_list.append(pg_file_path)
	return pg_path_list

def process_database(db, output_directory, write_files=True):
	"""Process the database and load its contents into the correct objects.

	Arguments:
	db -- the path to the database file
	output_directory -- the directory to write output files to
	write_files -- boolean signaling whether or not to write files

	Returns:
	output_list -- a list containing paths to output files

	TODO:
	this is a very stupid (and slow) implementation - fix this
	"""
	db_name = db.split('/')[1]
	if not os.path.exists(output_directory + '/' + db_name):
		os.makedirs(output_directory + '/' + db_name)
	if write_files:
		output_list = []
		database = open(db, 'r')
		user_data = 0
		user_counter = 0
		for line in database:
			#Get all dumped lines following auth_user line
			if line.split(' ')[0] == 'COPY' and line.split(' ')[1] == 'auth_user':
				user_data = 1
				user_counter += 1
				g = open(output_directory + '/' + db_name + '/user_data', 'w')
				output_list.append(output_directory + '/' + db_name + "/user_data")
				g.write('USER\n')
			elif line.split('.')[0] != '\\' and user_data == 1:
				g.write(line)
			elif line.split('.')[0] == '\\' and user_data == 1:
				user_data = 0
				g.close()
				break
			elif user_data == 0:
				continue
		database.close()
		database = open(db, 'r')
		article_data = 0
		article_counter = 0			
		for line in database:
			#Get all dumped lines following content_article line
			if line.split(' ')[0] == 'COPY' and line.split(' ')[1] == 'content_article':
				article_data = 1
				article_counter += 1
				g = open(output_directory + '/' + db_name + '/article_data', 'w')
				output_list.append(output_directory + '/' + db_name + '/article_data')
				g.write('ARTICLE\n')
			elif line.split('.')[0] != '\\' and article_data == 1:
				g.write(line)
			elif line.split('.')[0] == '\\' and article_data == 1:
				article_data = 0
				g.close()
				break
			elif article_data == 0:
				continue	
		database.close()
		database = open(db, 'r')			
		rss_data = 0
		rss_counter = 0				
		for line in database:
			#Get all dumped lines following content_rssarticle line
			if line.split(' ')[0] == 'COPY' and line.split(' ')[1] == 'content_rssarticle':
				rss_data = 1
				rss_counter += 1
				g = open(output_directory + '/' + db_name + '/rss_data', 'w')
				output_list.append(output_directory + '/' + db_name + '/rss_data')
				g.write('RSS\n')
			elif line.split('.')[0] != '\\' and rss_data == 1:
				g.write(line)
			elif line.split('.')[0] == '\\' and rss_data == 1:
				rss_data = 0
				g.close()
				break
			elif rss_data == 0:
				continue
		database.close()
		database = open(db, 'r')
		event_data = 0
		event_counter = 0	
		for line in database:
			#Get all dumped lines following django_admin_log line
			if line.split(' ')[0] == 'COPY' and line.split(' ')[1] == 'django_admin_log':
				event_data = 1
				event_counter += 1
				g = open(output_directory + '/' + db_name + '/event_data', 'w')
				output_list.append(output_directory + '/' + db_name + '/event_data')
				g.write('EVENT\n')
			elif line.split('.')[0] != '\\' and event_data == 1:
				g.write(line)
			elif line.split('.')[0] == '\\' and event_data == 1:
				event_data = 0
				g.close()
				break
			elif event_data == 0:
				continue	
		database.close()	
	else:
		output_directory_list = os.listdir(output_directory + '/' + db_name)
		output_list = []
		for output_file in output_directory_list:
			if output_file[0] != '.':
				output_list.append(output_directory + '/' + db_name + '/' + output_file)
	return output_list

def load_to_class(database_data_files):
	"""Get the different data files and load them into lists of objects

	Arguments:
	data_files -- a list of lists containing paths to data files per db

	Returns:
	object_dictionary -- a dictionary of dictionaries, with as keys the db files 
	and as values dictionaries of object lists per type of data
	"""
	object_dictionary = {}
	for database in database_data_files:
		object_dictionary[database] = {}
		database_list = database_data_files[database]
		for data_type in database_list:
			data = open(data_type, 'r')
			object_type =  data.readline().split('\n')[0]
			print object_type
			object_list = []
			if object_type == 'USER':
				for line in data:
					all_data = line.split('\t')
					arguments = {}
					arguments['uid'] = all_data[0]
					arguments['last_login'] = all_data[2]
					arguments['is_su'] = all_data[3]
					arguments['username'] = all_data[4]
					arguments['first_name'] = all_data[5]
					arguments['last_name'] = all_data[6]
					arguments['e_mail'] = all_data[7]
					arguments['is_staff'] = all_data[8]
					arguments['is_active'] = all_data[9]
					arguments['date_joined'] = all_data[10].split('\n')[0]
					user_object = AuthUser(arguments)
					object_list.append(user_object)
			elif object_type == 'ARTICLE':
				for line in data:
					all_data = line.split('\t')
					arguments = {}
					arguments['aid'] = all_data[0]
					arguments['title'] = all_data[2]
					arguments['body'] = all_data[3]
					arguments['image'] = all_data[4]
					article_object = ContentArticle(arguments)
					object_list.append(article_object)
			try:
				object_dictionary[database][object_type] = object_list
			except KeyError:
				object_dictionary[database] = {object_type: object_list}
	return object_dictionary

if __name__ == "__main__":
    decompress, parse_db, dump_directory, db_directory, output_directory = parse_command_line()
    dump_path_list = get_files(dump_directory)
    print "---"
    if decompress:
    	print "Getting dump files from '" + dump_directory + "'..."
    	print "---"
    	print "Decompressing dump files to '" + db_directory + "'..."
    	print "---"
    pg_path_list = decompress_files(dump_path_list, db_directory, decompress)
    data_files = {}
    for db in pg_path_list:
    	if parse_db:
    		print "Parsing database file '" + db + "'..."
    		print "---"
    	data_files[db.split('/')[1]] = process_database(db, output_directory, parse_db)
    print "Loading data objects from '" + output_directory + "'..."
    print "---"
    object_dictionary = load_to_class(data_files)
    for db in object_dictionary:
    	print db
    	for item in object_dictionary[db]:
    		print item
    		#print object_dictionary[db][item]

    

