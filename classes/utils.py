import hashlib

class Utils:
    def md5(self, string):
        return str(hashlib.md5(string.encode('utf-8')).hexdigest())
