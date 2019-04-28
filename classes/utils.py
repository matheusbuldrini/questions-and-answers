import hashlib
from flask import session

class Utils:
    def md5(self, string):
        return str(hashlib.md5(string.encode('utf-8')).hexdigest())

    def validate_not_empty(self, array):
        for item in array:
            if item == '' or item == None :
                return False
        return True

    def get_alert(self):
        try:
            return session['alert']
        except:
            return False

    def set_alert(self, type, text):
        session['alert'] = {'type': type, 'text': text}

    def unset_alert(self):
        session['alert'] = None
        return ''
