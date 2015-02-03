import psycopg2
import pandas as pd
import sqlite3
import sqlalchemy
import operator
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
pd.options.display.max_colwidth = 10000

class DatabaseConnection:
	def __init__(self, db_url):
		"""Retrieve data from DB and store in relevant dictionaries
		"""
		#Create connection with local database
		self.engine = sqlalchemy.create_engine(db_url)

		#Create dictionary of relevant queries
		queries = {'query_content':"SELECT * FROM content_article;",
		'query_rss':"SELECT * FROM content_rssarticle;",
		'query_event':"SELECT * FROM django_admin_log;",
		'query_word':"SELECT * FROM main_wordhistoryitem;",
		'article_category':"SELECT * FROM content_article_categories;",
		'content_category':"SELECT * FROM content_category;",
		'clicked_article':"SELECT * FROM main_articlehistoryitem;",
		'main_article_user':"SELECT * FROM main_history",
		'main_event':"SELECT * FROM main_event",
		'article_rating':"SELECT * FROM main_articleratingitem",}

		#Create dataframe 
		self.dataframe = {'word':pd.read_sql(queries['query_word'], self.engine), 
		'rss':pd.read_sql(queries['query_rss'], self.engine),
		'article':pd.read_sql(queries['query_content'], self.engine),
		'event':pd.read_sql(queries['query_event'], self.engine),
		'article_category':pd.read_sql(queries['article_category'], self.engine),
		'content_category':pd.read_sql(queries['content_category'], self.engine),
		'clicked_article':pd.read_sql(queries['clicked_article'], self.engine),
		'main_article_user':pd.read_sql(queries['main_article_user'], self.engine),
		'main_event':pd.read_sql(queries['main_event'], self.engine),
		'article_rating':pd.read_sql(queries['article_rating'], self.engine),}

		#Create data dictionaries
		self.length_counts, self.capital_percentage = self.word_length_counts_clicked()
		self.article_clicks = self.article_click_count()
		self.histogram_clicks = self.click_histogram()
		self.read_articles = self.clicked_articles()
		self.read_categories = self.clicked_categories()
		self.category_clicks = self.category_click_count()
		self.category_titles = self.id_to_category(list(self.read_categories.keys()))
		self.article_store = self.get_body_from_id()
		self.corpus_lengths = self.word_length_corpus()
		self.user_article = self.user_article_count()
		self.user_clicks = self.user_click_count()
		self.average_categories = self.get_category_ratings()
	
	def get_category_ratings(self):
		"""Compute average rating per category
		"""
		article_ratings = {}
		number_ratings = {}
		for item in self.dataframe['article_rating']['article_id']:
			print item
			try:
				article_ratings[item] += self.dataframe['article_rating'][self.dataframe['article_rating'].article_id == item]['rating']
			except KeyError:
				article_ratings[item] = self.dataframe['article_rating'][self.dataframe['article_rating'].article_id == item]['rating']
			try:
				number_ratings[item] += 1
			except KeyError:
				number_ratings[item] = 1

		category_frame = self.dataframe['article_category']
		sum_categories = {}
		article_count = {}
		for item in article_ratings:
			ids = category_frame[category_frame.article_id == item]['category_id']
			cat_list = ids.to_dict().values()
			for cat in cat_list:
				rating_sum = article_ratings[item]
				#print rating_sum
				try:
					sum_categories[cat] += rating_sum
				except KeyError:
					sum_categories[cat] = rating_sum
				try:
					article_count[cat] += number_ratings[item]
				except KeyError:
					article_count[cat] = number_ratings[item]

		average_categories = {}
		for category in sum_categories:
			average_categories[category] = float(sum_categories[category]) / article_count[category]

		return average_categories



	def word_length_counts_clicked(self):
		"""Computes the counts of clicks per word length

		Returns:
			length_counts -- Dictionary of click counts per word length
		"""
		length_counts = {}
		capital_count = 0.0
		no_capital_count = 0
		for item in self.dataframe['word']['word']:
			try:
				length_counts[len(item)] += 1
			except KeyError:
				length_counts[len(item)] = 1
			if item[0].isupper():
				capital_count += 1
			else:
				no_capital_count += 1
		return length_counts, capital_count/(capital_count+no_capital_count)

	def article_click_count(self):
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
		return article_clicks

	def category_click_count(self):
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
		return category_clicks

	def user_article_count(self):
		user_dict = {}
		article_hist = self.dataframe['clicked_article']
		main_hist = self.dataframe['main_event']
		for event_id in main_hist['id']:
			data = article_hist[article_hist.event_ptr_id == event_id]
			user_id = main_hist[main_hist.id == event_id]['user_id'].to_dict().values()[0]
			if len(data['article_id'].to_dict().values()):
				try:
					user_dict[user_id] += 1
				except KeyError:
					user_dict[user_id] = 1
		return user_dict

	def user_click_count(self):
		user_dict = {}
		article_hist = self.dataframe['word']
		main_hist = self.dataframe['main_event']
		for event_id in main_hist['id']:
			data = article_hist[article_hist.event_ptr_id == event_id]
			user_id = main_hist[main_hist.id == event_id]['user_id'].to_dict().values()[0]
			if len(data['word'].to_dict().values()):
				try:
					user_dict[user_id] += 1
				except KeyError:
					user_dict[user_id] = 1
		return user_dict

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
		return read_articles

	def word_length_corpus(self):
		"""Compute counts of word lengths over the corpus of read articles

		Returns:
			length_dict -- Dictionary of appearance counts per word length
		"""
		length_dict = {}
		for item in self.article_store:
			soup = BeautifulSoup(self.article_store[item])
			#Get HTML text separated by whitespace and split on line break tags
			for sentence in soup.get_text(separator=u' ').split("<br/>"):
				#For each in a line, retrieve alphanumeric words
				for word in "".join( (char if char.isalnum() else " ") for char in sentence).split():                    
					#Add 1 to word length count
					try:
						length_dict[len(word)] += 1
					except KeyError:
						length_dict[len(word)] = 1
		return length_dict

	def get_body_from_id(self):
		"""Store article body per article id

		Returns:
			article_store -- Dictionary of article body text per article id
		"""
		article_frame = self.dataframe['article']
		article_store = {}
		for item in self.read_articles:
			body_text = article_frame[article_frame.id == item]['body'].values[0]
			article_store[item] = body_text
		return article_store


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
		return read_categories

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
		return category_titles	

	def click_histogram(self):
		click_histogram = {}
		for item in self.article_clicks:
			click_count = self.article_clicks[item]
			try:
				click_histogram[click_count] += 1
			except KeyError:
				click_histogram[click_count] = 1
		return click_histogram

	def bar_plot(self, xticks, scores, ylabel, title):
		"""Creates a bar plot

		Parameters:
			xticks -- The labels for the x axis
			scores -- The data values
			ylabel -- The label for the y axis
			title -- The graph's title
		"""
		N = len(scores)
		ind = np.arange(N)
		width = 0.35
		p1 = plt.bar(ind, scores, width, color='r')
		plt.ylabel(ylabel)
		plt.title(title)
		plt.xticks(ind+width/2., tuple(xticks), rotation=30)
		plt.show()

	def plot_word_lengths(self):
		"""Plots the word length counts
		"""
		self.word_length_counts_clicked()
		xticks = []
		scores = []
		for item in self.length_counts:
			xticks.append(item)
			scores.append(self.length_counts[item])
		self.bar_plot(xticks, scores, 'Aantal keer geklikt', 'Hoe vaak geklikt per woordlengte')

	def plot_clicked_categories(self):
		"""Plots the read article counts per category in a bar chart
		"""
		#Plot bar chart
		xticks = []
		scores = []
		for item in self.read_categories:
			xticks.append(self.category_titles[item])
			scores.append(self.read_categories[item])
		self.bar_plot(xticks, scores, 'Aantal gelezen artikelen', 'Hoeveelheid gelezen artikelen per categorie')

	def plot_normalized_clicked_categories(self):
		"""Plots the clicked word counts per category, normalized over the 
		number of read articles
		"""
		xticks = []
		scores = []
		for item in self.category_clicks:
			scores.append(float(self.category_clicks[item])/self.read_categories[item])
			xticks.append(self.category_titles[item])
		self.bar_plot(xticks, scores, 'Aantal geklikte woorden', 'Hoeveelheid geklikte woorden per categorie, genormaliseerd')


	def plot_category_clicks(self):
		"""Plots the word clicks per category in a bar chart
		"""
		xticks = []
		scores = []
		for item in self.category_clicks:
			xticks.append(self.category_titles[item])
			scores.append(self.category_clicks[item])
		self.bar_plot(xticks, scores, 'Aantal geklikte woorden', 'Hoeveelheid geklikte woorden per categorie')

	def plot_normalized_word_clicks(self):
		"""Plots the number of clicks per word length, normalized over word
		length appearance in the corpus of read articles
		"""
		scores = []
		xticks = []
		for item in self.length_counts:
			scores.append(float(self.length_counts[item])/self.corpus_lengths[item])
			xticks.append(item)
		self.bar_plot(xticks, scores, 'Aantal geklikte woorden', 'Aantal geklikte woorden, genormaliseerd')

	def plot_user_clicks(self):
		"""Plots the number of clicks per user ID
		"""
		xticks = []
		scores = []
		for item in self.user_clicks:
			xticks.append(item)
			scores.append(self.user_clicks[item])
		self.bar_plot(xticks, scores, 'Aantal geklikte woorden', 'Aantal geklikte woorden per gebruiker')

	def plot_user_reads(self):
		"""Plots the number of read articles per user ID
		"""
		xticks = []
		scores = []
		for item in self.user_article:
			xticks.append(item)
			scores.append(self.user_article[item])
		self.bar_plot(xticks, scores, 'Aantal gelezen artikelen', 'Aantal gelezen artikelen per gebruiker')

	def plot_normalized_user_clicks(self):
		"""Plots the number of clicked words per user ID, normalized over read
		articles for that ID
		"""
		xticks = []
		scores = []
		for item in self.user_clicks:
			xticks.append(item)
			scores.append(float(self.user_clicks[item])/self.user_article[item])
		self.bar_plot(xticks, scores, 'Aantal geklikte woorden', 'Aantal geklikte woorden per gebruiker, genormaliseerd')

	def plot_article_clicks(self):
		"""Plots a histogram of articles with 0 clicks, 1 click, 2 clicks, etc
		"""
		xticks = []
		scores = []
		for item in self.histogram_clicks:
			scores.append(self.histogram_clicks[item])
			xticks.append(item)
		self.bar_plot(xticks, scores, 'Aantal artikelen', 'Aantal artikelen met hoeveelheid geklikte woorden')

	def plot_zero_rest_article_clicks(self):
		"""Plots the number of articles without clicks, versus the number of 
		articles with at least one click
		"""
		#Number of times read summed over all articles
		all_count = sum(self.read_articles.values())
		#Number of clicks summed over all articles
		clicked_count = 0
		for item in self.histogram_clicks:
			clicked_count += item * self.histogram_clicks[item]
		#Articles without clicks
		zero = all_count - clicked_count
		xticks = ['0', '>=1']
		scores = [zero, clicked_count]
		self.bar_plot(xticks, scores, 'Aantal geklikte woorden', 'Aantal artikelen zonder vs met clicks')


	def get_read_click_ratio(self):
		"""Computes the read-click ratio, or: how often is an article read
		versus how often are words in the article clicked
		"""
		pass

	def get_capital_percentage(self):
		"""Computes the percentage of clicked words that start with a capital 
		letter: First words in the sentence and/or names/locations, etc.
		"""
		perc = self.capital_percentage * 100 
		return_string = "Geklikte woorden die met een hoofdletter beginnen: %.4f procent." % perc
		return return_string

	def plot_article_ratings(self):
		"""Plots article ratings
		"""
		xticks = []
		scores = []
		for item in self.average_categories:
			xticks.append(item)
			scores.append(self.average_categories[item])


if __name__ == "__main__":
	db_con = DatabaseConnection('postgresql://elise@localhost:5432/read_more')
	#db_con.plot_article_ratings()
	
	#Number of clicks per word length
	db_con.plot_word_lengths()

	#Number of clicks per word length, normalized over read article corpus
	db_con.plot_normalized_word_clicks()
	
	#Number of word clicks per category
	db_con.plot_category_clicks()

	#Number of read articles per category
	db_con.plot_clicked_categories()

	#Number of word clicks per category, normalized over read articles in category
	db_con.plot_normalized_clicked_categories()

	#Ratio artikel geklikt vs woorden in artikel geklikt
	db_con.get_read_click_ratio()
	#Percentage woorden geklikt die met een hoofdletter beginnen
	print db_con.get_capital_percentage()
	#Userid vs aantal geklikte woorden 
	db_con.plot_user_clicks()
	#User id vs aantal gelezen artikelen
	db_con.plot_user_reads()
	#Normalized user ID vs clicked words
	db_con.plot_normalized_user_clicks()
	#grafiek aantal artikelen met 0 woorden, 1, 2, 3 enz
	db_con.plot_article_clicks()
	#grafiek aantal artikelen met 0 kliks, vs 1 of meer
	db_con.plot_zero_rest_article_clicks()


