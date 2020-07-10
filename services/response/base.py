from models import db_session


class Base:
    def __init__(self, line_event_message=None):
        self.line_event_message = line_event_message
        self.db_session = db_session

    def response(self):
        raise NotImplementedError
