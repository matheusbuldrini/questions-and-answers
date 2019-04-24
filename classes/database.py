#!/usr/bin/env python3

# Username: h0X0rG27Cf
# Password: X5vM8SVTEO
# Database Name: h0X0rG27Cf
# Server: remotemysql.com
# Port: 3306

# Server: sql10.freemysqlhosting.net
# Name: sql10288957
# Username: sql10288957
# Password: jervEuXDVq
# Port number: 3306
import pymysql


class Database:
    def __init__(self):
        host = "remotemysql.com"
        user = "h0X0rG27Cf"
        password = "X5vM8SVTEO"
        db = "h0X0rG27Cf"
        self.con = pymysql.connect(host=host,
                                   user=user,
                                   password=password,
                                   db=db,
                                   cursorclass=pymysql.cursors.DictCursor,
                                   autocommit=True)
        self.cur = self.con.cursor()

    def query(self, sql_query):
        # returns list of elements
        self.cur.execute(str(sql_query))
        return self.cur.fetchall()

    def sql(self, sql_query):
        # returns number of affected items
        # print(sql)
        return self.cur.execute(str(sql_query))
