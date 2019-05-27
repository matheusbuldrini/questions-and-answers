from classes.database import Database
from classes.utils import Utils

class VoteQuestion:

    def __init__(self):
        self.db = Database()
        self.utils = Utils()

    def _insert(self, idquestion, iduser, vote):
    	return self.db.sql('INSERT INTO VoteQuestion(idquestion, iduser, vote) VALUES ('+idquestion+','+iduser+','+vote+')')

    def _select_vote(self, idquestion, iduser):
    	return int(self.db.query('SELECT COUNT(*) AS COUNT FROM VoteQuestion WHERE idquestion = '+idquestion+' AND iduser = '+iduser)[0]['COUNT'])

    def validate_vote(self, idquestion, iduser, vote):
        if self._select_vote(idquestion, iduser) == 0:
            if self._insert(idquestion, iduser, vote) == 1:
                return True
        return False