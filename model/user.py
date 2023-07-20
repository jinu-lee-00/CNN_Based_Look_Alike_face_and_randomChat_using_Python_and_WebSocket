import pymysql
import re
from flask import session, request

class User:
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            charset='utf8'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute('USE mbtichat')
                
    def login(self, userID, userPassword):
        self.cursor.execute('SELECT * FROM USER WHERE userID = %s', userID)
        account = self.cursor.fetchone()
        if userID == '': # 아이디 미입력
            return 1
        if userPassword == '': # 비밀번호 미입력
            return 2
        if account == None: # 없는 아이디
            return 3
        if account['userPassword'] != userPassword: # 비밀번호 불일치
            return 4
        if account['userPassword'] == userPassword: # 로그인 성공
            session["userID"] = account['userID']
            session["userPassword"] = account['userPassword']
            session["userName"] = account['userName']
            session["userNickname"] = account['userNickname']
            session["userEmail"] = account['userEmail']
            session["userGender"] = account['userGender']
            session["userMBTI"] = account['userMBTI']
            return account
        else: # 데이터베이스 오류
            return 5
        
    def ID_duplicated(self, userID):
        self.cursor.execute('SELECT * FROM USER WHERE userID = %s', userID)
        account = self.cursor.fetchone()
        if account != None: # ID가 이미 존재
            return True
        
    def join(self, userID, userPassword, userName, userNickname, userEmail, userGender, userMBTI):
        if userID == '': 
            return 1 # ID 미입력
        if self.ID_duplicated(userID):
            return 2 # ID 중복
        if not re.match(r'^[a-zA-Z0-9_]+$', userID):
            return 3 # ID 형식 불일치
        if userPassword == '':
            return 4 # 비밀번호 미입력
        if userName == '':
            return 5 # 이름 미입력
        if userNickname == '':
            return 6 # 닉네임 미입력
        else:
            session["userID"] = userID
            session["userPassword"] = userPassword
            session["userName"] = userName
            session["userNickname"] = userNickname
            session["userEmail"] = userEmail
            session["userGender"] = userGender
            session["userMBTI"] = userMBTI
            self.cursor.execute("INSERT INTO USER VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                                %(userID, userPassword, userName, userNickname, userEmail, userGender, userMBTI))
            self.db.commit()