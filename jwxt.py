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

class JWXT:
    def __init__(self, username):
        self.username = username
        self.nowUsername = ''
        self.dbSite = username + 'Jwxt.db'
        self.captchaSite = 'captcha.jpeg'
        self.loginUrl = 'http://wjw.sysu.edu.cn/mjwxt/sign_in'
        self.captchaUrl = 'http://wjw.sysu.edu.cn/api/get_captcha'
        self.markUrl = 'http://wjw.sysu.edu.cn/api/score'
        self.loginSuccess = '<title>学分绩点 - SYSU 学生微教务</title>'
        self.markMatch = re.compile(r'"kcmc":"(.*?)".*?"xf":"(.*?)".*?"zzcj":"(.*?)".*?"jd":"(.*?)".*?"jsxm":"(.*?)".*?"jxbpm":"(.*?)\\/(.*?)"')
        #self.markMatchNoTeacher = re.compile(r'"kcmc":"(.*?)".*?"xf":"(.*?)".*?"zzcj":"(.*?)".*?"jd":"(.*?)","bzw":".*?","sftg":"1","jxbpm":"(.*?)\\/(.*?)"')
        self.tryTime = 0
        self.data = {
                'year':'',
                'term':'',
                'pylb':'',
        }

    def menu(self):
        self.printUser()
        print 'Please input number to choose function'
        print '1.add user'
        print '2.delete user'
        print '3.get mark'
        choose = raw_input()
        if choose == '1':
            self.addUser()
        elif choose == '2':
            self.deleteUser()
        elif choose == '3':
            self.getUserMark()
        else:
            print 'Your input is not legal.'
            self.menu()

    def getUserMark(self):
        error = None
        year = raw_input('Please enter the year(XXXX-XXXX):')
        if(year == '-1'):
            return
        term = raw_input('Please enter the term:')
        if(term == '-1'):
            return
        pylb = raw_input('Please enter the class(XX):')
        if(pylb == '-1'):
            return
        self.data = {
            'year':year,
            'term':term,
            'pylb':pylb,
        }
        print 'Please input the username that you want to get mark.'
        print "Or input \"alluser\" to get all users' mark"
        print 'And enter back to go back to the menu'
        username = raw_input('Please input the username:')
        if username == 'back' :
            return self.menu()
        error = self.is_valid(username, 'Mirror', 'getMark')
        if error is None:
                self.getMarkBegin(username)
        else:
            print error
            return self.menu()

    def addUser(self):
        print 'Please iuput the username and password to add a new user.'
        print 'And enter back to go back to the menu'
        error = None
        username = raw_input('Please input the username:')
        if username == 'back' :
            return self.menu()
        password = raw_input('Please input the password:')
        error = self.is_valid(username, password, 'add')
        if error is None:
            self.insertUser(username, password)
            print 'Add success.'
            return self.menu()
        else:
            print error
            return self.menu()

    def deleteUser(self):
        print 'Please iuput the username to delete a new user.'
        print 'And enter back to go back to the menu'
        error = None
        username = raw_input('Please input the username:')
        if username == 'back' :
            return self.menu()
        error = self.is_valid(username, 'Mirror', 'delete')
        if error is None:
            self.eraseUser(username)
            print 'Delete success.'
            return self.menu()
        else:
            print error
            return self.menu()

    def insertUser(self, username, password):
        g = self.connect_db()
        encrypt_password = self.encryptPassword(password)
        g.execute('insert into users(username,password) values (?, ?)',
                         [username, encrypt_password])
        g.commit()
        g.close()

    def eraseUser(self, username):
        g = self.connect_db()
        g.execute('delete from users where username = (?)',
                         [username])
        g.commit()
        g.close()

    def printUser(self):
        g = self.connect_db()
        cur = g.cursor().execute('select username from users')
        userList = [str(row[0])  for row in cur.fetchall()]
        print 'Now the userlist is:'
        for i in userList:
            print i
        g.close()

    def getUsername(self):
        g = self.connect_db()
        cur = g.cursor().execute('select username from users')
        userList = [str(row[0])  for row in cur.fetchall()]
        g.close()
        return userList
   
    def is_valid(self, username, password, s):
        g = self.connect_db()
        error = None
        if username == '' or password == '':
            error = 'The username and password could not be empty.'
            return error
        if(s == 'add'):
            cur = g.cursor().execute('select username from users')
            userList = [str(row[0])  for row in cur.fetchall()]
            if str(username) in userList:
                error = 'the user has been added.'
        elif(s == 'delete'):
            cur = g.cursor().execute('select username from users')
            userList = [str(row[0])  for row in cur.fetchall()]
            if str(username) not in userList:
                error = 'Cannot find the user.'
        elif(s == 'getMark'):
            cur = g.cursor().execute('select username from users')
            userList = [str(row[0])  for row in cur.fetchall()]
            if str(username) not in userList:
                error = 'Cannot find the user.'
            if username == 'alluser' :
                error = None
        g.close()
        return error

    def getPassword(self,username):
        g = self.connect_db()
        cur = g.cursor().execute('select password from users where username = (?)',
            [username])
        passwordList = [str(row[0])  for row in cur.fetchall()]
        return passwordList[0]
        g.close()

    def encryptPassword(self, password): 
        m = hashlib.md5()   
        m.update(password)   
        pubkey = 'b6b992d57695d296c6de1ee330a464bf30f21ead1af10fd923a109e9b32efbc1d197663163818f3537c92944f780d7ba00bf830c073974d67d2adfb8bb89306b'
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
        crypto = rsa.encrypt(m.hexdigest().upper(), key)
        crypto = binascii.b2a_hex(crypto)
        return crypto

    def getCaptcha(self, session):
        print 'Downloading the captcha...'
        self.cpatchaJPG = session.get(self.captchaUrl)
        fp = open(self.captchaSite,"w+")
        fp.write(self.cpatchaJPG.content)

    def killCpatcha(self):
        im = Image.open(self.captchaSite)
        text = image_to_string(im)
        im.close()
        return text.replace(' ','').strip()

    def getMarkBegin(self, username):
        if username == 'alluser':
            userList = self.getUsername()
            for username in userList:
                self.nowUsername = username
                self.login(username)
        else:
            self.nowUsername = username
            self.login(username)

    def login(self,username):
            session = requests.Session()
            self.tryTime+=1
            print 'This is #%d try in %s' % (self.tryTime, username) 
            self.getCaptcha(session)
            self.cpatcha = self.killCpatcha()
            data = {
                'username':username,
                'password':self.getPassword(username),
                'captcha':self.cpatcha
        	}
            response = session.post(self.loginUrl, data).content
            if(response.find(self.loginSuccess) != -1) :
                print 'Login Success'
                self.tryTime = 0
                self.getMark(session)
            else :
                print 'Login failed.'
                if(self.tryTime > 2):
                    print'Login failed. Please check your username and password.'
                    self.tryTime = 0
                    return self.getUserMark()
                self.login(username)
            return response    

    def getMark(self, session):
            print 'Getting the score data...'
            print '----------------------***Username:%s***----------------------' % (self.nowUsername)
            response = session.get(self.markUrl, params = self.data).content
            score = re.findall(self.markMatch, response)
            #scoreNoTeacher = re.findall(self.markMatchNoTeacher, response)
            for s in score:
                string = r"Subject Name: {name}   Teacher's name: {tname}   Credit: {credit}   Score: {score}   Point: {point} Rank: {rank}/{total}".format(name = s[0], tname = s[4], credit = s[1], score = s[2], point = s[3], rank = s[5], total = s[6])
                print string
            #for s in scoreNoTeacher:
                #string = r"Subject Name: {name}   Teacher's name: NULL   Credit: {credit}   Score: {score}   Point: {point} Rank: {rank}/{total}".format(name = s[0],  credit = s[1], score = s[2], point = s[3], rank = s[4], total = s[5])
                #print string
            #self.getMark()
    def connect_db(self):
        return sqlite3.connect(self.dbSite)