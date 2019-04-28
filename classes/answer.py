from classes.database import Database

class Answer:

    def __init__(self):
        self.db = Database()

    def _select_all(self):
        return self.db.query('SELECT * FROM Answer')

    def _select_all_by_questionid(self, questionid):
        return self.db.query('SELECT a.idanswer, a.idquestion, a.iduser, a.description, DATE_FORMAT(a.data, "%d/%m/%Y %H:%i:%s") AS data, u.fullname as user_fullname FROM Answer a JOIN User u on a.iduser = u.iduser WHERE a.idquestion = "' + questionid + '"')

    def _select_count_by_author(self, author):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM Answer WHERE author = "' + author + '"')[0]['COUNT'])

    def _insert(self, idquestion, iduser, description):
        return self.db.sql('INSERT INTO Answer(idquestion, iduser, description) VALUES ("' + idquestion + '", "' + str(iduser) + '", "' + description + '")')

    def _delete(self, answer_id, user_id):
        return self.db.sql('DELETE FROM Answer WHERE idanswer = ' + str(answer_id) + ' AND iduser = ' + str(user_id))

    def get_by_user(self, user_id):
        return self.db.query('SELECT a.idquestion, a.idanswer, a.description, DATE_FORMAT(a.data, "%d/%m/%Y %H:%i:%s") AS data, q.title, u.fullname FROM Answer a INNER JOIN Question q ON a.idquestion = q.idquestion INNER JOIN User u ON a.iduser = u.iduser WHERE a.iduser = "' + user_id + '"')

    def remove_by_question_id(self, question_id):
        return self.db.sql('DELETE FROM Answer WHERE idquestion = ' + str(question_id))

    def get_iduser_by_idanswer(self, answer_id):
        return self.db.sql('SELECT iduser FROM Answer WHERE idanswer = "' + str(answer_id) + '"')

    def remove(self, answer_id, user_id):
        self._delete(answer_id, user_id)
        return True

