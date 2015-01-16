class AuthUser():
	"""User object as retrieved from Postgresql db

	Keyword arguments: user information
	"""
	def __init__(self, *kwargs):
		kwargs = kwargs[0]
		self.user_id = kwargs['uid']
		self.last_login = kwargs['last_login']
		self.username = kwargs['username']
		self.first_name = kwargs['first_name']
		self.last_name = kwargs['last_name']
		self.e_mail = kwargs['e_mail']
		self.is_su = kwargs['is_su']
		self.is_staff = kwargs['is_staff']
		self.is_active = kwargs['is_active']
		self.date_joined = kwargs['date_joined']
		


