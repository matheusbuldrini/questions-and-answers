import hashlib

class Utils:
    def md5(self, string):
        return str(hashlib.md5(string.encode('utf-8')).hexdigest())

    def validate_not_empty(self, array):
        for item in array:
            if item == '' or item == None :
                return False
        return True
