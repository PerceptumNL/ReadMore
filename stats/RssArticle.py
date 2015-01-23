class RssArticle():
	"""RssArticle object as retrieved from Postgresql db

	Keyword arguments: rss article information
	"""
	def __init__(self, *kwargs):
		kwargs = kwargs[0]
		self.article_id = kwargs['aid']
		self.time = kwargs['time']
		self.url = kwargs['url']
		
	def get_url(self):
		return self.url


