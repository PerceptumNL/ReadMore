import os
import sys
import subprocess
import argparse
import time
import cPickle as pickle
from AuthUser import AuthUser
from ContentArticle import ContentArticle
from RssArticle import RssArticle
from Event import Event
from Word import Word
import parse_dbs
import extract_dumps

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
	Also, if there is no db file yet, and you choose to decompress, 
	this code will somehow not find it ..
	"""
	db_name = db.split('/')[1]
	if not os.path.exists(output_directory + '/' + db_name):
		os.makedirs(output_directory + '/' + db_name)
	if write_files:
		database = open(db, 'r')
		output_list = []
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
		database = open(db, 'r')	
		word_data = 0
		word_counter = 0
		for line in database:
			#Get all dumped lines following main_wordhistoryitem line
			if line.split(' ')[0] == 'COPY' and line.split(' ')[1] == 'main_wordhistoryitem':
				word_data = 1
				word_counter += 1
				g = open(output_directory + '/' + db_name + '/word_data', 'w')
				output_list.append(output_directory + '/' + db_name + '/word_data')
				g.write('WORD\n')
			elif line.split('.')[0] != '\\' and word_data == 1:
				g.write(line)
			elif line.split('.')[0] == '\\' and word_data == 1:
				word_data = 0
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
			object_list = {}
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
					object_list[all_data[0]] = user_object
			elif object_type == 'ARTICLE':
				for line in data:
					all_data = line.split('\t')
					arguments = {}
					arguments['aid'] = all_data[0]
					arguments['title'] = all_data[2]
					arguments['body'] = all_data[3]
					arguments['image'] = all_data[4]
					article_object = ContentArticle(arguments)
					object_list[all_data[0]] = article_object
			elif object_type == 'RSS':
				for line in data:
					all_data = line.split('\t')
					arguments = {}
					arguments['aid'] = all_data[0]
					arguments['time'] = all_data[1]
					arguments['url'] = all_data[2].split('\n')[0]
					rss_object = RssArticle(arguments)
					object_list[all_data[0]] = rss_object
			elif object_type == 'EVENT':
				for line in data:
					all_data = line.split('\t')
					arguments = {}
					arguments['eid'] = all_data[0]
					arguments['time'] = all_data[1]
					arguments['uid'] = all_data[2]
					arguments['type_id'] = all_data[3]
					arguments['object_id'] = all_data[4]
					arguments['object_representation'] = all_data[5]
					arguments['action_flag'] = all_data[6]
					arguments['message'] = all_data[7]
					event_object = Event(arguments)
					object_list[all_data[0]] = event_object
			elif object_type == 'WORD':
				for line in data:
					all_data = line.split('\t')
					arguments = {}
					arguments['aid'] = all_data[0]
					arguments['word'] = all_data[1].decode('utf-8').encode('ascii', 'xmlcharrefreplace')
					arguments['eid'] = all_data[2].split('\n')[0]
					word_object = Word(arguments)
					object_list[all_data[2].split('\n')[0]] = word_object
			try:
				object_dictionary[database][object_type] = object_list
			except KeyError:
				object_dictionary[database] = {object_type: object_list}
	return object_dictionary