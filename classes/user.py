from database import Database
from utils import Utils

class User:
    def __init__(self):
        self.db = Database()
        self.utils = Utils()

    def _select_all(self):
        return self.db.query('SELECT * FROM User')

    def _select_count_by_email(self, email):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM User WHERE email = "' + email + '"')[0]['COUNT'])

    def _select_count_by_email_password(self, email, password):
        return int(self.db.query('SELECT COUNT(*) AS COUNT FROM User WHERE email = "' + email + '" AND password = "' + self.utils.md5(password) + '"')[0]['COUNT'])

    def _insert(self, fullname, email, password):
        return self.db.sql('INSERT INTO User(fullname, email, password) VALUES ("' + fullname + '", "' + email + '", "' + self.utils.md5(password) + '")')

    def _delete_user(self, email, password):
        return self.db.sql('DELETE FROM User WHERE email = "' + email + '" AND password = "' + self.utils.md5(password) + '"')

    def _select_id_by_email(self, email):
        return self.db.query('SELECT iduser FROM User WHERE email = "' + email + '"')[0]['iduser']

    def _select_all_by_userid(self, userid):
        return self.db.query('SELECT * FROM User WHERE iduser = "' + userid + '"')

    def _update_but_password(self, fullname, email, description, userid):
        return self.db.sql('UPDATE User SET fullname="' + fullname + '", email="' + email + '", description="' + description + '" WHERE iduser = "' + str(userid) + '"')

    def _update_password(self, password, userid):
        return self.db.sql('UPDATE User SET password="' + self.utils.md5(password) + '" WHERE iduser = "' + str(userid) + '"')

    def _delete(self, user_id):
        self.db.sql('DELETE FROM Answer WHERE iduser = "' + str(user_id) + '"')
        self.db.sql('DELETE a FROM Answer a INNER JOIN Question q ON a.idquestion = q.idquestion WHERE q.iduser = "' + str(user_id) + '"')
        self.db.sql('DELETE FROM Question WHERE iduser = "' + str(user_id) + '"')
        self.db.sql('DELETE FROM User WHERE iduser = "' + str(user_id) + '"')

    def get_by_id(self,id):
        data = self._select_all_by_userid(id)
        if len(data) == 1:
            return data[0]
        else:
            return False

    def validate_register(self, fullname, email, password):
        if not self.utils.validate_not_empty([fullname, email, password]):
            return False
        if self._select_count_by_email(email) == 0:
            if self._insert(fullname, email, password) == 1:
                return True
        return False

    def validate_login(self, email, password):
        if not self.utils.validate_not_empty([email, password]):
            return False
        if self._select_count_by_email_password(email, password) == 1:
            return True
        return False

    def validate_update(self, fullname, email, password, description, userid):
        if not self.utils.validate_not_empty([fullname, email, userid]):
            return False
        r = False
        if password != '':
            self._update_password(password, userid)
        self._update_but_password(fullname, email, description, userid)
        return True
