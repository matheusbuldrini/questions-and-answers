from classes.database import Database

class Question:

    def __init__(self):
        self.db = Database()

    def _select_all(self):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser ORDER BY data DESC')

    def _select_question_by_title(self, question_title):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser WHERE q.title LIKE "%' + question_title + '%"')

    def get_by_id(self, question_id):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser WHERE q.idquestion = "' + question_id + '"')

    def get_by_user(self, user_id):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser WHERE q.iduser = "' + user_id + '"')

    def _edit(self, question_id, question_new_title, question_new_description):
        return self.db.sql('UPDATE Question SET (title, description) = ("' + question_new_title
                           + '", "' + question_description + '") WHERE id = ("' + question_id + '")')

    def _insert(self, question_title, question_description, question_id_user):
        return self.db.sql('INSERT INTO Question(title, description, iduser) VALUES ("' + question_title
                           + '", "' + question_description + '", "' + str(question_id_user) + '")')

    def _delete(self, question_id):
        return self.db.sql('DELETE FROM Question WHERE idquestion = "' + question_id + '")')

    def get_all(self):
        return self._select_all()

    def get_by_title(self, title_search):
        return self._select_question_by_title(title_search)

    def validate_question_post(self, title, description, user_id):
        if user_id:
            return self._insert(title, description, user_id)
        else:
            return False
