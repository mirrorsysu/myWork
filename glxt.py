# -*- coding: UTF-8 -*-
__author__ = 'Hejing'

from contextlib import closing
import sqlite3

class GLXT:
    def __init__(self):
        self.userdateSite = 'userdate.db'
        self.mailSite = ''
        self.jwxtSite = ''
        self.userdateSchema = 'userdateSchema.sql'
        self.mailSchema = 'mailSchema.sql'
        self.jwxtSchema = 'jwxtSchema.sql'
        self.log_in = 0
        self.username = ''
        try:
            open(self.userdateSite,"r")
        except Exception,e:
            self.init_userdb()

    def menu(self):
        if(self.log_in == 0):
            print 'Please iuput the number to:'
            print '1.Login'
            print '2.Register'
            choose = raw_input()
            if choose == '1':
                return self.login()
            elif choose == '2':
                return self.register()
            else :
                print 'Your input is not legal.'
        elif(self.log_in == 1):
            return self.username

    def login(self):
        print 'Please iuput the username and password to login.'
        print 'And enter back to go back to the menu'
        error = None
        username = raw_input('Please input the username:')
        if username == 'back' :
            return self.menu()
        password = raw_input('Please input the password:')
        error = self.is_valid(username, password,'login')
        if error == None:
            self.log_in = 1
            print 'Login Success.'
            self.username = username
            return self.menu()
        else:
            print error
            return self.menu()

    #
    def logout(self):
        self.username = ''
        self.mailSite = ''
        self.jwxtSite = ''
        self.log_in = 0

    #
    def register(self):
        print 'Please iuput the username and password to register a new user.'
        print 'And enter back to go back to the menu'
        error = None
        username = raw_input('Please input the username:')
        if username == 'back' :
            return self.menu()
        password = raw_input('Please input the password:')
        error = self.is_valid(username, password,'register')
        if error is None:
            self.insertUser(username, password)
            print 'Register success.'
            return self.menu()
        else:
            print error
            return self.menu()

    def is_valid(self, username, password, s):
        g = self.connect_userdb()
        error = None
        if username == '' or password == '':
            error = 'The username and password could not be empty.'
            return error
        if(s == 'login'):
            #查找数据库中的用户名和密码
            cur = g.cursor().execute('select password from users where username = (?)',
            [username])
            passwordList = [str(row[0])  for row in cur.fetchall()]
            print passwordList
            if str(password) not in passwordList:
                error =  'Invalid username or password'
        elif(s == 'register'):
            #判断用户名是否重复
            cur = g.cursor().execute('select username from users')
            userList = [str(row[0]) for row in cur.fetchall()]
            print userList
            if str(username) in userList:
                error = 'The username has been registered.'
        g.close()
        return error

    def insertUser(self, username, password):
        g = self.connect_userdb()
        g.execute('insert into users(username,password) values (?, ?)',
                         [username, password])
        g.commit()
        g.close()
        self.mailSite = username + 'Mail.db'
        self.jwxtSite = username + 'Jwxt.db'
        self.init_maildb()
        self.init_jwxtdb()

    #初始化数据库
    def init_userdb(self):
        with closing(self.connect_userdb()) as db:
            with open(self.userdateSchema,"r") as f:
                db.cursor().executescript(f.read())
            db.commit()

    def init_maildb(self):
        with closing(self.connect_maildb()) as db:
            with open(self.mailSchema,"r") as f:
                db.cursor().executescript(f.read())
            db.commit()

    def init_jwxtdb(self):
        with closing(self.connect_jwxtdb()) as db:
            with open(self.jwxtSchema,"r") as f:
                db.cursor().executescript(f.read())
            db.commit()

    def connect_userdb(self):
        return sqlite3.connect(self.userdateSite)
    #连接数据库
    def connect_maildb(self):
        return sqlite3.connect(self.mailSite)
    #连接数据库
    def connect_jwxtdb(self):
        return sqlite3.connect(self.jwxtSite)