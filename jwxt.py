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
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.encryptPass = self.encryptPassword()
        self.captchaSite = 'captcha.jpeg'
        self.loginUrl = 'http://wjw.sysu.edu.cn/mjwxt/sign_in'
        self.captchaUrl = 'http://wjw.sysu.edu.cn/api/get_captcha'
        self.markUrl = 'http://wjw.sysu.edu.cn/api/score'
        self.loginSuccess = '<title>学分绩点 - SYSU 学生微教务</title>'
        self.markMatch = re.compile(r'"kcmc":"(.*?)".*?"xf":"(.*?)".*?"zzcj":"(.*?)".*?"jd":"(.*?)".*?"jsxm":"(.*?)".*?"jxbpm":"(.*?)\\/(.*?)"')
        #self.markMatchNoTeacher = re.compile(r'"kcmc":"(.*?)".*?"xf":"(.*?)".*?"zzcj":"(.*?)".*?"jd":"(.*?)","bzw":".*?","sftg":"1","jxbpm":"(.*?)\\/(.*?)"')
        self.session = requests.Session()
        self.tryTime = 0
        
    def encryptPassword(self): 
        m = hashlib.md5()   
        m.update(self.password)   
        pubkey = 'b6b992d57695d296c6de1ee330a464bf30f21ead1af10fd923a109e9b32efbc1d197663163818f3537c92944f780d7ba00bf830c073974d67d2adfb8bb89306b'
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
        crypto = rsa.encrypt(m.hexdigest().upper(), key)
        crypto = binascii.b2a_hex(crypto)
        return crypto

    def getCaptcha(self):
        print 'Downloading the captcha...'
        self.cpatchaJPG = self.session.get(self.captchaUrl)
        fp = open(self.captchaSite,"w+")
        fp.write(self.cpatchaJPG.content)

    def killCpatcha(self):
        im = Image.open(self.captchaSite)
        text = image_to_string(im)
        im.close()
        return text.replace(' ','').strip()

    def login(self):
            self.tryTime+=1
            print 'This is #%d try' % (self.tryTime)
            self.getCaptcha()
            self.cpatcha = self.killCpatcha()
            data = {
                'username':self.username,
                'password':self.encryptPass,
                'captcha':self.cpatcha
        	}
            response = self.session.post(self.loginUrl, data).content
            if(response.find(self.loginSuccess) != -1) :
                print 'Login Success'
                self.tryTime = 0
                self.getMark()
            else :
                print 'Login failed.'
                if(self.tryTime > 2):
                    print'Login failed. Please check your username and password.'
                    self.tryTime = 0
                    return
                self.login()
            return response    

    def getMark(self):
            year = raw_input('Please enter the year(XXXX-XXXX):')
            if(year == '-1'):
                return
            term = raw_input('Please enter the term:')
            if(term == '-1'):
                return
            pylb = raw_input('Please enter the class(XX):')
            if(pylb == '-1'):
                return
            data = {
                'year':year,
                'term':term,
                'pylb':pylb,
            }
            print 'Getting the score data...'
            response = self.session.get(self.markUrl, params = data).content
            score = re.findall(self.markMatch, response)
            #scoreNoTeacher = re.findall(self.markMatchNoTeacher, response)
            for s in score:
                string = r"Subject Name: {name}   Teacher's name: {tname}   Credit: {credit}   Score: {score}   Point: {point} Rank: {rank}/{total}".format(name = s[0], tname = s[4], credit = s[1], score = s[2], point = s[3], rank = s[5], total = s[6])
                print string
            #for s in scoreNoTeacher:
                #string = r"Subject Name: {name}   Teacher's name: NULL   Credit: {credit}   Score: {score}   Point: {point} Rank: {rank}/{total}".format(name = s[0],  credit = s[1], score = s[2], point = s[3], rank = s[4], total = s[5])
                #print string
            #self.getMark()