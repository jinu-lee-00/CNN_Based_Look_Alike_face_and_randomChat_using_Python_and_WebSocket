import pymysql
import re
from flask import session, request

class Bbs:
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute('USE mbtichat')
    
    def getDate(self):
        self.cursor.execute('SELECT NOW() as current_date')
        return self.cursor.fetchone()["current_date"]
    
    def getNext(self):
        self.cursor.execute('SELECT bbsID FROM BBS ORDER BY bbsID DESC')
        result = self.cursor.fetchone()
        
        if result is not None:
            return int(result['bbsID'])+1
        else:
            return 1
    
    def write(self, bbsTitle, userNickname, bbsContent):
        self.cursor.execute("INSERT INTO BBS VALUES(%s, %s, %s, NOW(), %s, %s)",
                            (self.getNext(), bbsTitle, userNickname, bbsContent, 1))
        self.db.commit()


    def getList(self):
        self.cursor.execute('SELECT * FROM BBS ORDER BY bbsID DESC')
        result = self.cursor.fetchall()
        return result
    
    def getBoard(self, bbsID):
        self.cursor.execute("SELECT * FROM BBS WHERE bbsID = %s", bbsID)
        result = self.cursor.fetchone()
        return result