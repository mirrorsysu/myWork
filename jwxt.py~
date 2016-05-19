# -*- coding: UTF-8 -*-
__author__ = 'Hejing'

import requests
import urllib2
import re
from pytesser import *
import rsa
import binascii
import hashlib   
from contextlib import closing
import sqlite3
import time

#教务系统的登录与查询成绩
class JWXT:
    def __init__(self, username):
	    #从软件登录返回用户名，连接对应的数据库
        self.username = username
	    #当前登录教务系统的用户名
        self.nowUsername = ''
	    #当前用户名对应的教务系统数据库的路径
        self.dbSite = username + 'Jwxt.db'
	    #验证码的路径
        self.captchaSite = 'captcha.jpeg'
	    #登录网址
        self.loginUrl = 'http://wjw.sysu.edu.cn/mjwxt/sign_in'
	    #验证码地址
        self.captchaUrl = 'http://wjw.sysu.edu.cn/api/get_captcha'
	    #获取成绩的地址
        self.markUrl = 'http://wjw.sysu.edu.cn/api/score'
	    #成功登录的返回
        self.loginSuccess = '<title>学分绩点 - SYSU 学生微教务</title>'
	    #抓取成绩的正则表达式
        self.markMatch = re.compile(r'"kcmc":"(.*?)".*?"xf":"(.*?)".*?"zzcj":"(.*?)".*?"jd":"(.*?)".*?"jsxm":"(.*?)".*?"jxbpm":"(.*?)\\/(.*?)"')
        #self.markMatchNoTeacher = re.compile(r'"kcmc":"(.*?)".*?"xf":"(.*?)".*?"zzcj":"(.*?)".*?"jd":"(.*?)","bzw":".*?","sftg":"1","jxbpm":"(.*?)\\/(.*?)"')
	    #尝试登录的次数，大于三则退出
        self.tryTime = 0
	    #查询成绩的参数：学年，学期，类别
        self.data = {
                'year':'',
                'term':'',
                'pylb':'',
        }

    def menu(self):
	    #打印当前用户下的教务系统账户
        self.printUser()
        text = (
        "",
        '*--Please input number to choose function--*',
        '*--1.add user--*',
        '*--2.delete user--*',
        '*--3.get mark--*',
        '*--4.go back--*',
        ""
        )
        self.printText(text)
        choose = raw_input()
        if choose == '1':
            #添加新账户
            self.addUser()
        elif choose == '2':
            #删除用户
            self.deleteUser()
        elif choose == '3':
            #获得成绩
            self.getUserMark()
        elif choose == '4':
            #返回
            return
        else:
            #非法输入
            print 'Your input is not legal.'
            self.menu()
    
    #获得用户成绩
    def getUserMark(self):
        error = None
        #输出查询学年
        year = raw_input('Please enter the year(XXXX-XXXX):')
        if(year == '-1'):
            return
        #输入查询学期
        term = raw_input('Please enter the term:')
        if(term == '-1'):
            return
        #输入查询类别
        pylb = raw_input('Please enter the class(XX):')
        if(pylb == '-1'):
            return
        #产生data
        self.data = {
            'year':year,
            'term':term,
            'pylb':pylb,
        }
        text = (
        '',
        '*--Please input the username that you want to get mark--*',
        "*--Or input \"alluser\" to get all users' mark--*",
        '*--And enter back to go back to the menu--*',
        ''
        )
        self.printText(text)
        #输入查询用户，若为alluser则全部查询
        username = raw_input('Please input the username:')
        #输入为back则返回
        if username == 'back' :
            return self.menu()
        #判断用户名密码是否有效
        error = self.is_valid(username, 'Mirror', 'getMark')
        if error is None:
                #开始获得成绩
                self.getMarkBegin(username)
        else:
            #发生错误
            print error
            return self.menu()

    #添加用户
    def addUser(self):
        text = (
        '',
        '*--Please iuput the username and password to add a new user--*',
        '*--And enter back to go back to the menu--*',
        '',
        )
        self.printText(text)
        error = None
        #输入用户名，back返回
        username = raw_input('Please input the username:')
        if username == 'back' :
            return self.menu()
        #输入密码
        password = raw_input('Please input the password:')
        #判断账户名密码是否有效
        error = self.is_valid(username, password, 'add')
        if error is None:
            #向数据库插入账户
            self.insertUser(username, password)
            print 'Add success.'
            return self.menu()
        else:
            #发生错误
            print error
            return self.menu()

    #删除用户
    def deleteUser(self):
        text = (
        '',
        '*--Please iuput the username to delete a new user--*',
        '*--And enter back to go back to the menu--*',
        ''
        )
        self.printText(text)
        error = None
        #输入要删除的用户名，back返回
        username = raw_input('Please input the username:')
        if username == 'back' :
            return self.menu()
        #判断用户名是否有效
        error = self.is_valid(username, 'Mirror', 'delete')
        if error is None:
            #删除账户
            self.eraseUser(username)
            print 'Delete success.'
            return self.menu()
        else:
            #发生错误
            print error
            return self.menu()

    #向数据库插入文件
    def insertUser(self, username, password):
        #连接数据库        
        g = self.connect_db()
        #加密密码 md5+rsa
        encrypt_password = self.encryptPassword(password)
        #插入账户名密码
        g.execute('insert into users(username,password) values (?, ?)',
                         [username, encrypt_password])
        #提交更改        
        g.commit()
        #关闭数据库连接
        g.close()

    #在数据库删除账户
    def eraseUser(self, username):
        #连接数据库
        g = self.connect_db()
        #删除账户
        g.execute('delete from users where username = (?)',
                         [username])
        g.commit()
        g.close()
    
    #打印所有的教务系统账户
    def printUser(self):
        #连接数据库
        g = self.connect_db()
        #选取所有的账户名
        cur = g.cursor().execute('select username from users')
        #打印所有的账户
        userList = [str(row[0])  for row in cur.fetchall()]
        print 'Now the userlist is:'
        for i in userList:
            print i
        g.close()

    #返回所有的账户名
    def getUsername(self):
        #连接数据库
        g = self.connect_db()
        #选取所有的账户名        
        cur = g.cursor().execute('select username from users')
        userList = [str(row[0])  for row in cur.fetchall()]
        g.close()
        return userList
   
    #判断账户名密码输入是否有效
    def is_valid(self, username, password, s):
        error = None
        #账户名密码不能为空
        if username == '' or password == '':
            error = 'The username and password could not be empty.'
            return error
        #添加账户时
        if(s == 'add'):
            #获得用户名
            userList = self.getUsername()
            #用户名已存在
            if str(username) in userList:
                error = 'the user has been added.'
        #删除账户时        
        elif(s == 'delete'):
            #获得用户名
            userList = self.getUsername()
            #无法找到用户名
            if str(username) not in userList:
                error = 'Cannot find the user.'
        #获得成绩时        
        elif(s == 'getMark'):
            #获得用户名
            userList = self.getUsername()
            #无法找到用户名
            if str(username) not in userList:
                error = 'Cannot find the user.'
            if username == 'alluser' :
                error = None
        return error

    #返回密码
    def getPassword(self,username):
        #连接数据库
        g = self.connect_db()
        #获得用户名对应的密码
        cur = g.cursor().execute('select password from users where username = (?)',
            [username])
        passwordList = [str(row[0])  for row in cur.fetchall()]
        #返回密码
        return passwordList[0]
        g.close()

    #加密密码
    def encryptPassword(self, password): 
        #创建md5
        m = hashlib.md5()
        #密码用md5加密   
        m.update(password)
        #公钥   
        pubkey = 'b6b992d57695d296c6de1ee330a464bf30f21ead1af10fd923a109e9b32efbc1d197663163818f3537c92944f780d7ba00bf830c073974d67d2adfb8bb89306b'
        rsaPublickey = int(pubkey, 16)
        #创建公钥
        key = rsa.PublicKey(rsaPublickey, 65537) 
        #将密码用rsa加密
        crypto = rsa.encrypt(m.hexdigest().upper(), key)
        crypto = binascii.b2a_hex(crypto)
        return crypto

    #下载验证码
    def getCaptcha(self, session):
        print 'Downloading the captcha...'
        #打开验证码地址并下载
        self.cpatchaJPG = session.get(self.captchaUrl)
        fp = open(self.captchaSite,"w+")
        fp.write(self.cpatchaJPG.content)

    #绕过验证码
    def killCpatcha(self):
        #打开验证码图片并解析
        im = Image.open(self.captchaSite)
        text = image_to_string(im)
        im.close()
        return text.replace(' ','').strip()

    #开始获取成绩
    def getMarkBegin(self, username):
        #若为alluser则获取所有账户
        if username == 'alluser':
            #获取所有账户
            userList = self.getUsername()
            #遍历所有用户名
            for username in userList:
                self.nowUsername = username
                #line start!                
                self.login(username)
        #获取单个用户成绩
        else:
            self.nowUsername = username
            #link start!
            self.login(username)

    #link start!
    def login(self,username):            
        session = requests.Session()
        #尝试次数+1
        self.tryTime+=1
        print 'This is #%d try in %s' % (self.tryTime, username)
        #获取验证码 
        self.getCaptcha(session)
        #绕过验证码
        self.cpatcha = self.killCpatcha()
        #生成登录data
        data = {
            'username':username,
            'password':self.getPassword(username),
            'captcha':self.cpatcha
        }
        #获得登录页面的内容
        response = session.post(self.loginUrl, data).content
        #登录成功
        if(response.find(self.loginSuccess) != -1) :
            print 'Login Success'
            self.tryTime = 0
            #开始获取成绩                
            self.getMark(session)
        else :
            #登录失败
            print 'Login failed.'
            #尝试次数大于3
            if(self.tryTime > 2):
                #返回
                print'Login failed. Please check your username and password.'
                self.tryTime = 0
                return self.getUserMark()
                #尝试次数小于3则继续尝试
            self.login(username)
        #返回登录页面内容
        return response    

    #获得用户成绩
    def getMark(self, session):
        print 'Getting the score data...'
        print '----------------------***Username:%s***----------------------' % (self.nowUsername)
        #获得成绩页面内容        
        response = session.get(self.markUrl, params = self.data).content
        #用正则表达式匹配成绩内容
        score = re.findall(self.markMatch, response)
        #scoreNoTeacher = re.findall(self.markMatchNoTeacher, response)
        #遍历成绩内容并格式化输出        
        for s in score:
            string = r"Subject Name: {name}   Teacher's name: {tname}   Credit: {credit}   Score: {score}   Point: {point} Rank: {rank}/{total}".format(name = s[0], tname = s[4], credit = s[1], score = s[2], point = s[3], rank = s[5], total = s[6])
            print string
        print '----------------------***Username:%s***----------------------' % (self.nowUsername)
            #for s in scoreNoTeacher:
                #string = r"Subject Name: {name}   Teacher's name: NULL   Credit: {credit}   Score: {score}   Point: {point} Rank: {rank}/{total}".format(name = s[0],  credit = s[1], score = s[2], point = s[3], rank = s[4], total = s[5])
                #print string
            #self.getMark()

    #连接数据库
    def connect_db(self):
        return sqlite3.connect(self.dbSite)
    
    #格式化输出
    def printText(self,text,sleepTime = 0.1):
        for string1 in text:
            time.sleep(sleepTime)
            print string1.center( 70 )
