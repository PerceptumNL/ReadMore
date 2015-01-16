import os
import subprocess

def get_files(directory):
    """Retrieve all dump files from the specified directory

    Keyword arguments:
    directory -- the directory to retrieve dump files from

    Returns:
    dump_path_list -- a list of paths to checked dump files
    """
    #List all files in directory
    dump_files = os.listdir(directory)
    dump_path_list = []
    for dump in dump_files:
    	#If file is a dump file
        if dump.lower().endswith('.dump'):
        	#Append to dump_path_list
            dump_path_list.append(directory + '/' + dump)
    return dump_path_list

def decompress_files(dump_path_list, db_directory, decompress=True):
	"""Decompress all files in dump_path_list to Postgresql

	Keyword arguments:
	dump_path_list -- the list of relative paths to compressed files

	Returns:
	pg_path_list -- a list of paths to decompressed Postgresql files
	"""
	pg_path_list = []
	for dump in dump_path_list:
		#Get path for decompressed file
		pg_file_path = db_directory + '/' + dump.split('/')[1].split('.')[0]
		#Decompression command writes to pg_file_path
		if decompress:
		    command = 'pg_restore -O ' + dump + ' >> ' + pg_file_path
		    #Run bash command 
		    p = subprocess.Popen(command, shell=True)
		#Append to pg_path_list
		pg_path_list.append(pg_file_path)
	return pg_path_list

def process_database(db, output_directory, write_files=True):
	"""Process the database and load its contents into the correct objects.

	Keyword arguments:
	db -- the path to the database file
	output_directory -- the directory to write output files to

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
				output_list.append(output_directory + "/user_data")
				g.write(line)
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
				g.write(line)
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
				g.write(line)
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
				g.write(line)
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

def load_to_class(data_files):
	for data_file in data_files:
		print data_file

if __name__ == "__main__":
    dump_path_list = get_files('dumps')
    pg_path_list = decompress_files(dump_path_list, 'dbs', decompress=False)
    data_files = []
    for db in pg_path_list:
    	data_files.append(process_database(db, 'output', write_files=False))
    load_to_class(data_files)

    

