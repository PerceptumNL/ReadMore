import psycopg2
import pandas as pd
import sqlite3
import sqlalchemy
import operator

class DatabaseConnection:
	def __init__(self, db_url):
		print "--Connecting to database..", db_url
		self.engine = sqlalchemy.create_engine(db_url)

		queries = {'query_content':"SELECT * FROM content_article;",
		'query_rss':"SELECT * FROM content_rssarticle;",
		'query_event':"SELECT * FROM django_admin_log;",
		'query_word':"SELECT * FROM main_wordhistoryitem;",
		'article_category':"SELECT * FROM content_article_categories;"}

		self.dataframe = {'word':pd.read_sql(queries['query_word'], self.engine), 
		'rss':pd.read_sql(queries['query_rss'], self.engine),
		'article':pd.read_sql(queries['query_content'], self.engine),
		'event':pd.read_sql(queries['query_event'], self.engine),
		'article_category':pd.read_sql(queries['article_category'], self.engine)}

	def word_length_counts_clicked(self):
		print "--Computing word length counts.."
		length_counts = {}
		for item in self.dataframe['word']['word']:
			try:
				length_counts[len(item)] += 1
			except KeyError:
				length_counts[len(item)] = 1
		self.length_counts = length_counts
		return self.length_counts

	def article_clicks(self):
		print "--Computing article clicks.."
		article_clicks = {}
		for item in self.dataframe['word']['article_id']:
			try:
				article_clicks[item] += 1
			except KeyError:
				article_clicks[item] = 1
		self.article_clicks = article_clicks
		return self.article_clicks

	def category_clicks(self):
		print "--Computing category clicks.."
		category_clicks = {}
		category_frame = self.dataframe['article_category']
		for item in self.article_clicks:
			ids = category_frame[category_frame.article_id == item]['category_id']
			cat_list = ids.to_dict().values()
			for cat in cat_list:
				counter = self.article_clicks[item]
				try:
					category_clicks[cat] += 1
				except KeyError:
					category_clicks[cat] = 1
		self.category_clicks = category_clicks
		return self.category_clicks


if __name__ == "__main__":
	db_con = DatabaseConnection('postgresql://elise@localhost:5432/read_more')
	print db_con.word_length_counts_clicked()
	print sorted(db_con.article_clicks().items(), key=operator.itemgetter(1), reverse=True)
	print db_con.category_clicks()



