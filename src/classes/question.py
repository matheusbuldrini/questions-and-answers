from classes.database import Database
from classes.answer import Answer
from classes.votequestion import VoteQuestion
from classes.utils import Utils
import json


class Question:

    def __init__(self):
        self.db = Database()
        self.answer = Answer()
        self.votequestion = VoteQuestion()
        self.utils = Utils()

    def _select_all(self):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser ORDER BY data DESC')

    def _select_question_by_title(self, question_title):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser WHERE q.title LIKE "%' + question_title + '%"')

    def get_by_id(self, question_id):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, (CASE WHEN v.votes IS NULL THEN 0 ELSE v.votes END) AS votes, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser, (SELECT SUM(vote) AS votes FROM VoteQuestion WHERE idquestion="'+str(question_id)+'") v WHERE q.idquestion = "' + str(question_id) + '"')[0]

    def get_by_user(self, user_id):
        return self.db.query('SELECT u.fullname, q.idquestion, q.iduser, q.title, q.description, DATE_FORMAT(q.data, "%d/%m/%Y %H:%i:%s") AS data FROM Question q INNER JOIN User u ON q.iduser = u.iduser WHERE q.iduser = "' + user_id + '"')

    def _edit(self, question_title, question_description, question_id):
        return self.db.sql('UPDATE Question SET title="' + question_title + '", description="' + question_description + '" WHERE idquestion = "' + str(question_id) + '"')

    def _insert(self, question_title, question_description, question_id_user, question_tag):
        json_tag = json.dumps(question_tag)
        print('INSERT INTO Question(title, description, iduser, tags) VALUES ("' + question_title + '", "' + question_description + '", "' + str(question_id_user) + '", "' + str({"1": "xxx", "2": "yyyy"}) + '")')
        return self.db.sql('INSERT INTO Question(title, description, iduser, tags) VALUES ("' + question_title + '", "' + question_description + '", "' + str(question_id_user) + '", "' + str({"1": "xxx", "2": "yyyy"}) + '")')

    def _delete(self, question_id, user_id):
        return self.db.sql('DELETE FROM Question WHERE idquestion = ' + str(question_id) + ' AND iduser = ' + str(user_id))

    def get_all(self):
        return self._select_all()

    def update(self, question_id, question_new_title, question_new_description):
        if not self.utils.validate_not_empty([ question_id, question_new_title, question_new_description]):
            return False
        return self._edit(question_id, question_new_title, question_new_description)

    def remove(self, question_id, user_id):
        if int(user_id) == int(self.get_by_id(question_id)['iduser']):
            self.answer.remove_by_question_id(question_id)
            self._delete(question_id, user_id)
            return True
        return False

    def get_by_title(self, title_search):
        return self._select_question_by_title(title_search)

    def validate_question_post(self, title, description, user_id, tag, question_id):
        if not self.utils.validate_not_empty([title, description, user_id, tag]):
            return False
        if user_id:
            if question_id:
                return self._edit(title, description, question_id)
            else:
                return self._insert(title, description, user_id, tag)
        else:
            return False
