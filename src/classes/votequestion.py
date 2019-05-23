from classes.database import Database
from classes.utils import Utils

class VoteQuestion:

    def __init__(self):
        self.db = Database()
        self.utils = Utils()

    def _insert_vote(self, idquestion, iduser, vote):
    	return self.db.sql('INSERT INTO VoteQuestion(idquestion, iduser, vote) VALUES ('+idquestion+','+iduser+','+vote+')')

    def vote(self, idquestion, iduser, vote):
        self._insert_vote(idquestion, iduser, vote)
