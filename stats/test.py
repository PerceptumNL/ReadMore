import psycopg2
import pandas as pd
import sqlite3
import sqlalchemy
import operator
import numpy as np
import matplotlib.pyplot as plt

class DatabaseConnection:
	def __init__(self, db_url):
		self.engine = sqlalchemy.create_engine(db_url)

		queries = {'query_content':"SELECT * FROM content_article;",
		'query_rss':"SELECT * FROM content_rssarticle;",
		'query_event':"SELECT * FROM django_admin_log;",
		'query_word':"SELECT * FROM main_wordhistoryitem;",
		'article_category':"SELECT * FROM content_article_categories;",
		'content_category':"SELECT * FROM content_category;",
		'clicked_article':"SELECT * FROM main_articlehistoryitem;"}

		self.dataframe = {'word':pd.read_sql(queries['query_word'], self.engine), 
		'rss':pd.read_sql(queries['query_rss'], self.engine),
		'article':pd.read_sql(queries['query_content'], self.engine),
		'event':pd.read_sql(queries['query_event'], self.engine),
		'article_category':pd.read_sql(queries['article_category'], self.engine),
		'content_category':pd.read_sql(queries['content_category'], self.engine),
		'clicked_article':pd.read_sql(queries['clicked_article'], self.engine),}

	def word_length_counts_clicked(self):
		"""Computes the counts of clicks per word length

		Returns:
			length_counts -- Dictionary of click counts per word length
		"""
		length_counts = {}
		for item in self.dataframe['word']['word']:
			try:
				length_counts[len(item)] += 1
			except KeyError:
				length_counts[len(item)] = 1
		self.length_counts = length_counts
		return self.length_counts

	def article_clicks(self):
		"""Computes the counts of word clicks per article

		Returns:
			article_clicks -- Dictionary of word clicks per article
		"""
		article_clicks = {}
		for item in self.dataframe['word']['article_id']:
			try:
				article_clicks[item] += 1
			except KeyError:
				article_clicks[item] = 1
		self.article_clicks = article_clicks
		return self.article_clicks

	def category_clicks(self):
		"""Computes the counts of word clicks per category

		Returns:
			category_clicks -- Dictionary of word clicks per category
		"""
		category_clicks = {}
		category_frame = self.dataframe['article_category']
		for item in self.article_clicks:
			ids = category_frame[category_frame.article_id == item]['category_id']
			cat_list = ids.to_dict().values()
			for cat in cat_list:
				counter = self.article_clicks[item]
				try:
					category_clicks[cat] += counter
				except KeyError:
					category_clicks[cat] = counter
		self.category_clicks = category_clicks
		return self.category_clicks

	def clicked_articles(self):
		"""Computes the counts of read articles

		Returns:
			read_articles -- Dictionary of read article counts
		"""
		read_articles = {}
		article_frame = self.dataframe['clicked_article']
		for item in article_frame['article_id']:
			try:
				read_articles[item] += 1
			except KeyError:
				read_articles[item] = 1
		self.read_articles = read_articles
		return self.read_articles

	def clicked_categories(self):
		"""Computes the counts of read articles per category

		Returns:
			read_categories -- Dictionary of read article counts per category
		"""
		read_categories = {}
		category_frame = self.dataframe['article_category']
		for item in self.read_articles:
			ids = category_frame[category_frame.article_id == item]['category_id']
			cat_list = ids.to_dict().values()
			for cat in cat_list:
				counter = self.read_articles[item]
				try:
					read_categories[cat] += counter
				except KeyError:
					read_categories[cat] = counter
		self.read_categories = read_categories
		return self.read_categories

	def plot_word_lengths(self):
		"""Plots the word length counts
		"""
		self.word_length_counts_clicked()
		#Plot bar chart
		xticks = []
		scores = []
		for item in self.length_counts:
			xticks.append(item)
			scores.append(self.length_counts[item])
		N = len(scores)
		ind = np.arange(N)
		width = 0.35
		p1 = plt.bar(ind, scores, width, color='r')
		plt.ylabel('Aantal keer geklikt')
		plt.title('Hoe vaak geklikt per woordlengte')
		plt.xticks(ind+width/2., tuple(xticks), rotation=30)
		#plt.yticks(np.arange(0,81,10))
		plt.show()

	def plot_clicked_categories(self):
		"""Plots the read article counts per category in a bar chart
		"""
		#Get article click dictionary
		self.clicked_articles()
		#Get category click dictionary
		self.clicked_categories()
		#Get category id dictionary
		self.id_to_category(list(self.read_categories.keys()))

		#Plot bar chart
		xticks = []
		scores = []
		for item in self.read_categories:
			xticks.append(self.category_titles[item])
			scores.append(self.read_categories[item])
		N = len(scores)
		ind = np.arange(N)
		width = 0.35
		p1 = plt.bar(ind, scores, width, color='r')
		plt.ylabel('Aantal gelezen artikelen')
		plt.title('Hoeveelheid gelezen artikelen per categorie')
		plt.xticks(ind+width/2., tuple(xticks), rotation=30)
		#plt.yticks(np.arange(0,81,10))
		plt.show()

	def plot_categories(self):
		"""Plots the word clicks per category in a bar chart
		"""
		#Get word length dictionary
		self.word_length_counts_clicked()
		#Get article click dictionary
		self.article_clicks()
		#Get category click dictionary
		self.category_clicks()
		#Get category id dictionary
		self.id_to_category(list(self.category_clicks.keys()))

		#Plot bar chart
		xticks = []
		scores = []
		for item in self.category_clicks:
			xticks.append(self.category_titles[item])
			scores.append(self.category_clicks[item])
		N = len(scores)
		ind = np.arange(N)
		width = 0.35
		p1 = plt.bar(ind, scores, width, color='r')
		plt.ylabel('Aantal geklikte woorden')
		plt.title('Hoeveelheid geklikte woorden per categorie')
		plt.xticks(ind+width/2., tuple(xticks), rotation=30)
		#plt.yticks(np.arange(0,81,10))
		plt.show()	

	def id_to_category(self, id_set):
		"""Finds the title of each category id in id_set

		Parameters:
			id_set -- The ids of categories

		Returns:
			category_titles -- Dictionary that links an id to a title
		"""
		title_frame = self.dataframe['content_category']
		category_titles = {}
		for cat in id_set:
			category_titles[cat] = title_frame[title_frame.id == cat]['title'].to_dict().values()[0]
		self.category_titles = category_titles
		return self.category_titles


if __name__ == "__main__":
	db_con = DatabaseConnection('postgresql://elise@localhost:5432/read_more')
	db_con.plot_word_lengths()
	#print sorted(db_con.clicked_articles().items(), key=operator.itemgetter(1), reverse=True)


