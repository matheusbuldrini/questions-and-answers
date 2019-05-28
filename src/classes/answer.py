from classes.database import Database
from classes.utils import Utils

class Answer:

    def __init__(self):
        self.db = Database()
        self.utils = Utils()

    def _select_all(self):
        return self.db.query('SELECT * FROM Answer')

    def _select_all_by_questionid(self, questionid):
        return self.db.query('SELECT a.idanswer, a.idquestion, a.iduser, a.description, (CASE WHEN b.rating IS NULL THEN 0 ELSE b.rating END) AS rating, DATE_FORMAT(a.data, "%d/%m/%Y %H:%i:%s") AS data, u.fullname AS user_fullname FROM Answer a LEFT JOIN (SELECT idanswer, SUM(vote) AS rating FROM VoteAnswer GROUP BY idanswer) b ON b.idanswer = a.idanswer INNER JOIN User u on a.iduser = u.iduser WHERE a.idquestion = "' + questionid + '"')

    def _select_count_by_author(self, author):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM Answer WHERE author = "' + author + '"')[0]['COUNT'])

    def _insert_vote(self, idanswer, iduser, vote):
        return self.db.sql('INSERT INTO VoteAnswer(idanswer, iduser, vote) VALUES ('+idanswer+','+iduser+','+vote+')')
	
    def _insert(self, idquestion, iduser, description):
        return self.db.sql('INSERT INTO Answer(idquestion, iduser, description) VALUES ("' + idquestion + '", "' + str(iduser) + '", "' + description + '")')

    def _delete(self, answer_id, user_id):
        return self.db.sql('DELETE FROM Answer WHERE idanswer = ' + str(answer_id) + ' AND iduser = ' + str(user_id))

    def _edit(self, answer_description, answer_id):
        return self.db.sql('UPDATE Answer SET description="' + answer_description + '" WHERE idanswer = "' + str(answer_id) + '"')

    def get_by_user(self, user_id):
        return self.db.query('SELECT a.idquestion, a.idanswer, a.description, DATE_FORMAT(a.data, "%d/%m/%Y %H:%i:%s") AS data, q.title, u.fullname FROM Answer a INNER JOIN Question q ON a.idquestion = q.idquestion INNER JOIN User u ON a.iduser = u.iduser WHERE a.iduser = "' + user_id + '"')

    def remove_by_question_id(self, question_id):
        return self.db.sql('DELETE FROM Answer WHERE idquestion = ' + str(question_id))

    def get_iduser_by_idanswer(self, answer_id):
        return self.db.sql('SELECT iduser FROM Answer WHERE idanswer = "' + str(answer_id) + '"')

    def get_by_id(self, answer_id):
        return self.db.query('SELECT q.title, a.iduser, a.description FROM Answer a INNER JOIN Question q ON a.idquestion = q.idquestion WHERE a.idanswer = "' + str(answer_id) + '"')[0]

    def remove(self, answer_id, user_id):
        self._delete(answer_id, user_id)
        return True

    def validate_answer_edit(self, description, user_id, answer_id):
        if not self.utils.validate_not_empty([description, user_id, answer_id]):
            return False
        if user_id:
            return self._edit(description, answer_id)
        else:
            return False

    def validate_answer_post(self, idquestion, iduser, description):
        if not self.utils.validate_not_empty([idquestion, iduser, description]):
            return False
        if iduser:
            return self._insert(idquestion, iduser, description)
        else:
            return False
			
    def vote(self, idanswer, iduser, vote):
        self._insert_vote(idanswer, iduser, vote)
