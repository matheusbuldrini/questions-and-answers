from classes.database import Database
from classes.utils import Utils

class VoteAnswer:

    def __init__(self):
        self.db = Database()
        self.utils = Utils()

    def _insert(self, idanswer, iduser, vote):
    	return self.db.sql('INSERT INTO VoteAnswer(idanswer, iduser, vote) VALUES ('+idanswer+','+iduser+','+vote+')')

    def _select_vote(self, idanswer, iduser):
    	return int(self.db.query('SELECT COUNT(*) AS COUNT FROM VoteAnswer WHERE idanswer = '+idanswer+' AND iduser = '+iduser)[0]['COUNT'])

    def validate_vote(self, idanswer, iduser, vote):
        if self._select_vote(idanswer, iduser) == 0:
            if self._insert(idanswer, iduser, vote) == 1:
                return True
        return False