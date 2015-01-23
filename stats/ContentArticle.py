class ContentArticle():
	"""ContentArticle object as retrieved from Postgresql db

	Keyword arguments: article information
	"""
	def __init__(self, *kwargs):
		kwargs = kwargs[0]
		self.article_id = kwargs['aid']
		self.title = kwargs['title']
		self.body = kwargs['body']
		self.image = kwargs['image']
	
	def get_body(self):
		return self.body


