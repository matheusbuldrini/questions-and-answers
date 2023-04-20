#!/usr/bin/env python3
import pymysql


class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "qea"
        self.con = pymysql.connect(host=host,
                                   user=user,
                                   password=password,
                                   db=db,
                                   cursorclass=pymysql.cursors.DictCursor,
                                   autocommit=True,
                                   use_unicode=True, 
                                   charset="utf8")
        self.cur = self.con.cursor()

    def query(self, sql_query):
        # returns list of elements
        self.cur.execute(str(sql_query))
        return self.cur.fetchall()

    def sql(self, sql_query):
        # returns number of affected items
        # print(sql)
        return self.cur.execute(str(sql_query))
