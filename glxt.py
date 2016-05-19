# -*- coding: UTF-8 -*-
__author__ = 'Hejing'

from contextlib import closing
import sqlite3
import time

#软件登录管理系统
class GLXT:
    def __init__(self):
        #账户数据库路径
        self.userdateSite = 'userdate.db'
        #教务系统账户数据库路径	
        self.jwxtSite = ''	
        #数据库创建格式路径
        self.userdateSchema = 'userdateSchema.sql'	
        self.jwxtSchema = 'jwxtSchema.sql'
        self.log_in = 0
        self.username = ''
        #判断数据库是否存在，无则创建
        try:
            open(self.userdateSite,"r")
        except Exception,e:
            self.init_userdb()
    
    #欢迎以及功能选择界面
    def menu(self):
        #判断是否登录
        if(self.log_in == 0):
            text=(
            '',
            '---*--author by mirrorsysu--*--',
            '*--It\'s my honor to help you--*',
            '*--Please iuput the number to--*',
            '*--1.Login--*',
            '*--2.Register--*',
            '*--3.Exit--*',
            ''
            )
            #格式化输出
            self.printText(text)
            choose = raw_input()
            if choose == '1':
                #登录账户
                return self.login()
            elif choose == '2':
                #注册账户
                return self.register()
            elif choose == '3':
                #注册账户
                return -1
            else :
                #非法输入
                print 'Your input is not legal.'
        elif(self.log_in == 1):
            #登录成功返回用户名
            return self.username

    #账户登录实现
    def login(self):
        text = (
        '',
        '*--Please iuput the username and password to login--*',
        '*--And enter back to go back to the menu--*',
        '',
        )
        self.printText(text)
        #错误信息
        error = None
        username = raw_input('Please input the username:')
        #若输入为back则返回上一级
        if username == 'back' :
            return self.menu()
        password = raw_input('Please input the password:')
        #判断账户名密码是否符合要求
        error = self.is_valid(username, password,'login')
        if error == None:
            self.log_in = 1
            print 'Login Success.'
            self.username = username
            return self.menu()
        else:
            print error
            return self.menu()

    #注销
    def logout(self):
        self.username = ''
        self.mailSite = ''
        self.jwxtSite = ''
        self.log_in = 0

    #账户注册
    def register(self):
        text = (
        '',
        '*--Please iuput the username and password to register a new user--*',
        '*--And enter back to go back to the menu--*',
        ''
        )
        self.printText(text)
        error = None
        #错误信息
        username = raw_input('Please input the username:')
        #若输入为back则返回上一级
        if username == 'back' :
            return self.menu()
        password = raw_input('Please input the password:')
        #判断账户名密码是否符合要求
        error = self.is_valid(username, password,'register')
        if error is None:
            #向数据库插入账户密码数据
            self.insertUser(username, password)
            print 'Register success.'
            return self.menu()
        else:
            print error
            return self.menu()

    #判断账户名密码是否符合要求
    def is_valid(self, username, password, s):
        #连接数据库
        g = self.connect_userdb()
        error = None
        #账户名密码不能为空
        if username == '' or password == '':
            error = 'The username and password could not be empty.'
            return error
        #登录时的判断：账户名密码是否匹配
        if(s == 'login'):
            #获取账户名对应的密码
            cur = g.cursor().execute('select password from users where username = (?)',
            [username])
            passwordList = [str(row[0])  for row in cur.fetchall()]
            #账户名密码不匹配
            if str(password) not in passwordList:
                error =  'Invalid username or password'
        elif(s == 'register'):
            #判断用户名是否重复
            cur = g.cursor().execute('select username from users')
            userList = [str(row[0]) for row in cur.fetchall()]
            #账户名重复
            if str(username) in userList:
                error = 'The username has been registered.'
        g.close()
        return error

    #向数据库插入账户名密码
    def insertUser(self, username, password):
        #连接数据库
        g = self.connect_userdb()
        g.execute('insert into users(username,password) values (?, ?)',
                         [username, password])
        #提交修改
        g.commit()
        #关闭连接
        g.close()
        #创建账户对应的教务系统账户数据库
        self.jwxtSite = username + 'Jwxt.db'
        self.init_jwxtdb()

    #初始化账户数据库
    def init_userdb(self):
        with closing(self.connect_userdb()) as db:
            with open(self.userdateSchema,"r") as f:
                db.cursor().executescript(f.read())
            db.commit()
    #初始化账户对应的教务系统账户数据库
    def init_jwxtdb(self):
        with closing(self.connect_jwxtdb()) as db:
            with open(self.jwxtSchema,"r") as f:
                db.cursor().executescript(f.read())
            db.commit()

    #连接数据库
    def connect_userdb(self):
        return sqlite3.connect(self.userdateSite)

    #连接数据库
    def connect_jwxtdb(self):
        return sqlite3.connect(self.jwxtSite)

    #格式化输出
    def printText(self,text,sleepTime = 0.1):
        for string1 in text:
            time.sleep(sleepTime)
            print string1.center( 70 )
