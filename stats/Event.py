class Event():
    """Event object as retrieved from Postgresql db

    Keyword arguments: event information
    """
    def __init__(self, *kwargs):
    	kwargs = kwargs[0]
        self.eid = kwargs['eid']
        self.time = kwargs['time']
        self.uid = kwargs['uid']
        self.type_id = kwargs['type_id']
        self.object_id = kwargs['object_id']
        self.object_representation = kwargs['object_representation']
        self.action_flag = kwargs['action_flag']
        self.message = kwargs['message']

    def get_action_flag(self):
    	return self.action_flag

    def get_message(self):
    	return self.message

    def get_type(self):
    	return self.type_id

    def get_obj_repr(self):
    	return self.object_representation

    def get_event_id(self):
    	return self.eid
		


