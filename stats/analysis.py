import os
import sys
import subprocess
import argparse
import time
import numpy as np
import cPickle as pickle
from bs4 import BeautifulSoup
from AuthUser import AuthUser
from ContentArticle import ContentArticle
from RssArticle import RssArticle
from Event import Event
import parse_dbs
import extract_dumps
import matplotlib.pyplot as plt


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

def distribution_corpus(object_dictionary):
    article_dict = object_dictionary['ARTICLE']
    length_dict = {}
    for article in article_dict:
        soup = BeautifulSoup(article_dict[article].get_body())
        for item in soup.get_text().split(" "):
            if len(item.split('http')) > 1:
                continue
            else:
                if len(item) > 30:
                    print item
                try:
                    length_dict[len(item)] += 1
                except KeyError:
                    length_dict[len(item)] = 1
    print length_dict
    sys.exit()
    return length_dict


def get_events(object_dictionary, corpus_length):
    clicked_word_dict = {}
    clicked_word_len = {}
    for item in object_dictionary:
        if item == 'WORD':
            for word in object_dictionary[item]:
                word_object = object_dictionary[item][word]
                try:
                    clicked_word_dict[word_object.get_word()] += 1
                except KeyError:
                    clicked_word_dict[word_object.get_word()] = 1
                try: 
                    clicked_word_len[len(word_object.get_word())] += 1
                except KeyError:
                    clicked_word_len[len(word_object.get_word())] = 1
    word_len = []
    key_len = []
    sec_word_len = []
    sec_key_len = []
    for key in sorted(corpus_length):
        sec_key_len.append(key)
        sec_word_len.append(corpus_length[key])
        try:
            word_len.append(clicked_word_len[key])
        except KeyError:
            word_len.append(0)
    n = len(sec_key_len)
    vals = tuple(word_len)
    second_vals = tuple(sec_word_len)
    ind = np.arange(n)
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, vals, width, color='r')
    rects2 = ax.bar(ind, second_vals, width, color='b')

    ax.set_ylabel('Clicks')
    ax.set_xlabel('Word length')
    ax.set_title('Clicks per word length')

    plt.show()


if __name__ == "__main__":
    decompress, parse_db, dump_directory, db_directory, output_directory = parse_command_line()
    dump_path_list = extract_dumps.get_files(dump_directory)
    print "---"
    pg_path_list = extract_dumps.decompress_files(dump_path_list, db_directory, decompress)
    data_files = {}
    print "---"
    for db in pg_path_list:
        if parse_db:
            print "Parsing database file '" + db + "'..."
        data_files[db.split('/')[1]] = parse_dbs.process_database(db, output_directory, parse_db)
    print "---"
    print "Loading data objects from '" + output_directory + "'..."
    print "---"
    object_dictionary = parse_dbs.load_to_class(data_files)

    corpus_length = distribution_corpus(object_dictionary['a107.txt'])
    get_events(object_dictionary['a107.txt'], corpus_length)
    


