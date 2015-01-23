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
import parse_dbs
import extract_dumps

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
	db_files = []
	if not os.path.exists(db_directory):
		os.makedirs(db_directory)
	if decompress:
		print "Getting dump files from '" + dump_path_list[0].split('/')[0] + "'..."
        print "---"
        print "Decompressing dump files to '" + db_directory + "'..."
        print "---"
	for dump in dump_path_list:
		#pg_file_path = db_directory + '/' + dump.split('/')[1].split('.')[0]
		db_file_path = os.path.join(db_directory, dump.split('/')[1].split('.')[0]+".txt")
		db_files.append(db_file_path)
		#command = 'pg_restore -O ' + dump + ' >> ' + pg_file_path
		if decompress:
			print "Loading dump file '" + dump + "'..."
			command = 'pg_restore -O ' + dump + ' >> ' + db_file_path
			p = subprocess.Popen(command, shell=True)
			print "Dumped file to '" + db_file_path + "'."
	return db_files
