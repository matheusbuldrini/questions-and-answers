from classes.database import Database

class User:
    def __init__(self):
        self.db = Database()

    def _select_all(self):
        return self.db.query('SELECT * FROM User')

    def _select_count_by_email(self, email):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM User WHERE email = "' + email + '"')[0]['COUNT'])

    def _select_count_by_email_password(self, email, password):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM User WHERE email = "' + email + '" AND password = "' + password + '"')[0]['COUNT'])

    def _insert(self, fullname, email, password):
        return self.db.sql('INSERT INTO User(fullname, email, password) VALUES ("' + fullname + '", "' + email + '", "' + password + '")')

    def _delete_user(self, email, password):
        return self.db.sql('DELETE FROM User WHERE email = "' + email + '" AND password = "' + password + '"')

    def _select_id_by_email_password(self, email, password):
        return int(self.db.query('SELECT iduser FROM User WHERE email = "' + email + '" AND password = "' + password + '"'))

    def validate_register(self, fullname, email, password):
        if self._select_count_by_email(email) == 0:
            if self._insert(fullname, email, password) == 1:
                return True
        return False

    def validate_login(self, email, password):
        if self._select_count_by_email_password(email, password) == 1:
            return self._select_id_by_email_password(email, password)
        return False
