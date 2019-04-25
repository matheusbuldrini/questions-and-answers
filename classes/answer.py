#!/usr/bin/env python3
from classes.database import Database


class Answer:
    def __init__(self):
        self.db = Database()

    def _select_all(self):
        return self.db.query('SELECT * FROM Answer')

    def _select_all_by_questionid(self, questionid):
        return self.db.query('SELECT * FROM Answer WHERE idquestion = "' + questionid + '"')

    def _select_count_by_author(self, author):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM Answer WHERE author = "' + author + '"')[0]['COUNT'])

    def _insert(self, idquestion, iduser, description):
        return self.db.sql('INSERT INTO Answer(idquestion, iduser, description) VALUES ("' + idquestion + '", "' + iduser + '", "' + description + '")')
