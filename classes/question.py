from classes.database import Database

class Question:

    def __init__(self):
        self.db = Database()

    def _select_all(self):
        return self.db.query('SELECT idquestion, iduser, title, description, DATE_FORMAT(data, "%d/%m/%Y %H:%i:%s") AS data FROM Question ORDER BY data DESC')

    def _select_question_by_title(self, question_title):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM Question WHERE title = "'
                                 + question_title + '"')[0]['COUNT'])

    def get_by_id(self, question_id):
        return self.db.query('SELECT * FROM Question WHERE idquestion = "' +
                                 question_id + '"')

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

    def validate_question_post(self, title, description, user_id):
        if user_id:
            return self._insert(title, description, user_id)
        else:
            return False
