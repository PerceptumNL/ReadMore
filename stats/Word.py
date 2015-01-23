class Word():
    """Word object as retrieved from Postgresql db

    Keyword arguments: word event information
    """
    def __init__(self, *kwargs):
        kwargs = kwargs[0]
        self.aid = kwargs['aid']
        self.word = kwargs['word']
        self.eid = kwargs['eid']

    def get_event_id(self):
    	return self.eid

    def get_word(self):
    	return self.word

