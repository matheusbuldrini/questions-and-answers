import classes.Database as Database

class User:
    def __init__(self):
        self.db = Database.Database()

    def select_all(self):
        return self.db.list('SELECT * FROM user')
		
    def insert(self, nickname, password):
        return self.db.sql('INSERT INTO user(nickname, password) VALUES ("' + nickname + '", "' + password + '")')