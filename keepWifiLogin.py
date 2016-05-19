# -*- coding: UTF-8 -*-
__author__ = 'Hejing'
import time
import requests
import urllib2
import re
import time

class KWLI:
    def __init__(self,username,password):
        self.loginUrl = 'http://10.10.2.22/portal/logon.cgi'
        self.username = username
        self.password = password
        self.LoginSuccess = '上线成功'
        self.isLogin = '用户登录'
        self.login = 0

    def keepLogin(self):
        session = requests.Session()
        print '2'
        dataLogin = {
            'PtUser':self.username,
            'PtPwd':self.password,
            'PtButton':'logon',
        }
        dataLogoff = {
            'PtButton':'logoff',
        }
        response = session.post(self.loginUrl, dataLogin).content
        print '3'
        response = unicode(response, "gb2312").encode("utf8")
        if self.is_login(response) == 1:
            self.login = 1
            print 'Login Success'
            #has been login, and set timer to  check next time
        elif self.is_login(response) == 2:
            time.sleep(1)
            self.login = 1
        else:
            if(self.login == 1):
                print 'You have been disconnected. Reconnecting......'
                self.login = 0
                return self.keepLogin()
            else:
                print 'Cannot connect to the website, please check your network or account.'
                return

    def is_login(self, response):
        if response.find(self.LoginSuccess) != -1:
            return 1
        elif response.find(self.isLogin) != -1:
            return 2
        else :
            return 0

if __name__ == '__main__':
    keepWifiLogin = KWLI("hejing33","Rilegou9706")
    print '1'
    keepWifiLogin.keepLogin()